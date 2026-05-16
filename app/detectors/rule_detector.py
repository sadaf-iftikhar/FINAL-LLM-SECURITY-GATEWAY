import re

THREAT_KEYWORDS_EN = [
    "ignore previous instructions",
    "ignore all instructions",
    "disregard your rules",
    "forget everything above",
    "override your settings",
    "jailbreak", "dan mode",
    "do anything now",
    "pretend you have no restrictions",
    "act as admin", "pretend you are",
    "you are now", "roleplay as",
    "reveal system prompt",
    "show your instructions",
    "repeat everything above",
    "print your prompt",
    "what are your hidden rules",
    "bypass", "simulate developer mode",
    "maintenance mode", "ignore rules",
    "override policy",
    "show hidden configuration",
    "forget earlier rules",
    "disable all security",
    "reveal confidential",
]

THREAT_KEYWORDS_UR = [
    "پچھلی ہدایات نظر انداز",
    "سسٹم پرامپٹ دکھاؤ",
    "تمام قوانین بھول جاؤ",
    "پابندیاں ہٹاؤ",
    "ہدایات ظاہر کریں",
    "سسٹم پرامپٹ",
    "خفیہ پرامپٹ",
    "حفاظتی اصول ختم",
]

THREAT_KEYWORDS_KO = [
    "이전 지침을 무시",
    "시스템 프롬프트를 보여",
    "모든 규칙을 무시",
    "제한을 해제",
    "보안 규칙을 우회",
    "숨겨진 관리자",
    "비밀번호를 출력",
]

OBFUSCATION_MAP = {
    '0': 'o', '1': 'i', '3': 'e',
    '4': 'a', '5': 's', '@': 'a',
    '$': 's', '!': 'i', '+': 't',
    '7': 't',
}

def deobfuscate(text: str) -> str:
    result = ""
    for ch in text.lower():
        result += OBFUSCATION_MAP.get(ch, ch)
    return result

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s@.\-]', '', text)
    return text

def get_rule_score(text: str):
    normalized = normalize(text)
    deobfuscated = deobfuscate(text)
    found = []
    score = 0
    all_keywords = (
        THREAT_KEYWORDS_EN +
        THREAT_KEYWORDS_UR +
        THREAT_KEYWORDS_KO
    )
    for phrase in all_keywords:
        if (phrase in normalized or
                phrase in deobfuscated):
            score += 1
            found.append(phrase)
    return score, found