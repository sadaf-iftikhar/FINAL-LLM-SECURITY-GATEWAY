import yaml
import os

config_path = os.path.join(
    os.path.dirname(__file__),
    "../../config/gateway_config.yaml"
)
with open(config_path) as f:
    config = yaml.safe_load(f)

thresholds = config["thresholds"]
pii_weights = config["pii_weights"]

def calculate_final_risk(
    rule_score: float,
    semantic_score: float,
    pii_types: list
) -> float:

    base_risk = max(
        min(rule_score / 3.0, 1.0),
        semantic_score
    )

    pii_weight = 0.0
    high_risk_pii = [
        "PAK_CNIC", "API_KEY",
        "CREDIT_CARD", "PAK_PHONE"
    ]
    medium_risk_pii = [
        "EMAIL_ADDRESS", "INTERNAL_ID"
    ]

    for pii in pii_types:
        if pii in high_risk_pii:
            pii_weight += pii_weights["high"]
        elif pii in medium_risk_pii:
            pii_weight += pii_weights["medium"]
        else:
            pii_weight += pii_weights["low"]

    final_risk = min(base_risk + pii_weight, 1.0)
    return round(final_risk, 3)
def make_decision(
    rule_score: float,
    semantic_score: float,
    pii_types: list,
    has_pii: bool
) -> dict:

    final_risk = calculate_final_risk(
        rule_score, semantic_score, pii_types
    )

    reason_codes = []

    if rule_score >= thresholds["rule_block"]:
        reason_codes.append("RULE_INJECTION")

    if semantic_score >= thresholds["semantic_block"]:
        reason_codes.append("SEMANTIC_INJECTION")

    if has_pii:
        reason_codes.append("PII_DETECTED")

    # Pure PII with no attack signal = always MASK not BLOCK
    is_pure_pii = (
        has_pii and
        rule_score < thresholds["rule_block"] and
        semantic_score < thresholds["semantic_block"]
    )

    if is_pure_pii:
        decision = "MASK"

    # Rule score 2+ always blocks
    elif rule_score >= thresholds["rule_block"]:
        decision = "BLOCK"

    # High semantic score blocks
    elif semantic_score >= thresholds["semantic_block"]:
        decision = "BLOCK"

    # High final risk blocks
    elif final_risk >= thresholds["final_risk_block"]:
        decision = "BLOCK"

    # PII found = mask
    elif has_pii:
        decision = "MASK"

    # Medium risk = mask
    elif final_risk >= thresholds["final_risk_mask"]:
        decision = "MASK"

    # Everything safe = allow
    else:
        decision = "ALLOW"

    return {
        "final_risk": final_risk,
        "decision": decision,
        "reason_codes": reason_codes
    }