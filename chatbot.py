def get_response(message):
    msg = message.lower().strip()

    if "hello" in msg or "hi" in msg or "hey" in msg:
        return "Hey there! How can I help you today?"

    elif "how are you" in msg or "how r u" in msg:
        return "I'm just a bot, but I'm doing fine! Thanks for asking."

    elif "your name" in msg or "who are you" in msg:
        return "I'm RuleBot — a simple chatbot built with pre-defined rules!"

    elif "what can you do" in msg or "what can u do" in msg or "help" in msg:
        return "I can answer greetings, tell jokes, and more. Try asking!"

    elif "joke" in msg:
        import random
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers to change a bulb? None — it's a hardware problem.",
            "Why did the developer go broke? They used up all their cache!",
        ]
        return random.choice(jokes)

    elif "thanks" in msg:
        return "You're welcome! Let me know if you need anything else."

    elif "age" in msg or "how old are you" in msg:
        return "I was born the moment my code was written!"

    elif "bye" in msg or "goodbye" in msg or "exit" in msg:
        return "Goodbye! Have a wonderful day!"

    else:
        return "I don't have a rule for that. Try: greetings, jokes, etc."


def main():
    print("RuleBot is running! Type 'bye' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        response = get_response(user_input)
        print(f"Bot: {response}\n")

        if any(word in user_input.lower() for word in ["bye", "goodbye", "exit"]):
            break

main()