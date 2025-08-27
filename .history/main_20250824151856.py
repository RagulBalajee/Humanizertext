from humanizer import Humanizer

def main():
    humanizer = Humanizer()

    # Example input
    input_text = "Cinema is a powerful medium that reflects culture, influences society, and provides entertainment to audiences worldwide."

    print("\n🤖 AI-Generated Text:\n")
    print(input_text)

    print("\n✨ Humanized Variations:\n")
    variations = humanizer.humanize(input_text, num_variations=4)
    for i, v in enumerate(variations, start=1):
        print(f"{i}. {v}")

if __name__ == "__main__":
    main()
