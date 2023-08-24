import streamlit as st
from FUNCTIONS import get_data, generate_df, get_freq, get_pos_neg
import pandas as pd
import plotly.express as px


st.title('Ebay Sentiment Analysis Generator')
st.write("This app helps you to see the the sentiment of ebay product review with just one click, you just need to insert the product link")

url = st.text_input('Ebay Product URL', placeholder = 'Insert url here ...')
generateButton = st.button("Generate")

if generateButton:
    with st.spinner('Scraping data ...'):
        data = get_data(url)
    with st.spinner('Transforming data ...'):
        data = generate_df(data)

    # words freq treemap    
    words_freq, clear_words = get_freq(data)
    words_freq = pd.DataFrame(list(words_freq.items()), columns=["Token", "Frequency"]).sort_values('Frequency', ascending=False).head(20)
    words_freq['Top Words'] = 'Top Words'
    fig = px.treemap(words_freq, path=['Top Words', 'Token'], values='Frequency')
    fig.data[0].textinfo = 'label+value'
    
    st.subheader('Words Frequency')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # positive and negative words
    pos_words_freq, neg_words_freq, pos_words, neg_words = get_pos_neg(clear_words)
    
    pos_fig = px.bar(pos_words_freq, x = 'Frequency', y = 'Word', orientation='h')

    color = ['#f54242'] * 20
    neg_fig = px.bar(neg_words_freq, x = 'Frequency', y = 'Word', orientation='h', color_discrete_sequence=color)

    # pos_fig.update_layout(height=700, width = 350)
    # neg_fig.update_layout(height=700, width = 350)
    pos_fig.update_layout(height=700)
    neg_fig.update_layout(height=700)

    st.subheader('Positive and Negative Words')
    col1, col2= st.columns(2)
    with col1:
        st.text('Positive Words Distribution')
        st.plotly_chart(pos_fig, theme="streamlit", use_container_width=True)
    with col2:
        st.text('Negative Words Distribution')
        st.plotly_chart(neg_fig, theme="streamlit", use_container_width=True)

    # overall sentiment
    len_pos_words = len(pos_words)
    len_neg_words = len(neg_words)
    lens = [len_pos_words, len_neg_words]
    labels = ['Positive Words', 'Negative Words']

    st.subheader('Sentiment Result')
    fig_pie = px.pie(values = lens, names = labels)
    st.plotly_chart(fig_pie, use_container_width=True)