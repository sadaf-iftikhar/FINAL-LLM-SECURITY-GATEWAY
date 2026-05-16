from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    Pattern
)
from presidio_anonymizer import AnonymizerEngine
import yaml
import os

config_path = os.path.join(
    os.path.dirname(__file__),
    "../../config/gateway_config.yaml"
)
with open(config_path) as f:
    config = yaml.safe_load(f)

MIN_CONFIDENCE = config["thresholds"]["min_confidence"]

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

pak_phone = PatternRecognizer(
    supported_entity="PAK_PHONE",
    patterns=[
        Pattern("PAK_LOCAL",
                r"0[3][0-9]{2}[-\s]?[0-9]{7}", 0.85),
        Pattern("PAK_INTL",
                r"\+92[3][0-9]{9}", 0.90),
    ],
    context=["call", "contact", "number",
             "phone", "whatsapp", "mobile"]
)

api_key = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[
        Pattern("SK_KEY",
                r"sk-[a-zA-Z0-9]{20,}", 0.90),
        Pattern("BEARER",
                r"Bearer\s[a-zA-Z0-9\-._~+/]+=*", 0.88),
    ],
    context=["key", "token", "secret",
             "authorization", "api", "bearer"]
)

cnic = PatternRecognizer(
    supported_entity="PAK_CNIC",
    patterns=[
        Pattern("CNIC",
                r"[0-9]{5}-[0-9]{7}-[0-9]{1}", 0.95),
    ],
    context=["cnic", "identity", "id card",
             "national", "nadra"]
)

internal_id = PatternRecognizer(
    supported_entity="INTERNAL_ID",
    patterns=[
        Pattern("STU_ID",
                r"[A-Z]{2}[0-9]{2}-[A-Z]{3}-[0-9]{3}", 0.85),
        Pattern("EMP_ID",
                r"EMP-[0-9]{4,6}", 0.80),
    ],
    context=["student", "employee", "id",
             "registration", "roll", "number"]
)

for recognizer in [pak_phone, api_key, cnic, internal_id]:
    analyzer.registry.add_recognizer(recognizer)

def scan_pii(text: str) -> dict:
    raw = analyzer.analyze(text=text, language="en")
    filtered = [r for r in raw if r.score >= MIN_CONFIDENCE]

    if not filtered:
        return {
            "has_pii": False,
            "masked_text": text,
            "pii_types": [],
            "pii_entities": [],
            "composite_risk": "LOW"
        }

    pii_types = list(set([r.entity_type for r in filtered]))
    pii_entities = [
        {
            "type": r.entity_type,
            "score": round(r.score, 2),
            "start": r.start,
            "end": r.end
        }
        for r in filtered
    ]

    composite_risk = (
        "HIGH" if len(pii_types) >= 2 else "MEDIUM"
    )

    masked = anonymizer.anonymize(
        text=text,
        analyzer_results=filtered
    )

    return {
        "has_pii": True,
        "masked_text": masked.text,
        "pii_types": pii_types,
        "pii_entities": pii_entities,
        "composite_risk": composite_risk
    }