import urllib.request
import urllib.error
import json
def ask_ollama(prompt):
    """Send a prompt to the local Ollama model."""

    data = {
        "model": "llama3.2",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are SmartChef AI, a helpful cooking assistant. "
                    "Use the supplied recipe information when discussing "
                    "specific recipes. Clearly identify missing ingredients."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request, timeout=120
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result["message"]["content"]

    except (urllib.error.URLError, TimeoutError, KeyError, ValueError):
        return None
print("================================")
print("       SMARTCHEF AI")
print("================================")

print("Welcome to SmartChef AI!")
print("Tell us which ingredients you have at home.")

ingredients = input("Enter your ingredients: ")

print("\nYour available ingredients are:")
print(ingredients)

print("\nSmartChef AI is getting ready to recommend dishes!")
use_ai = input("\nWould you like AI cooking advice? (yes/no): "
    ).strip().lower()

if use_ai in ("yes", "y"):
        prompt = (
            f"The user has these ingredients: {ingredients}. "
            "Give practical cooking suggestions. "
            "Prioritize dishes requiring fewer additional ingredients. "
            "Mention missing ingredients clearly."
        )

        print("\nConnecting to Ollama...")

        answer = ask_ollama(prompt)

        if answer:
            print("\nSmartChef AI says:\n")
            print(answer)
        else:
            print(
                "Could not connect to Ollama. "
                "Check that Ollama is running and the model is installed."
            )