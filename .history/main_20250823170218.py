from humanizer import humanize_text

def main():
    print("🤖 AI to Human Content Converter")
    print("Type 'exit' anytime to quit.\n")

    while True:
        user_input = input("Enter AI-generated text:\n> ")
        if user_input.lower().strip() == "exit":
            print("\n👋 Goodbye! Keep writing human-like content.")
            break

        tone = input("Choose tone (casual/formal/storytelling): ").strip().lower()
        if tone not in ["casual", "formal", "storytelling"]:
            tone = "casual"  # default tone

        output = humanize_text(user_input, tone)
        
        print("\n✨ Humanized Content:\n")
        print(output)
        print("\n" + "-"*60 + "\n")

if __name__ == "__main__":
    main()
