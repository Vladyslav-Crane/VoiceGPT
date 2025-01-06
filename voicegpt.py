#! /usr/bin/env python3
import os
import time
import openai
import pyaudio
import speech_recognition as speech_recog

client = openai.Client()

r = speech_recog.Recognizer()
mic = speech_recog.Microphone()


def speak(text, voice="alloy"):
    player_stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16, channels=1, rate=24000, output=True
    )
    start_time = time.time()

    with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        response_format="pcm",  # similar to WAV, but without a header chunk at the start.
        input=text,
    ) as response:
        print(f"Time to first byte: {int((time.time() - start_time) * 1000)}ms")
        for chunk in response.iter_bytes(chunk_size=1024):
            player_stream.write(chunk)

    print(f"Done in {int((time.time() - start_time) * 1000)}ms.")


def listen():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Transcribing...")
        query = r.recognize_openai(audio)
        print(f"You said: {query}")
        return query
    except speech_recog.UnknownValueError:
        print("I did not get that.")
        return None
    except speech_recog.RequestError as e:
        print(f"Error: {e}")
        return None


def get_completion(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content


def main():
    print("Say something to ChatGPT (Ctrl+C to exit)...")
    user_query = listen()
    if user_query:
        answer = get_completion(user_query)
        speak(answer)


if __name__ == "__main__":
    main()
