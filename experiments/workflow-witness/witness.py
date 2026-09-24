#!/usr/bin/env python3
"""Record and verify the hinges of a small file-based workflow.

A manifest declares ordered shell steps plus their input/output files. The witness
records hashes at each boundary and treats validation failures as route failures,
not as ordinary command failures hidden by a successful final artifact.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root: Path, paths: list[str]) -> dict[str, dict[str, Any]]:
    out = {}
    for raw in paths:
        p = (root / raw).resolve()
        try:
            rel = str(p.relative_to(root.resolve()))
        except ValueError:
            rel = raw
        out[rel] = {"exists": p.exists(), "sha256": sha256(p), "bytes": p.stat().st_size if p.exists() and p.is_file() else None}
    return out


_SYSCALL_PATH = re.compile(r"(?:openat|open|newfstatat|statx|stat|lstat|access|unlink|mkdir|rename|chmod|execve)\([^,]*,?\s*\"((?:[^\"\\]|\\.)*)\"")


def captured_paths(log: Path, root: Path) -> dict[str, list[str]]:
    """Extract in-root file paths observed by strace, conservatively.

    This is an observation layer, not a sandbox: syscall parsing is intentionally
    incomplete and only reports paths that can be normalized under the workflow root.
    """
    seen: dict[str, set[str]] = {"read": set(), "write": set(), "other": set()}
    root = root.resolve()
    for line in log.read_text(errors="replace").splitlines():
        match = _SYSCALL_PATH.search(line)
        if not match:
            continue
        raw = bytes(match.group(1), "utf-8").decode("unicode_escape")
        path = Path(raw)
        if not path.is_absolute():
            path = root / path
        try:
            rel = path.resolve().relative_to(root)
        except ValueError:
            continue
        # Directory probes and failed import/path lookups are not file dependencies.
        if not path.exists() or not path.is_file():
            continue
        rel_s = str(rel)
        if "execve(" in line:
            kind = "other"
        else:
            kind = "write" if any(op in line for op in ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "unlink(", "rename(")) else "read"
        seen[kind].add(rel_s)
    return {key: sorted(value) for key, value in seen.items()}


def run(manifest_path: Path, out_path: Path, capture: bool = False) -> int:
    manifest = json.loads(manifest_path.read_text())
    root = manifest_path.parent.resolve()
    steps = manifest.get("steps", [])
    if not steps:
        raise SystemExit("manifest has no steps")
    trace: dict[str, Any] = {
        "workflow": manifest.get("name", manifest_path.stem),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root": str(root),
        "steps": [],
        "status": "passed",
    }
    prior_outputs: set[str] = set()
    for i, step in enumerate(steps, 1):
        name = step.get("name", f"step-{i}")
        inputs = list(step.get("inputs", []))
        outputs = list(step.get("outputs", []))
        declared = list(dict.fromkeys(inputs + outputs))
        before = snapshot(root, declared)
        missing_inputs = [p for p in inputs if not (root / p).is_file()]
        for p in inputs:
            if p not in prior_outputs and i > 1 and p not in manifest.get("source_inputs", []):
                # This is a warning only: external inputs are legitimate, but the
                # trace should make their unproven entry explicit.
                pass
        cmd = step["command"]
        started = time.time()
        syscall_log = root / f".witness-strace-{i}.log"
        wrapped = cmd
        if capture:
            if not shutil.which("strace"):
                raise SystemExit("--capture requires strace")
            wrapped = f"strace -f -qq -e trace=file -o {subprocess.list2cmdline([str(syscall_log)])} sh -c {subprocess.list2cmdline([cmd])}"
        proc = subprocess.run(wrapped, shell=True, cwd=root, text=True, capture_output=True,
                              env={**os.environ, "WITNESS_ROOT": str(root)})
        after = snapshot(root, declared)
        missing_outputs = [p for p in outputs if not (root / p).is_file()]
        changed_outputs = [p for p in outputs if before.get(p, {}).get("sha256") != after.get(p, {}).get("sha256")]
        ok = proc.returncode == 0 and not missing_inputs and not missing_outputs
        record = {
            "index": i, "name": name, "command": cmd, "inputs": inputs, "outputs": outputs,
            "before": before, "after": after, "missing_inputs": missing_inputs,
            "missing_outputs": missing_outputs, "changed_outputs": changed_outputs,
            "returncode": proc.returncode, "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:], "duration_ms": round((time.time() - started) * 1000, 1),
            "ok": ok,
        }
        if capture:
            observed = captured_paths(syscall_log, root)
            declared_set = set(declared)
            record["observed_paths"] = observed
            record["undeclared_in_root"] = sorted(set(observed["read"] + observed["write"]) - declared_set)
            syscall_log.unlink(missing_ok=True)
        trace["steps"].append(record)
        if ok:
            prior_outputs.update(outputs)
        else:
            trace["status"] = "failed"
            trace["first_broken_hinge"] = {"step": i, "name": name,
                                            "reasons": (["command_failed"] if proc.returncode else [])
                                                       + (["missing_input"] if missing_inputs else [])
                                                       + (["missing_output"] if missing_outputs else [])}
            break
    trace["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    out_path.write_text(json.dumps(trace, indent=2) + "\n")
    print(json.dumps({"status": trace["status"], "trace": str(out_path),
                      "first_broken_hinge": trace.get("first_broken_hinge")}))
    return 0 if trace["status"] == "passed" else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--out", type=Path, default=Path("witness.json"))
    ap.add_argument("--capture", action="store_true", help="capture in-root file syscalls with strace")
    args = ap.parse_args()
    return run(args.manifest.resolve(), args.out.resolve(), capture=args.capture)

if __name__ == "__main__":
    raise SystemExit(main())
