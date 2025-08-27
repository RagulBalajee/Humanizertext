# test_consistency.py
from humanizer import TextHumanizer

def test_consistency():
    """Test that the humanizer produces consistent 50-55% similarity"""
    
    # Sample AI text
    ai_text = """
    Artificial intelligence has revolutionized the way we approach problem-solving in modern technology. 
    Machine learning algorithms can process vast amounts of data to identify patterns and make predictions 
    with remarkable accuracy. The implementation of AI systems requires careful consideration of ethical 
    implications and potential biases in the training data. Organizations must develop comprehensive 
    strategies to integrate AI solutions while maintaining transparency and accountability.
    """
    
    print("🧪 Testing AI Text Humanizer Consistency")
    print("=" * 50)
    print(f"Original AI Text:\n{ai_text.strip()}")
    print("\n" + "=" * 50)
    
    # Create humanizer with target 50-55% similarity
    humanizer = TextHumanizer(target_similarity_range=(0.50, 0.55))
    
    # Test multiple runs
    for i in range(5):
        print(f"\n🔄 Test Run #{i+1}")
        print("-" * 30)
        
        humanized_text, similarity = humanizer.humanize_text(ai_text)
        
        print(f"Similarity: {similarity:.1%}")
        print(f"Target Range: 50%-55%")
        
        if 0.50 <= similarity <= 0.55:
            print("✅ Target achieved!")
        else:
            print("⚠️  Outside target range")
            
        print(f"Humanized Text:\n{humanized_text}")
        print("-" * 30)
    
    print("\n🎯 Summary:")
    print("The humanizer is designed to consistently produce text with 50-55% similarity")
    print("to the original AI text, making it sound more human while maintaining coherence.")

if __name__ == "__main__":
    test_consistency()
