# main.py
from humanizer import TextHumanizer

def main():
    print("🤖 AI Text Humanizer - Target Similarity: < 50%")
    print("=" * 50)
    
    # Create humanizer instance (ensure similarity stays below 50%)
    humanizer = TextHumanizer(target_similarity_range=(0.00, 0.49))
    
    while True:
        print("\nEnter your AI-generated text (or 'quit' to exit):")
        ai_text = input(">> ")
        
        if ai_text.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
            
        if not ai_text.strip():
            print("Please enter some text!")
            continue
        
        print("\n🔄 Humanizing text...")
        
        # Humanize the text
        humanized_text, similarity = humanizer.humanize_text(ai_text)
        
        print(f"\n📊 Similarity: {similarity:.1%}")
        print(f"🎯 Target: < 50% (current bounds: {humanizer.target_similarity_range[0]:.0%}-{humanizer.target_similarity_range[1]:.0%})")
        
        print("\n✨ Humanized Text:")
        print("-" * 30)
        print(humanized_text)
        print("-" * 30)
        
        # Show if target was achieved
        if humanizer.target_similarity_range[0] <= similarity <= humanizer.target_similarity_range[1]:
            print("✅ Below 50% — target achieved!")
        else:
            print("⚠️  Not within target bounds, best result returned")

if __name__ == "__main__":
    main()
