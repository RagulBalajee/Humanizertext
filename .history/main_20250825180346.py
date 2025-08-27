# main.py
from humanizer import humanize_text

def main():
    print("🤖 Enter your AI-generated text (single paragraph):\n")
    ai_text = input(">> ")

    humanized_text = humanize_text(ai_text)

    print("\n✨ Humanized Text :\n")
    print(humanized_text)

if __name__ == "__main__":
    main()
