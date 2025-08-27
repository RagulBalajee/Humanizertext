# test_consistency.py
from humanizer import TextHumanizer

def test_consistency():
    ai_text = "Artificial intelligence has revolutionized problem-solving. Machine learning algorithms process data to identify patterns."
    
    print("🧪 Testing Consistency - Target: 50-55% Similarity")
    print("=" * 50)
    
    humanizer = TextHumanizer(target_similarity_range=(0.50, 0.55))
    
    for i in range(3):
        print(f"\n🔄 Run #{i+1}")
        humanized_text, similarity = humanizer.humanize_text(ai_text)
        print(f"Similarity: {similarity:.1%}")
        print(f"Text: {humanized_text}")

if __name__ == "__main__":
    test_consistency()
