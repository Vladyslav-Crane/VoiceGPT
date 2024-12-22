import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")

CHAT_MODEL = 'gpt-4o-mini'

def query_openai(prompt):

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def main():
    print("VoiceGPT is ready.")
    user_prompt = input("Prompt: ")
    response = query_openai(user_prompt)
    print(f"ChatGPT: {response}")

if __name__ == "__main__":
    main()
