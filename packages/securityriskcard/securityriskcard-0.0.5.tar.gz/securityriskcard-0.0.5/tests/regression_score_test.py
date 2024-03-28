from securityriskcard import calculate_score, convert_to_risk

from . import load_test_data


def test_regression_score_formula():
    input_data, result_data = load_test_data("klocc")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert result_data["score"] == calculate_score(result_data["checks"])

    input_data, result_data = load_test_data("telethon")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert result_data["score"] == calculate_score(result_data["checks"])

    input_data, result_data = load_test_data("ansible")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert result_data["score"] == calculate_score(result_data["checks"])

    input_data, result_data = load_test_data("autogpt")
    assert input_data["score"] == calculate_score(input_data["checks"])
    assert result_data["score"] == calculate_score(result_data["checks"])
