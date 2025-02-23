from transformers import pipeline

def summarize_text(text, max_length=200, min_length=100):
    if not text:
        return "No content available for summarization."
    
    # Use a smaller model
    summarizer = pipeline("summarization", model="facebook/bart-large")
    
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summarization failed due to an error."
