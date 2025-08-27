from humanizer import humanize_paragraph

if __name__ == "__main__":
    ai_text = input("🤖 Enter your AI-generated text (single paragraph):\n\n>> ")
    human_text = humanize_paragraph(ai_text)
    
    print("\n✨ Humanized Text :\n")
    print(human_text)
