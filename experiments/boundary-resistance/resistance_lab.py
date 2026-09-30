#!/usr/bin/env python3
"""Adversarial local workflow probe: endpoint survival versus route legitimacy."""
from __future__ import annotations
import argparse, hashlib, json, os, shlex, shutil, subprocess, tempfile, time
from pathlib import Path


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except PermissionError:
        return "<unreadable>"


def make_fixture(root: Path) -> None:
    (root / "source.txt").write_text("approved: ORBIT\nversion: 7\n")
    (root / "extract.py").write_text(
        "from pathlib import Path\n"
        "src = Path('source.txt').read_text()\n"
        "token = next(x.split(':',1)[1].strip() for x in src.splitlines() if x.startswith('approved:'))\n"
        "Path('answer.txt').write_text(f'answer: {token}\\n')\n"
    )
    (root / "validate.py").write_text(
        "from pathlib import Path\n"
        "answer = Path('answer.txt').read_text().strip()\n"
        "print(answer)\n"
        "raise SystemExit(0 if answer == 'answer: ORBIT' else 4)\n"
    )
    (root / "shortcut.txt").write_text("ORBIT\n")


def run_cmd(root: Path, command: str, log_name: str) -> dict:
    log = root / log_name
    wrapped = f"strace -f -qq -e trace=file -o {shlex.quote(str(log))} sh -c {shlex.quote(command)}"
    p = subprocess.run(wrapped, shell=True, cwd=root, text=True, capture_output=True)
    return {"command": command, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "trace": str(log)}


def observed_in_root(log: Path, root: Path) -> list[str]:
    if not log.exists():
        return []
    found = set()
    for line in log.read_text(errors="replace").splitlines():
        # strace quotes paths in the first syscall argument; this is intentionally conservative.
        for raw in line.split('"')[1::2]:
            p = Path(raw)
            if not p.is_absolute():
                p = root / p
            try:
                rel = p.resolve().relative_to(root.resolve())
            except (ValueError, OSError):
                continue
            if p.is_file():
                found.add(str(rel))
    return sorted(found)


def scenario(name: str, mutate) -> dict:
    with tempfile.TemporaryDirectory(prefix="boundary-resistance-") as td:
        root = Path(td)
        make_fixture(root)
        original_source = digest(root / "source.txt")
        mutate(root)
        before = {p: digest(root / p) for p in ["source.txt", "answer.txt", "shortcut.txt"]}
        extract = run_cmd(root, "python3 extract.py", "extract.strace")
        extract_seen = observed_in_root(Path(extract["trace"]), root)
        answer_after_extract = digest(root / "answer.txt")
        validate = run_cmd(root, "python3 validate.py", "validate.strace")
        validate_seen = observed_in_root(Path(validate["trace"]), root)
        expected_declared = {"source.txt", "extract.py", "answer.txt", "validate.py"}
        undeclared = sorted((set(extract_seen + validate_seen) - expected_declared))
        endpoint_passed = validate["returncode"] == 0
        route_flags = []
        if extract["returncode"] != 0:
            route_flags.append("extract_failed")
        if undeclared:
            route_flags.append("undeclared_dependency")
        if original_source != digest(root / "source.txt") and answer_after_extract == before["answer.txt"]:
            route_flags.append("stale_answer")
        if name == "permission_denied" and extract["returncode"] != 0:
            route_flags.append("source_unreadable")
        route_valid = not route_flags and endpoint_passed
        return {
            "scenario": name,
            "endpoint_passed": endpoint_passed,
            "route_valid": route_valid,
            "route_flags": route_flags,
            "extract_returncode": extract["returncode"],
            "validate_returncode": validate["returncode"],
            "observed_paths": sorted(set(extract_seen + validate_seen)),
            "undeclared_paths": undeclared,
            "answer_sha256": digest(root / "answer.txt"),
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("results.json"))
    ap.add_argument("--markdown", type=Path, default=Path("report.md"))
    args = ap.parse_args()
    cases = [
        ("normal", lambda root: None),
        ("shortcut_dependency", lambda root: (root / "extract.py").write_text(
            "from pathlib import Path\n"
            "token = Path('shortcut.txt').read_text().strip()\n"
            "Path('answer.txt').write_text(f'answer: {token}\\n')\n")),
        ("stale_endpoint", lambda root: ((root / "answer.txt").write_text("answer: ORBIT\n"),
            (root / "source.txt").write_text("approved: COMET\nversion: 8\n"),
            (root / "extract.py").write_text("from pathlib import Path\nPath('answer.txt').touch()\n"))),
        ("permission_denied", lambda root: ((root / "answer.txt").write_text("answer: ORBIT\n"),
            (root / "source.txt").chmod(0),
            (root / "extract.py").write_text("from pathlib import Path\nPath('source.txt').read_text()\nPath('answer.txt').write_text('answer: ORBIT\\n')\n"))),
    ]
    results = [scenario(name, mutate) for name, mutate in cases]
    args.out.write_text(json.dumps({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "results": results}, indent=2) + "\n")
    lines = ["# Boundary Resistance Lab", "", "Endpoint correctness is deliberately separated from route legitimacy.", ""]
    for r in results:
        lines += [f"## {r['scenario']}", f"- endpoint passed: `{r['endpoint_passed']}`", f"- route valid: `{r['route_valid']}`", f"- flags: `{', '.join(r['route_flags']) or 'none'}`", f"- undeclared paths: `{', '.join(r['undeclared_paths']) or 'none'}`", ""]
    args.markdown.write_text("\n".join(lines))
    print(json.dumps({"scenarios": len(results), "endpoint_passes": sum(r["endpoint_passed"] for r in results), "route_passes": sum(r["route_valid"] for r in results), "out": str(args.out)}))


if __name__ == "__main__":
    raise SystemExit(main())
