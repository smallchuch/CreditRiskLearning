"""Checks on finished outputs. Run: python -m pytest tests"""
import pytest
from er_toolkit import contracts, project as proj

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("name", sorted(proj.manifest(ROOT)))
def test_contract_tables_valid(name):
    df, is_demo = proj.read_table(name, start=ROOT)
    assert not is_demo
    if name in contracts.TABLES:
        contracts.validate(df, name)
    assert len(df) > 0
