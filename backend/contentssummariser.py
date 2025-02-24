# from transformers import pipeline

# def summarize_text(text, max_length=200, min_length=100):
#     if not text or not isinstance(text, str) or text.strip() == "":
#         return "No content available for summarization."
#     try:
#         summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#         summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
#         summary_text = summary[0]['summary_text']
#         if not summary_text or summary_text.strip() == "":
#             raise ValueError("Empty summary generated")
#         return summary_text
#     except Exception as e:
#         print(f"Error during summarization: {e}")
#         return "Summarization failed due to an error."

import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()

def summarize_text(text, max_length=200, min_length=100, retries=3, delay=5):
    if not text or not isinstance(text, str) or text.strip() == "":
        return "No content available for summarization."

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False
        }
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            summary = response.json()[0]["summary_text"]
            if not summary or summary.strip() == "":
                raise ValueError("Empty summary generated from API")
            print("Summary generated successfully using Hugging Face API.")
            return summary
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"API error (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("All API retries exhausted.")
                return "Summarization failed due to a persistent error."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Summarization failed due to an unexpected error."
        
