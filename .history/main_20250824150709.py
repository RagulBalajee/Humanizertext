from humanizer import humanize_text

if __name__ == "__main__":
    ai_text = (
        "In the modern digital economy, artificial intelligence serves as a critical driver of efficiency, "
        "enabling organizations to process vast datasets, optimize operations, and unlock innovative solutions "
        "that redefine industry standards."
    )

    humanized = humanize_text(ai_text)

    print("🤖 AI-Generated Text:\n")
    print(ai_text)
    print("\n✨ Humanized Text:\n")
    print(humanized)
