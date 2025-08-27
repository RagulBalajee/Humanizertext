from humanizer import Humanizer

def main():
    humanizer = Humanizer()

    # Ask for user input
    input_text = input("✍️ Enter your text: ").strip()

    # AI text (raw input)
    print("\n🤖 AI-Generated Text:\n")
    print(input_text)

    # Humanized text
    humanized_text = humanizer.humanize(input_text)
    print("\n✨ Humanized Text:\n")
    print(humanized_text)

if __name__ == "__main__":
    main()
