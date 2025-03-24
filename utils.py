from transformers import pipeline
from gtts import gTTS
from googletrans import Translator

# Loading models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # Load summarizer
sentiment_analyzer = pipeline("sentiment-analysis") # Load sentiment analyzer
# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli") # Load classifier

def analyze_sentiment(text):
    result = sentiment_analyzer(text[:500])[0]
    return result['label']

def summarize_text(text):
    cleaned_text = text.strip().replace("\n", " ")
    cleaned_text = cleaned_text[:3000]  # Limit to avoid token overflow

    result = summarizer(
        cleaned_text,
        max_length=130,
        min_length=30,
        do_sample=False
    )

    summary_text = result[0]['summary_text']
    return summary_text


def translate_to_hindi(text):
    translator = Translator()
    result = translator.translate(text, dest='hi')
    return result.text

def generate_hindi_tts(text, filename="output.mp3"):
    try:
        hindi_text = translate_to_hindi(text)
        tts = gTTS(text=hindi_text, lang='hi')
        tts.save(filename)
        print(f"Hindi audio saved to {filename}")
        return filename
    except Exception as e:
        print(f"Error in generating the TTS: {e}")
        return None
