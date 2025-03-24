import streamlit as st
import requests
from api import analyze_news
# import nest_asyncio

st.title("Company News Sentiment Analyzer")

company = st.text_input("Enter Company Name", placeholder="Example: Tesla")
source =  st.selectbox(
    "Select the source you want news from: ", ("NewsOrg", "Yahoo News")
)

if st.button("Fetch News & Analyze"):
    if not company or not source:
        st.error("Please enter a company name! or select the source")
    else:
        with st.spinner("Fetching from API..."):
            api_url = f"http://localhost:8000/analyze_news?company={company}&source={source}"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
            # data = analyze_news(company = company, source = source)
            # nest_asyncio.apply()
            # if data:

                st.subheader(f"Sentiment Distribution for {company}")
                st.json(data["sentiment_distribution"])

                st.subheader("Articles:")
                for idx, article in enumerate(data["articles"]):
                    st.write(f"**{idx+1}. Title:** {article['title']}")
                    st.write(f"**Sentiment:** {article['sentiment']}")
                    st.write(f"**Summary:** {article['summary']}")
                    st.write(f"[Read Full Article]({article['url']})")
                    st.markdown("---")
            else:
                st.error("Failed to fetch data from API.")
