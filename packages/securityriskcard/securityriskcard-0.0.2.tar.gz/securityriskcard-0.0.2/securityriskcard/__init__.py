import re

MIN_SCORE = 0
MAX_SCORE = 10
RE_REASON = re.compile(r"(-- score normalized to) \d+")

CHECK_TO_RISK = {
    "Binary-Artifacts": "High",
    "Branch-Protection": "High",
    "CI-Tests": "Low",
    "CII-Best-Practices": "Low",
    "Code-Review": "High",
    "Contributors": "Low",
    "Dangerous-Workflow": "Critical",
    "Dependency-Update-Tool": "High",
    "Fuzzing": "Medium",
    "License": "Low",
    "Maintained": "High",
    "Pinned-Dependencies": "Medium",
    "Packaging": "Medium",
    "SAST": "Medium",
    "Security-Policy": "Medium",
    "Signed-Releases": "High",
    "Token-Permissions": "High",
    "Vulnerabilities": "High",
    "Webhooks": "Critical",
}
RISK_TO_WEIGHT = {"Critical": 10, "High": 7.5, "Medium": 5, "Low": 2.5}


def calculate_score(checks: list):
    total, score = 0, 0
    for check in checks:
        # Ignore 'inconclusive' score (-1).
        if check["score"] < MIN_SCORE:
            continue

        weight = RISK_TO_WEIGHT[CHECK_TO_RISK[check["name"]]]
        total += weight
        score += weight * check["score"]
    return round(score / total, 1)


def _convert_check(check: dict):
    if check["score"] not in (None, -1):
        check["score"] = round(MAX_SCORE - check["score"], 1)
        check["reason"] = RE_REASON.sub(rf"\1 {check['score']}", check["reason"])
    return check


def _filter_check(check: dict):
    # @TODO: Here we are ignoring the gimmic (badge) check, so we don't need to bother displaying
    #        it nor will we want to confuse LLM at any point to count this as a meaningful risk.
    #        However, with this change the total risk might not properly add up to 10, which is
    #        very unlikely to happen anyways so we are not as affected right now, but fixing it
    #        long term is probably a good idea.                               - andrew, March 26 2024
    return check["name"].lower() != "cii-best-practices"


def convert_to_risk(data: dict):
    data["checks"] = [_convert_check(check) for check in data["checks"] if _filter_check(check)]
    data["score"] = calculate_score(data["checks"])
    return data
