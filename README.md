# eBay Sentiment Analysis Generator


This app will help you to find the summary of reviews sentiment, where there are three main charts:
- Words Frequency
- Positive and Negative Words
- Sentiment Result

This app created with Python programming language, made with Streamlit, this app scrape reviews data using BeautifulSoup, then will process the data mainly use Pandas, for the sentiment analysis use NLTK, and for the visualization use Plotly

To use this app you can go to this url
https://ebay-sentiment-analysis-generator.streamlit.app/

or from the file go to app.py file then run 
`streamlit run app.py`

The app will show title, simple description, and one input field for you to input the product url, insert the product details url that want to be analyzed, and make sure that the product has Rating and Reviews section.
Here are some product url example that can be used to see the result:
- https://www.ebay.com/itm/PS5-Sony-PlayStation-5-Console-Disc-Version-/325389825157

- https://www.ebay.com/itm/294111390755?hash=item447a67ac23:g:V84AAOSw2wZjWgJP&amdata=enc%3AAQAIAAAA0PXNcLBcSbU63dNav9kkyUvrCeYHzi7JX4oTzoHt9tIts52pZ1RYNVaHIlpQxeuwaSoSBPrhcbrgodH8kLhbjr%2BwQup8CDrNZm8tZvAgh8VRUIveXqCqT6ZwkSDJ6SwzKIfd0Y58zjFGfKA9LG1DJm7RZMapIzXAuv6%2FKAfmTlbTzErRFbsq%2BkLoKbdITsFt7Q5QydtaAiAKPXgjmgMiXJSg3SBPZCyYDHsShPwVmxOoW0FC1MIasKIdyGL1x9aIP5VGIzpMyVzvOVu%2FjyRtUZY%3D%7Ctkp%3ABFBMqMOY_MRi
