#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).parent
source = (root / "source.md").read_text()
title = next((line.lstrip("# ").strip() for line in source.splitlines() if line.startswith("#")), "untitled")
paragraphs = [p.strip().replace("\n", " ") for p in source.split("\n\n") if p.strip()]
report = "# Witnessed report\n\n" + f"Source title: {title}\n\n"
report += f"Paragraphs: {len(paragraphs)}\n\n"
report += "\n\n".join(f"{i}. {p}" for i, p in enumerate(paragraphs, 1)) + "\n"
(root / "report.md").write_text(report)
print(f"extracted {len(paragraphs)} paragraphs from {title!r}")
