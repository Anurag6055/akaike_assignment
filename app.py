import streamlit as st
import requests
import nest_asyncio

nest_asyncio.apply()

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
                st.subheader(f"Sentiment Analysis for {data['Company']}")

                # Comparative Sentiment Score
                st.write("### Comparative Sentiment Score")
                sentiment_dist = data.get("Comparitive Sentiment Score", {})
                st.json(sentiment_dist)

                # Final Sentiment Analysis
                st.write("### Final Sentiment Analysis")
                st.success(data.get("Final Sentiment Analysis", "No analysis available"))

                # Audio Player for Hindi TTS
                if "Audio" in data:
                    st.write("### Listen to Hindi Summary")
                    audio_bytes = base64.b64decode(data["Audio"])
                    st.audio(audio_bytes, format="audio/mp3")

                # Articles Display
                st.write("### Articles:")
                for idx, article in enumerate(data["Articles"]):
                    st.write(f"**{idx+1}. Title:** {article['Title']}")
                    st.write(f"**Sentiment:** {article['Sentiment']}")
                    st.write(f"**Summary:** {article['Summary']}")
                    st.markdown("---")
            else:
                st.error("Failed to fetch data from API.")
