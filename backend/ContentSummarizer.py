from transformers import pipeline

def summarize_text(text, max_length=200, min_length=100):
    """
    Summarize the given text using a pre-trained model from Hugging Face.
    """
    if not text:
        return "No content available for summarization."
    
    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Summarize the text
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summarization failed due to an error."