import streamlit as st
# NLP Pkgs
from textblob import TextBlob
import pandas as pd
import numpy as np
import nltk
nltk.download()

# Emoji
import emoji

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

#Data Viz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

# Fetch Text From Url
@st.cache
def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text



def main():
	"""Sentiment Analysis Web App """

	st.title("Sentiment Analysis Web App")

	activities = ["Sentiment","Text Analysis from URL","About"]
	choice = st.sidebar.selectbox("Choice",activities)

	# Choice = Sentiment
	if choice == 'Sentiment':
		st.subheader("Sentiment Analysis")
		#st.write(emoji.emojize('Everyone :red_heart: Streamlit ',use_aliases=True))
		raw_text = st.text_area("Enter Your Text","Type Here")
		if st.button("Analyze"):
			blob = TextBlob(raw_text)
			result = blob.sentiment.polarity
			if result > 0.0:
				custom_emoji = ':smile:'
				st.markdown('Sentiment :: {}'.format(custom_emoji))
			elif result < 0.0:
				custom_emoji = ':disappointed:'
				st.markdown('Sentiment :: {}'.format(custom_emoji))
			else:
				custom_emoji = ':expressionless:'
				st.markdown('Sentiment :: {}'.format(custom_emoji))

			st.info("Polarity Score is:: {}".format(result))
	
	# Choice Text Analysis
	if choice == 'Text Analysis from URL':
		st.subheader("Analysis on Text From URL")
		raw_url = st.text_input("Enter URL Here","Type here")
		text_preview_length = st.slider("Length to Preview",50,100)
		if st.button("Analyze"):
			if raw_url != "Type here":
				result = get_text(raw_url)
				blob = TextBlob(result)
				len_of_full_text = len(result)
				len_of_short_text = round(len(result)/text_preview_length)
				st.success("Length of Full Text::{}".format(len_of_full_text))
				st.success("Length of Short Text::{}".format(len_of_short_text))
				st.info(result[:len_of_short_text])
				c_sentences = [ sent for sent in blob.sentences ]
				c_sentiment = [sent.sentiment.polarity for sent in blob.sentences]

				# Dataframe
				new_df = pd.DataFrame(zip(c_sentences,c_sentiment),columns=['Sentence','Sentiment'])
				st.dataframe(new_df)

				#Plot 
				st.write(new_df.head(20).plot(kind='bar'))
				st.pyplot()
				st.write(new_df.dtypes)
				result_avg = round(np.mean(c_sentiment, axis = 0),3)
				st.write(result_avg)
				st.markdown('##### Average Sentiment of Complete Text')
				if result_avg > 0.0:
					custom_emoji = ':smile:'
					st.markdown('Sentiment :: {}'.format(custom_emoji))
				elif result_avg < 0.0:
					custom_emoji = ':disappointed:'
					st.markdown('Sentiment :: {}'.format(custom_emoji))
				else:
					custom_emoji = ':expressionless:'
					st.markdown('Sentiment :: {}'.format(custom_emoji))

			st.info("Average polarity Score is:: {}".format(result_avg))

	# Choice Abou
	if choice == 'About':
		st.subheader("About")
		st.markdown("""
			#### Sentiment Analysis Web App
			##### Built with Streamlit

			#### By
			+ Hrishikesh Sharad Malkar
			+ References: Jesus Saves@[JCharisTech](https://jcharistech.com)

			""")
		

if __name__ == '__main__':
	main()