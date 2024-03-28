from securityriskcard import convert_to_risk

from . import load_test_data


def test_regression_convert_to_risk_klocc():
    input_data, result_data = load_test_data("klocc")

    result = convert_to_risk(input_data)
    assert result == result_data


def test_regression_convert_to_risk_telethon():
    input_data, result_data = load_test_data("telethon")

    result = convert_to_risk(input_data)
    assert result == result_data


def test_regression_convert_to_risk_ansible():
    input_data, result_data = load_test_data("ansible")

    result = convert_to_risk(input_data)
    assert result == result_data


def test_regression_convert_to_risk_autogpt():
    input_data, result_data = load_test_data("autogpt")

    result = convert_to_risk(input_data)
    assert result == result_data
