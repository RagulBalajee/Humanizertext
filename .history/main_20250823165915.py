from humanizer import humanize_text

print("🤖 AI to Human Content Converter")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("Enter AI-generated text: ")
    if user_input.lower() == "exit":
        break
    
    tone = input("Choose tone (casual/formal/storytelling): ").strip().lower()
    output = humanize_text(user_input, tone)
    
    print("\n✨ Humanized Content:\n", output, "\n")
