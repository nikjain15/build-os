#!/usr/bin/env python3
"""Validate docs/data/scorecards.json before commit (SKILL.md §12 rules).

Checks: schema keys, the nine-pillar set, grade values, the overall formula
(round(mean(non-null pillars) * 10)), and non-empty question ids/labels.
Exit 0 = clean; exit 1 = findings printed.
"""
import json, sys
from pathlib import Path

PILLARS = [
    "Product Judgment", "System Design", "Evaluation", "Reliability & Ownership",
    "Safety", "Economics", "Communication", "UX/UI & Interaction",
    "Collaboration & Stakeholders",
]
REQUIRED = ["project", "title", "date", "type", "overall", "pillars", "artifacts",
            "questions", "notes", "weakest_pillar", "next_focus", "loop_ran",
            "projects_since_resource_refresh"]
GRADES = {"weak", "good", "great"}

path = Path(__file__).resolve().parent.parent / "docs/data/scorecards.json"
data = json.loads(path.read_text())
errors = []

for p in data.get("projects", []):
    name = p.get("project", "<unnamed>")
    for k in REQUIRED:
        if k not in p:
            errors.append(f"{name}: missing field '{k}'")
    pillars = p.get("pillars", {})
    if set(pillars) != set(PILLARS):
        errors.append(f"{name}: pillar set drift: {sorted(set(pillars) ^ set(PILLARS))}")
    vals = [v for v in pillars.values() if v is not None]
    if vals:
        expect = round(sum(vals) / len(vals) * 10)
        if p.get("overall") != expect:
            errors.append(f"{name}: overall={p.get('overall')} but formula gives {expect}")
    for q in p.get("questions", []):
        if not q.get("id") or not q.get("label"):
            errors.append(f"{name}: question missing id/label: {q}")
        if q.get("grade") not in GRADES:
            errors.append(f"{name}: question {q.get('id')}: bad grade '{q.get('grade')}'")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK — {len(data.get('projects', []))} project(s) valid.")
