# main.py
from humanizer import humanize_paragraph

def main():
    print("🤖 AI to Human Content Converter (~50-55% similarity)")
    print("Type 'exit' anytime to quit.\n")

    while True:
        ai_text = input(">> Enter your AI-generated paragraph:\n")
        if ai_text.lower().strip() == "exit":
            print("\n👋 Goodbye! Keep writing human-like content.")
            break

        humanized = humanize_paragraph(ai_text)

        print("\n✨ Humanized Text:\n")
        print(humanized)
        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    main()
