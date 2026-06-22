import os
import json
import time # <--- Import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"), 
)

def save_chat_log(user_text, bot_text, model_name, latency):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": model_name,
        "user": user_text,
        "bot": bot_text,
        "latency_sec": round(latency, 3) # Store latency rounded to 3 decimal places
    }

    with open("logs/chat.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def openrouter_chatbot():
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: API Key not found!")
        return

    print("--- OpenRouter CLI Chatbot (Latency Tracking) ---")
    model_name = "nvidia/nemotron-nano-9b-v2:free" 
    messages = [{"role": "system", "content": "You are a helpful AI."}]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        messages.append({"role": "user", "content": user_input})

        try:
            # --- START TIMER ---
            start_time = time.time() 

            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True,
                extra_headers={"HTTP-Referer": "http://localhost:3000", "X-Title": "Python CLI Bot"}
            )

            print("\nBot: ", end="", flush=True)
            full_reply = ""

            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    full_reply += content
            print()

            # --- END TIMER ---
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"⏱️  Response time: {elapsed_time:.2f} seconds")

            # Pass the latency to the logger
            save_chat_log(user_input, full_reply, model_name, elapsed_time)

            messages.append({"role": "assistant", "content": full_reply})

        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    openrouter_chatbot()
