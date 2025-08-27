from humanizer import humanize_paragraph

if __name__ == "__main__":
    print("\n🤖 Enter your AI-generated text (single paragraph):\n")
    ai_text = input(">> ")

    humanized_text = humanize_paragraph(ai_text)

    print("\n✨ Humanized Text (~50-55% similar):\n")
    print(humanized_text)
