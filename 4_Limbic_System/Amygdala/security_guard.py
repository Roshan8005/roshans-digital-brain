# Amygdala Safety Guard - Security & Threat Analyzer
# Location: Limbic System / Amygdala

import re

# Suspect system command keywords that could damage the host system
DANGEROUS_KEYWORDS = [
    r"\brmdir\b",
    r"\bdel\b",
    r"\bformat\b",
    r"\bshred\b",
    r"\bshutdown\b",
    r"\bpoweroff\b",
    r"\breboot\b",
    r"\brm -rf\b",
]

# Common prompt injection patterns
INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "ignore safety",
    "you are now a",
    "override safety",
    "bypass firewall",
]


def check_input(user_input):
    """
    Scans the user query for security violations, command injections, or malicious prompts.
    Returns: dict {"is_safe": bool, "threat_level": str, "reason": str}
    """
    clean_input = user_input.lower().strip()

    # Check 1: Dangerous OS commands
    for kw in DANGEROUS_KEYWORDS:
        if re.search(kw, clean_input):
            return {
                "is_safe": False,
                "threat_level": "CRITICAL",
                "reason": f"Dangerous command keyword detected: '{kw}'",
            }

    # Check 2: Prompt Injections
    for kw in INJECTION_KEYWORDS:
        if kw in clean_input:
            return {
                "is_safe": False,
                "threat_level": "HIGH",
                "reason": f"Suspected prompt injection pattern detected: '{kw}'",
            }

    # Check 3: Suspicious shell characters
    # Look for pipe, redirect, or command concatenation characters that might indicate exploit attempts
    shell_escapes = [";", "&&", "||", "|", ">", "<"]
    for char in shell_escapes:
        # Allow pipe inside search queries if not followed by commands,
        # but block typical chaining patterns like: "some_query && whoami"
        if char in clean_input:
            # Simple heuristic checking if chaining keywords like 'whoami', 'netstat', 'ipconfig' are present
            for cmd in ["whoami", "netstat", "ipconfig", "systeminfo", "dir "]:
                if cmd in clean_input:
                    return {
                        "is_safe": False,
                        "threat_level": "MEDIUM",
                        "reason": f"Potential command chaining pattern: '{char} {cmd}'",
                    }

    return {
        "is_safe": True,
        "threat_level": "NONE",
        "reason": "Input scanned. No threats detected.",
    }
