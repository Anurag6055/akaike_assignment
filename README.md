# News Sentiment Analysis & Hindi Text-to-Speech (TTS) Web Application

## Objective
This project is a web-based application that:
- Extracts key details from multiple news articles about a **user-provided company**
- Performs **sentiment analysis**
- Conducts **comparative sentiment analysis**
- Generates a **Hindi Text-to-Speech (TTS)** audio report
- Provides a user-friendly interface for interaction

The tool allows users to input a company name and receive a **structured sentiment report** along with **audio output**.

---

## Features
1. **News Extraction**: Scrapes and displays the title, summary, and metadata from at least 10 unique news articles (non-JavaScript pages) using **BeautifulSoup (bs4)**.
2. **Sentiment Analysis**: Determines the sentiment (positive, negative, neutral) of each article.
3. **Comparative Analysis**: Compares sentiment across articles to visualize sentiment distribution.
4. **Hindi TTS Generation**: Converts summarized insights into Hindi audio using an open-source TTS model.
5. **User Interface**: Simple web UI built with **Streamlit** or **Gradio**.
6. **API Communication**: Frontend and backend communicate via **REST APIs**.
7. **Deployment**: Live deployment on **Hugging Face Spaces**.
8. **Documentation**: Complete setup and usage guide.

---

## Project Setup

### Clone the Repository
```bash
git clone https://github.com/yourusername/news-sentiment-tts.git
cd news-sentiment-tts
```

### Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Application Locally
```bash
streamlit run app.py
```
```bash
python api.py
```
_or_
```bash
python app.py  # If using Gradio
```

### Deployment
The app is deployed on Hugging Face Spaces:
```
https://huggingface.co/spaces/yourusername/news-sentiment-tts
```

---

## Model Details

| Task                  | Model Used                          | Description |
|-----------------------|-------------------------------------|------------|
| **Summarization**     | `transformers.pipeline('summarization')` | Hugging Face pre-trained model for article summary generation |
| **Sentiment Analysis**| `transformers.pipeline('sentiment-analysis')` | Classifies article sentiment into Positive/Negative/Neutral |
| **Text-to-Speech**    | Coqui TTS / `indic-tts`             | Open-source TTS model to generate Hindi speech from text |

---

## API Development & Usage

### Backend APIs:
- **Endpoint**: `/analyze_news`
  - **Method**: POST
  - **Input**: `{"company": "Company Name"}`
  - **Output**: List of news articles with metadata

### Testing with Postman:
1. Set API base URL as `http://localhost:8000/`
2. Select appropriate endpoints and POST body
3. Test responses for JSON or audio file streaming

---

## Third-Party API Usage
| API/Library            | Purpose                                               |
|------------------------|--------------------------------------------------------|
| **News scraping**      | BeautifulSoup (no external news APIs used)             |
| **Hugging Face models**| Sentiment analysis & summarization                    |
| **gtts** | Hindi Text-to-Speech generation                     |

---

## Assumptions & Limitations
- **Scraping Limitations**: Only static, non-JS websites are scraped due to `BeautifulSoup` limitations. Also newsorg pi is also used.
- **Article Count**: A minimum of 10 articles is targeted, but the count may vary based on search results.
- **Language Support**: Sentiment analysis is primarily in English, TTS is specifically Hindi.
- **Deployment**: Optimized for Hugging Face Spaces; heavy TTS models may experience latency. Due to flask being used hugging face is not able to run two files at a time

---

## Dependencies
```text
beautifulsoup4
requests
transformers
torch
streamlit
gtts
scikit-learn
```

---