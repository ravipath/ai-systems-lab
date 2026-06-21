import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the variables from the .env file into the system
load_dotenv()

# 2. Retrieve the specific key using os.getenv
api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize the OpenRouter client using the key from the .env file
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key, 
)

def openrouter_chatbot():
    # Check if the key was actually loaded
    if not api_key:
        print("Error: API Key not found! Make sure your .env file is set up correctly.")
        return

    print("--- OpenRouter CLI Chatbot (Secure Mode) ---")
    # ... (rest of your chatbot code remains the same)
    model_name = "nvidia/nemotron-nano-9b-v2:free"
    messages = [{"role": "system", "content": "You are a helpful AI."}]

# ... (rest of your setup code)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        messages.append({"role": "user", "content": user_input})

        try:
            # Added stream=True here
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True, # <--- This is the magic change
                extra_headers={"HTTP-Referer": "http://localhost:3000", "X-Title": "Python CLI Bot"}
            )

            print("\nBot: ", end="", flush=True)
            full_reply = ""

            # Loop through the stream of chunks
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True) # Print word by word
                    full_reply += content

            print() # Add a newline at the end
            messages.append({"role": "assistant", "content": full_reply})

        except Exception as e:
            print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    openrouter_chatbot()
