# conversation_orchestrator.py

import requests
import time
import os
import sys

bot_a_url = os.getenv("BOT_A_URL")
bot_b_url = os.getenv("BOT_B_URL")

if not bot_a_url or not bot_b_url:
    print(f"❌ BOT_A_URL: {bot_a_url}")
    print(f"❌ BOT_B_URL: {bot_b_url}")
    print("❌ Required environment variables not set. Exiting.")
    sys.exit(1)


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

        speaker = "Bot_A" if current_bot == "A" else "Bot_B"
        transcript.append((speaker, response))

        # Prepare for next round
        current_message = response
        current_bot = "B" if current_bot == "A" else "A"

        time.sleep(1)  # Short pause between rounds

    except Exception as e:
        print(f"Error during round {i+1}: {e}")
        break

if 'response' in locals() and 'res' in locals():
    print(f"\n✅ Final: Bot {current_bot} responded last: {response}")
    print(f"Status: {res.status_code}")
else:
    print("\n❌ No successful response. Conversation did not complete.")


# Print transcript
print("\n📜 Conversation Transcript:")
for speaker, line in transcript:
    print(f"{speaker}: {line}")
