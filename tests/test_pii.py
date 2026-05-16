from app.pii.presidio_custom import scan_pii

def test_pak_phone():
    result = scan_pii("Call me at 0312-3456789")
    assert result["has_pii"] == True
    assert "PAK_PHONE" in result["pii_types"]
    print("PAK_PHONE test passed")

def test_cnic():
    result = scan_pii("My CNIC is 35202-1234567-9")
    assert result["has_pii"] == True
    assert "PAK_CNIC" in result["pii_types"]
    print("PAK_CNIC test passed")

def test_api_key():
    result = scan_pii(
        "My key is sk-abcdefghijklmnopqrstu123"
    )
    assert result["has_pii"] == True
    assert "API_KEY" in result["pii_types"]
    print("API_KEY test passed")

def test_safe():
    result = scan_pii("What is artificial intelligence?")
    assert result["has_pii"] == False
    print("Safe message test passed")

if __name__ == "__main__":
    test_pak_phone()
    test_cnic()
    test_api_key()
    test_safe()
    print("All PII tests passed!")