#!/usr/bin/env python3
"""verify_votes.py — deterministic adversarial verification (governance-kit).

The model never self-declares "verified". A finding only survives when an
independent panel of 3 voters returns >= 2 TRUE_POSITIVE votes.

Reads findings.json, votes.json, coverage.json from a run directory:
  - candidates in findings.json
  - rounds in votes.json (panel: true/false counts per candidate id)
  - coverage.json optional (coverage metadata)

Outputs verification.json with:
  - verified findings (confidence HIGH=3/3, MEDIUM=2/3)
  - refuted findings (REJECTED, reclassified severity)
  - unverified findings (no round or incomplete panel — never counts as verified)

Usage: python3 scripts/verify_votes.py <run_dir>
Exit codes: 0 = verdict computed, 1 = invalid input, 2 = could not run.
"""

import json
import sys
from pathlib import Path

PANEL_SIZE = 3
REQUIRED_QUORUM = 2


def load_json(path: Path):
    with open(path) as f:
        return json.load(f)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: verify_votes.py <run_dir>", file=sys.stderr)
        return 2

    run_dir = Path(sys.argv[1])
    findings_path = run_dir / "findings.json"
    votes_path = run_dir / "votes.json"

    if not findings_path.exists() or not votes_path.exists():
        print(f"verify_votes: missing findings.json or votes.json in {run_dir}", file=sys.stderr)
        return 2

    try:
        findings = load_json(findings_path)
        votes = load_json(votes_path)
    except json.JSONDecodeError as e:
        print(f"verify_votes: invalid JSON: {e}", file=sys.stderr)
        return 1

    candidates = findings.get("candidates", [])
    rounds = votes.get("rounds", {})

    verified, refuted, unverified = [], [], []

    for candidate in candidates:
        cid = candidate["id"]
        round_data = rounds.get(cid)
        if round_data is None:
            unverified.append({"id": cid, "reason": "no panel round — never evaluated"})
            continue

        panel = round_data.get("panel", {})
        n_true = panel.get("true", 0)
        n_false = panel.get("false", 0)
        n_total = n_true + n_false

        if n_total < PANEL_SIZE:
            unverified.append({"id": cid, "reason": f"incomplete panel: {n_total}/{PANEL_SIZE} votes"})
            continue

        kept = n_true >= REQUIRED_QUORUM
        confidence = "HIGH" if n_true == PANEL_SIZE else ("MEDIUM" if kept else "REJECTED")

        entry = {
            "id": cid,
            "severity": candidate.get("severity"),
            "confidence": confidence,
            "votes": {"true": n_true, "false": n_false},
        }
        if kept:
            verified.append(entry)
        else:
            entry["reclassified_severity"] = round_data.get("reclassified_severity", "FALSE_POSITIVE")
            refuted.append(entry)

    output = {
        "verification": {
            "verified": verified,
            "refuted": refuted,
            "unverified": unverified,
            "summary": {
                "candidates": len(candidates),
                "verified": len(verified),
                "refuted": len(refuted),
                "unverified": len(unverified),
            },
        }
    }

    out_path = run_dir / "verification.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"verify_votes: {len(verified)} verified, {len(refuted)} refuted, {len(unverified)} unverified → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
