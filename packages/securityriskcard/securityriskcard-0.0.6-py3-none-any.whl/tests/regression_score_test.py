from securityriskcard import calculate_score, convert_to_risk

from . import load_test_data


# This check uses original scorecard result to validate that our score
# calculation function is valid and behaves as expected.
def test_regression_score_formula_on_raw_data():
    input_data, _ = load_test_data("klocc")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert 10 - input_data["score"] == convert_to_risk(input_data, ignore_cii_badge=False)["score"]

    input_data, _ = load_test_data("telethon")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert 10 - input_data["score"] == convert_to_risk(input_data, ignore_cii_badge=False)["score"]

    input_data, _ = load_test_data("ansible")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert 10 - input_data["score"] == convert_to_risk(input_data, ignore_cii_badge=False)["score"]

    input_data, _ = load_test_data("autogpt")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert 10 - input_data["score"] == convert_to_risk(input_data, ignore_cii_badge=False)["score"]


# This check uses previously generated and manually reviewed output of the
# package to verify that we didn't have a regression for a default expected
# behavior.
def test_regression_score_formula_processed_data():
    _, result_data = load_test_data("ansible")
    assert result_data["score"] == calculate_score(result_data["checks"])

    _, _ = load_test_data("telethon")
    assert result_data["score"] == calculate_score(result_data["checks"])

    _, _ = load_test_data("ansible")
    assert result_data["score"] == calculate_score(result_data["checks"])

    _, _ = load_test_data("autogpt")
    assert result_data["score"] == calculate_score(result_data["checks"])
