 import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"


def ask_ollama(prompt):
    """Send a question to the local Ollama AI model."""

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are SmartChef AI, a helpful cooking assistant. "
                    "Recommend practical meals using available ingredients. "
                    "Prioritize recipes requiring fewer additional ingredients. "
                    "Clearly identify missing ingredients. "
                    "Do not claim that missing ingredients are available. "
                    "Give clear, beginner-friendly cooking advice."
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
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["message"]["content"]

    except urllib.error.URLError:
        return (
            "Could not connect to Ollama. "
            "Make sure Ollama is installed and running."
        )

    except (TimeoutError, KeyError, ValueError):
        return (
            "The AI request failed. Check that your model is installed "
            "and try again."
        )


def get_cooking_advice(ingredients, recipes):
    """Ask Ollama to explain the matching recipe suggestions."""

    prompt = f"""
The user has these household ingredients:
{ingredients}

These recipes were matched against the user's ingredients:
{json.dumps(recipes, indent=2)}

Explain which recipes are the most practical choices.
Prioritize recipes requiring the fewest additional ingredients.
Mention missing ingredients clearly.
Use simple language and numbered steps.
Do not invent ingredients that the user has available.
"""

    return ask_ollama(prompt)
