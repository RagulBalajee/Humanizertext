import random

def humanize_text(ai_text: str) -> str:
    """
    Humanizes AI-generated text by rephrasing it using
    synonyms, varying sentence structures, and slight randomness.
    """

    replacements = {
        "modern": ["contemporary", "current", "present-day"],
        "digital economy": ["tech-driven industry", "online economy", "technology-powered sector"],
        "artificial intelligence": ["AI", "machine intelligence", "smart technology"],
        "critical driver": ["key force", "fundamental engine", "major factor"],
        "efficiency": ["productivity", "effectiveness", "performance"],
        "process vast datasets": ["analyze massive data collections", "handle large-scale information", "manage extensive datasets"],
        "optimize operations": ["improve workflows", "streamline processes", "enhance systems"],
        "unlock innovative solutions": ["discover creative strategies", "enable groundbreaking ideas", "foster novel approaches"],
        "redefine industry standards": ["reshape business norms", "set new benchmarks", "transform sector practices"]
    }

    humanized = ai_text

    for key, values in replacements.items():
        if key in humanized:
            humanized = humanized.replace(key, random.choice(values))

    # Add slight randomness at the end for uniqueness
    extras = [
        " This shift continues to influence businesses worldwide.",
        " As a result, industries are constantly adapting to new challenges.",
        " Ultimately, it changes how organizations operate and grow.",
        " This trend highlights the role of innovation in shaping the future."
    ]

    if random.random() > 0.5:  # 50% chance to add an extra ending
        humanized += random.choice(extras)

    return humanized.strip()
