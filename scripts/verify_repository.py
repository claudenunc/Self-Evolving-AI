"""Check the export manifest, links, readable archives, and common secret patterns.

This is a bounded integrity/privacy check, not a complete security audit.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "verification/export_manifest.json"
RECEIPTS = {"verification/export_local_validation.json",
            "verification/remote_verification.json"}
SECRET_PATTERNS = {
    "github-token": re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "openai-key": re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}\b"),
    "aws-access-key": re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
TEXT_TYPES = {".md", ".py", ".json", ".jsonl", ".yaml", ".yml", ".cast", ".svg"}


def payload_files():
    return sorted(p for p in ROOT.rglob("*") if p.is_file()
                  and not any(part in {".git", "__pycache__", ".venv", "node_modules"}
                              for part in p.relative_to(ROOT).parts)
                  and p.suffix not in {".pyc", ".pyo"}
                  and p != MANIFEST and p.relative_to(ROOT).as_posix() not in RECEIPTS)


def describe(path):
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": hashlib.sha1(
                f"blob {len(data)}\0".encode() + data).hexdigest()}


def verify():
    expected = json.loads(MANIFEST.read_text())["files"]
    actual = [describe(p) for p in payload_files()]
    problems = []
    if actual != expected:
        expected_by_path = {x["path"]: x for x in expected}
        actual_by_path = {x["path"]: x for x in actual}
        for path in sorted(set(expected_by_path) | set(actual_by_path)):
            if expected_by_path.get(path) != actual_by_path.get(path):
                problems.append({"path": path, "issue": "manifest mismatch"})
    links = archives = 0
    for p in payload_files():
        data = p.read_bytes()
        if p.suffix in TEXT_TYPES:
            for name, pattern in SECRET_PATTERNS.items():
                if pattern.search(data):
                    problems.append({"path": p.relative_to(ROOT).as_posix(),
                                     "issue": "possible secret", "pattern": name})
        if p.suffix == ".md":
            # The project links use simple Markdown targets; skip remote URLs/anchors.
            for target in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", data.decode()):
                if re.match(r"(?:[A-Za-z][A-Za-z0-9+.-]*:|#)", target):
                    continue
                local = target.split("#", 1)[0]
                if local:
                    links += 1
                    if not (p.parent / local).exists():
                        problems.append({"path": p.relative_to(ROOT).as_posix(),
                                         "issue": "broken local link", "target": local})
        if p.suffix == ".zip":
            with zipfile.ZipFile(p) as archive:
                failed = archive.testzip()
                if failed:
                    problems.append({"path": p.relative_to(ROOT).as_posix(),
                                     "issue": "ZIP CRC failure"})
            archives += 1
        if p.suffix == ".pdf" and not data.startswith(b"%PDF-"):
            problems.append({"path": p.relative_to(ROOT).as_posix(), "issue": "invalid PDF header"})
    return {"scope": "Local export integrity, links, ZIP CRC, PDF headers, common live-secret patterns",
            "passed": not problems, "payload_files": len(actual),
            "payload_bytes": sum(x["bytes"] for x in actual),
            "local_links_checked": links, "zip_archives_checked": archives,
            "secret_scan": "Limited pattern scan; screenshots were reviewed separately",
            "model_trials_run": 0, "problems": problems}


def verify_git_ref(ref):
    """Compare an already-fetched Git commit against every tracked local file."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_/.-]*", ref):
        raise ValueError("Use a normal fetched Git ref or commit SHA")
    commit = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "--verify", ref + "^{commit}"],
        text=True).strip()
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-tree", "-rz", "-l", commit])
    observed = {}
    for record in raw.decode().split("\0"):
        if not record:
            continue
        metadata, name = record.split("\t", 1)
        mode, kind, sha, size = metadata.split()
        if kind != "blob":
            raise ValueError("Submodules require a separate verification procedure")
        observed[name] = {"sha": sha, "bytes": int(size)}
    names = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "-z"]).decode().split("\0")
    expected = {name: describe(ROOT / name) for name in names if name}
    mismatches = [name for name in sorted(set(expected) | set(observed))
                  if name not in expected or name not in observed
                  or expected[name]["git_blob_sha1"] != observed[name]["sha"]
                  or expected[name]["bytes"] != observed[name]["bytes"]]
    return {"passed": not mismatches, "ref": ref, "commit_sha": commit,
            "files_checked": len(expected), "mismatches": mismatches}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true",
                        help="Refresh only after intentionally reviewing payload changes")
    parser.add_argument("--report", type=Path, help="Optional JSON result path")
    parser.add_argument("--remote-ref", help="Compare an already-fetched Git ref with every tracked local file")
    args = parser.parse_args()
    if args.write_manifest:
        MANIFEST.parent.mkdir(exist_ok=True)
        MANIFEST.write_text(json.dumps({"date": "2026-10-03",
            "repository": "claudenunc/Self-Evolving-AI",
            "scope": "Project payload; manifest and verification receipts excluded to avoid self-reference",
            "files": [describe(p) for p in payload_files()]}, indent=2) + "\n")
    result = verify()
    if args.remote_ref:
        result["remote"] = verify_git_ref(args.remote_ref)
        result["passed"] = result["passed"] and result["remote"]["passed"]
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)
