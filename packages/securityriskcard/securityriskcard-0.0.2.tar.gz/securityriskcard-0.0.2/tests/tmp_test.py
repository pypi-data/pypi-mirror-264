from securityriskcard import calculate_score, convert_to_risk

from . import load_test_data


def test_regression_score_formula():
    input_data, result_data = load_test_data("klocc")

    good_checks = list(filter(lambda o: o["score"] > -1, input_data["checks"]))
    good_checks_sum = sum(map(lambda o: o["score"], good_checks))
    good_checks_eval = round(good_checks_sum / len(good_checks), 1)
    print(f"Input score: {input_data['score']} == {good_checks_eval}")


if __name__ == "__main__":
    test_regression_score_formula()
