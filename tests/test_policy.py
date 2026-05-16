from app.policy.policy_engine import make_decision

def test_block():
    result = make_decision(
        rule_score=2,
        semantic_score=0.9,
        pii_types=[],
        has_pii=False
    )
    assert result["decision"] == "BLOCK"
    print("Block test passed")

def test_mask():
    result = make_decision(
        rule_score=0,
        semantic_score=0.3,
        pii_types=["PAK_PHONE"],
        has_pii=True
    )
    assert result["decision"] == "MASK"
    print("Mask test passed")

def test_allow():
    result = make_decision(
        rule_score=0,
        semantic_score=0.1,
        pii_types=[],
        has_pii=False
    )
    assert result["decision"] == "ALLOW"
    print("Allow test passed")

if __name__ == "__main__":
    test_block()
    test_mask()
    test_allow()
    print("All policy tests passed!")