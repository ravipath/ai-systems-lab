import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key, 
)

def openrouter_chatbot():
    if not api_key:
        print("Error: API Key not found! Make sure your .env file is set up correctly.")
        return

    print("--- OpenRouter CLI Chatbot (Secure Mode) ---")
    model_name = "nvidia/nemotron-nano-9b-v2:free"
    messages = [{"role": "system", "content": "You are a helpful AI."}]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True, # <--- This is the magic change
                extra_headers={"HTTP-Referer": "http://localhost:3000", "X-Title": "Python CLI Bot"}
            )

            print("\nBot: ", end="", flush=True)
            full_reply = ""

            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True) # Print word by word
                    full_reply += content

            print()
            messages.append({"role": "assistant", "content": full_reply})

        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    openrouter_chatbot()
