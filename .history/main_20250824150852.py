from humanizer import humanize_text

def main():
    print("=== AI → Humanized Text Converter ===")
    user_input = input("Enter AI-generated text:\n> ").strip()

    if not user_input:
        print("⚠️ No input provided. Please enter some text.")
        return

    print("\n🤖 AI-Generated Text:\n")
    print(user_input)

    humanized = humanize_text(user_input)

    print("\n✨ Humanized Text:\n")
    print(humanized)

if __name__ == "__main__":
    main()
