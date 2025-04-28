# conversation_orchestrator.py

import requests
import time

bot_a_url = "http://localhost:8001/message"
bot_b_url = "http://localhost:8002/message"

initial_message = "Hello, who are you?"
current_message = initial_message
current_bot = "A"
transcript = [("User", initial_message)]

ROUNDS = 5  # total exchanges

for i in range(ROUNDS):
    try:
        if current_bot == "A":
            print(f"\n👉 Sending to Bot A: {current_message}")
            res = requests.post(bot_a_url, json={"message": current_message})
            res.raise_for_status()
            try:
                print(f"Raw response: {res.text}")
                response = res.json()["response"]
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
                break
            transcript.append(("Bot_A", response))
            current_bot = "B"
        else:
            print(f"\n👉 Sending to Bot B: {current_message}")
            res = requests.post(bot_b_url, json={"message": current_message})
            res.raise_for_status()
            try:
                print(f"Raw response: {res.text}")
                response = res.json()["response"]
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
                break
            transcript.append(("Bot_B", response))
            current_bot = "A"

        current_message = response
        time.sleep(1)  # short pause between rounds
    except Exception as e:
        print(f"Error during round {i+1}: {e}")
        break

print(f"✅ Bot {current_bot} responded: {response}")
print(f"Status: {res.status_code}")

# Print transcript
print("\n📜 Conversation Transcript:")
for speaker, line in transcript:
    print(f"{speaker}: {line}")


