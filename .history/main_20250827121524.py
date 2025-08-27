# main.py
from humanizer import TextHumanizer

def main():
    print("🤖 AI Text Humanizer - Target Similarity: < 50%")
    print("=" * 50)
    
    # Create humanizer instance (ensure similarity stays below 50%)
    humanizer = TextHumanizer(target_similarity_range=(0.00, 0.49))
    
    while True:
        print("\nPaste your AI-generated text (multi-line supported). Type 'END' on a new line to finish, or 'quit' to exit:")
        
        # Read multi-line input until a line with END
        lines = []
        while True:
            try:
                line = input(">> ")
            except EOFError:
                # In case of piped input with no END marker
                break
            
            if line.strip().lower() in ['quit', 'exit', 'q'] and not lines:
                print("Goodbye! 👋")
                return
            
            if line.strip() == 'END':
                break
            
            lines.append(line)
        
        ai_text = "\n".join(lines).strip()
        
        if not ai_text:
            print("Please enter some text! (Finish input with a line containing END)")
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
