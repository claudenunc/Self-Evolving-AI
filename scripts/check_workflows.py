"""Repeat the earlier deterministic fixture checks; no model trials are run."""
import importlib.util
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
fixtures = repo / "examples/workflow-checks"
spec = importlib.util.spec_from_file_location(
    "checked_clean_rows", fixtures / "verified-execution/clean_rows.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
zero = {"id": 0, "value": "first zero"}
first = {"id": 7, "value": "first seven"}
last = {"id": 2, "value": "two"}
source = [first, zero, {"id": 7, "value": "duplicate"}, {},
          {"id": None}, {"id": ""}, last, {"id": 0}]
result = module.clean_rows(source)
assert result == [first, zero, last], result
assert result[0] is first and result[1] is zero and result[2] is last
assert module.clean_rows([]) == []
assert module.clean_rows(iter(source)) == [first, zero, last]
assert len(source) == 8
assert module.clean_rows([{"id": "b"}, {"id": "a"}, {"id": "b"}]) == [
    {"id": "b"}, {"id": "a"}]
print("Execution fixture: 6 assertions passed.")

root = fixtures / "research-to-implementation"
brief = (root / "PROJECT_BRIEF.md").read_text()
decisions = (root / "DECISIONS.md").read_text()
ledger = (root / "IMPLEMENTATION_LEDGER.md").read_text()
assert "$250" in brief and "Android" in brief
assert "$250" in decisions and "Android" in decisions
assert "rejected" in ledger.lower()
settings_row = next(line for line in ledger.splitlines()
                    if line.startswith("| 6. Set global custom instructions |"))
assert "| rejected |" in settings_row
assert "subscription" in decisions.lower()
print("Implementation fixture: 5 assertions passed; no live settings changed.")
