#!/usr/bin/env python
# coding: utf-8

"""Test SOVAD gorules."""


import pytest
import zen


__author__ = "Yec'han Laizet"
__version__ = "0.1.0"


# Tests created according to Table 3 of the article
EXPECTED_EVALS = {
    "Benign": [
        {"BA": 1},
        {"BS": 2},
        {"BS": 3},
    ],
    "Likely benign": [
        {"BS": 1, "BP": 1, "PP": 1},
        {"BS": 1, "BP": 1},
        {"BP": 2},
        {"BP": 3},
    ],
    "Uncertain significance": [
        {"BA": 1, "PA": 1},
        {"BS": 2, "PS": 2},
        {"PS": 1},
        {"BS": 1},
    ],
    "Likely pathogenic": [
        {"PVS": 1, "PM": 1},
        {"PS": 1, "PM": 1},
        {"PS": 1, "PM": 2},
        {"PS": 1, "PP": 2},
        {"PS": 1, "PP": 3},
        {"PM": 3},
        {"PM": 4},
        {"PM": 2, "PP": 2},
        {"PM": 2, "PP": 3},
        {"PM": 1, "PP": 4},
        {"PM": 1, "PP": 5},
    ],
    "Pathogenic": [
        {"PA": 1},
        {"PA": 2},
        {"PVS": 1, "PS": 1},
        {"PVS": 1, "PS": 2},
        {"PVS": 1, "PM": 1, "PP": 1},
        {"PVS": 1, "PM": 0, "PP": 2},
        {"PVS": 1, "PM": 2, "PP": 0},
        {"PVS": 1, "PM": 2, "PP": 2},
        {"PS": 2},
        {"PS": 3},
        {"PS": 1, "PM": 3},
        {"PS": 1, "PM": 4},
        {"PS": 1, "PM": 2, "PP": 2},
        {"PS": 1, "PM": 2, "PP": 3},
        {"PS": 1, "PM": 1, "PP": 4},
        {"PS": 1, "PM": 1, "PP": 5},
    ],
}


def iter_evals(evals: dict) -> list:
    """Return a list of (counts, pathogenicity) from dict of expected evals.

    Args:
        evals (dict): pathogenicity for several counts

    Returns:
        list: (counts, pathogenicity)
    """
    return [(counts, patho) for patho, conditions in evals.items() for counts in conditions]


def test_iter_eval():
    """Test data formatting function."""
    eval_in = {
        "Benign": [
            {"BA": 1},
        ],
        "Likely benign": [
            {"BS": 1, "BP": 1},
            {"BP": 2},
        ],
    }
    eval_out = [
        ({"BA": 1}, "Benign"),
        ({"BS": 1, "BP": 1}, "Likely benign"),
        ({"BP": 2}, "Likely benign"),
    ]
    assert iter_evals(eval_in) == eval_out


@pytest.fixture(scope="module")
def decision_engine():
    """Creates a decision engine to perform inference testing."""
    engine = zen.ZenEngine()
    with open("sovad_gorules.json") as f:
        content = f.read()
    decision = engine.create_decision(content)
    return decision


@pytest.mark.parametrize("expected_counts_patho", iter_evals(EXPECTED_EVALS))
def test_sovad_rules(expected_counts_patho, decision_engine):
    """Test inference of pathogenicity with the gorules."""
    counts, expected_patho = expected_counts_patho
    result = decision_engine.evaluate(counts)
    evaluated_patho = result["result"]["pathogenicity"]
    assert evaluated_patho == expected_patho
