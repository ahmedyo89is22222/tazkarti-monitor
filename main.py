import requests
import time
import os

from plyer import notification

API_URL = "https://www.tazkarti.com/data/matches-list-json.json"

CHECK_EVERY = 20

BOT_TOKEN = "8542294581:AAH2Ee32XIUSu3YBCg-bvp9t04R4jbUKgR8"

CHAT_ID = "7249225351"

seen_matches = set()

first_run = True


def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


while True:

    os.system("cls")

    print("==== AVAILABLE MATCHES ====\n")

    try:

        response = requests.get(API_URL)

        matches = response.json()

        current_matches = set()

        for match in matches:

            home_team = match.get("teamName1", "Unknown")
            away_team = match.get("teamName2", "Unknown")

            match_text = f"{home_team} VS {away_team}"

            current_matches.add(match_text)

            print(match_text)

            # لو مش أول تشغيل
            if not first_run:

                # ماتش جديد
                if match_text not in seen_matches:

                    print(f"\nNEW MATCH FOUND: {match_text}")

                    # Notification
                    notification.notify(
                        title="NEW MATCH ADDED!",
                        message=match_text,
                        timeout=10
                    )

                    # صوت
                    print("\a")

                    # TELEGRAM MESSAGE
                    send_telegram_message(
                        f"🚨 NEW MATCH ADDED!\n\n{match_text}"
                    )

        print("\n==========================")
        print(f"TOTAL MATCHES: {len(matches)}")

        seen_matches = current_matches

        first_run = False

    except Exception as e:

        print("ERROR:", e)

    time.sleep(CHECK_EVERY)
