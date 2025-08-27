from humanizer import humanize_text

def main():
    print("💡 Enter a sentence you want to humanize:")
    ai_text = input(">>> ")

    print("\n🤖 AI-Generated Text:\n")
    print(ai_text)

    humanized = humanize_text(ai_text)

    print("\n✨ Humanized Text:\n")
    print(humanized)

if __name__ == "__main__":
    main()
