from flask import Flask, request, jsonify, send_file
from bs4 import BeautifulSoup
from newspaper import Article
from textblob import TextBlob
# from newsapi import NewsApiClient
from transformers import pipeline
import requests
from utils import *
import pandas as pd
import base64
import json
# import nest_asyncio

app = Flask(__name__)

# newsapi = NewsApiClient(api_key='YOUR_NEWS_API_KEY')  # Replace with your API key

# def analyze_news(company, source):
@app.route('/analyze_news', methods=['GET'])
def analyze_news():
    # company = company
    # source = source
    company = request.args.get('company')
    source = request.args.get('source')
    if not company or not source:
        return jsonify({"error": "Please provide a company name as a query parameter"}), 400
    
    all_articles = []
    output = {"Company": f"{company}", "Articles": all_articles}
    
    overall_sentiment_count = 0
    sentiment_count = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    if source == "NewsOrg":
        # Fetch articles from News API
        # response = newsapi.get_everything(q=company, page_size=5, sort_by='publishedAt', language='en')

        params = {"q":"tesla","apiKey":"7396bdb0bc0a42c5b5b0c9c5945d32fa", "pagesize":10, "sortBy": "publishedAt", "language":'en'}
        articles = requests.get(url = "https://newsapi.org/v2/everything", params= params)
        articles = json.loads(articles.text)

        # results = []
        # sentiment_count = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

        # print(f">>>>>>>>>>>>>>>>>>>>>{articles}")
        for idx, article in enumerate(articles["articles"]):
            # print(f">>>>>>>>>>>>>>>>>>>>>{article}")
            url = article.get("url")
            news_article = Article(url)
            try:
                news_article.download()
                news_article.parse()
            except:
                continue

            blob = TextBlob(news_article.text)
            polarity = blob.sentiment.polarity

            if polarity > 0.3:
                sentiment = "POSITIVE"
                overall_sentiment_count += 1
            elif polarity < -0.3:
                sentiment = "NEGATIVE"
                overall_sentiment_count -= 1
            else:
                sentiment = "NEUTRAL"
                # neutral_sentiment_count += 1

            all_articles.append({
                "Title": article.get("title"),
                "Summary": article.get("description"),
                "Sentiment": sentiment
            })

        output["Comparitive Sentiment Score"] = {
            "Sentiment Distribution": sentiment_count
        }

        if overall_sentiment_count>0:
            output["Final Sentiment Analysis"] = f"{company.capitalize()}'s lastest news is mostly positive. Potential stock growth expected."
        elif overall_sentiment_count<0:
            output["Final Sentiment Analysis"] = f"{company.capitalize()}'s lastest news is mostly negative. Potential stock decline expected."
        else:
            output["Final Sentiment Analysis"] = f"{company.capitalize()}'s lastest news is mostly neutral. Stocks going to stay stagnant for some time."
        
        print(output)
        print(f"{'>'*5} Starting text summarization.")

        # return jsonify({
        #     "company": company,
        #     "sentiment_distribution": sentiment_count,
        #     "articles": results
        # })
        # df = pd.DataFrame(all_articles)
        text_to_summarize = " ".join([d['Title'] + " " + d['Summary'] for d in all_articles[:5]])
        summary_final = summarize_text(text_to_summarize)

        audio_path = generate_hindi_tts(summary_final)
        if audio_path:# and os.path.exists(audio_path):
            # Convert audio file to base64
            with open(audio_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            output["Audio"] = audio_base64

            return output

        else:
            return jsonify({"error": "Failed to generate audio"}), 500
    
    elif source == "Yahoo News":
        url = f"https://finance.yahoo.com/quote/{company}/news/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Failed to fetch news articles")
            return {}

        paragraphs = []
        titles = []
        summaries = []
        soup = BeautifulSoup(response.content, 'html.parser')


        for news in soup.find_all("div", class_="holder yf-1napat3"):
            title_all = news.find_all('h3', class_="clamp yf-82qtw3")
            summary_all = news.find_all('p', class_="clamp yf-82qtw3")
            for title, summary in zip(title_all, summary_all):
                title_text = title.get_text()
                summary_text = summary.get_text()
                paragraph = title_text + ' ' + summary_text
                titles.append(title_text)
                summaries.append(summary_text)
                paragraphs.append(paragraph)
        
            # Analyze sentiment and prepare the output
            for i, paragraph in enumerate(paragraphs):
                sentiment = analyze_sentiment(paragraph)
                if sentiment == "POSITIVE":
                    # positive_sentiment_count += 1
                    overall_sentiment_count += 1
                elif sentiment == "NEGATIVE":
                    # negative_sentiment_count += 1
                    overall_sentiment_count -= 1
                # else:
                #     neutral_sentiment_count += 1
                # top_words = 
                sentiment_count[sentiment] += 1

            article = {
                "Title": titles[i],
                "Summary": summaries[i],
                "Sentiment": sentiment
            }

            all_articles.append(article)

        output["Comparitive Sentiment Score"]["Sentiment Distribution"] = sentiment_count

        if overall_sentiment_count>0:
            output["Final Sentiment Analysis"] = f"{company.capitalize()}'s lastest news is mostly positive. Potential stock growth expected."
        elif overall_sentiment_count<0:
            output["Final Sentiment Analysis"] = f"{company.capitalize()}'s lastest news is mostly negative. Potential stock decline expected."
        else:
            output["Final Sentiment Analysis"] = f"{company.capitalize()}'s lastest news is mostly neutral. Stocks going to stay stagnant for some time."
        
        df = pd.DataFrame(all_articles)
        text_to_summarize = " ".join([d['Title'] + " " + d['summary'] for d in article[:5]])
        summary_final = summarize_text(text_to_summarize)

        audio_path = generate_hindi_tts(summary_final)
        if audio_path:# and os.path.exists(audio_path):
            # Convert audio file to base64
            with open(audio_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            output["Audio"] = audio_base64

            return output

        else:
            return jsonify({"error": "Failed to generate audio"}), 500
        # df = pd.DataFrame(all_articles)
        # text_to_summarize = " ".join([d['Title'] + " " + d['summary'] for d in article[:5]])
        # summary_final = summarize_text(text_to_summarize)

        # audio_path = generate_hindi_tts(summary_final)
        # if audio_path:# and os.path.exists(audio_path):
        #     # Convert audio file to base64
        #     with open(audio_path, "rb") as f:
        #         audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            
        #     output["Audio"] = audio_base64

        #     return output

        # else:
        #     return jsonify({"error": "Failed to generate audio"}), 500
    else:
        return jsonify({"error": "Invalid source provided"}), 400 

if __name__ == '__main__':
    app.run(debug=True, port=8000)
