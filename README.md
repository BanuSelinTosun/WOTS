# WOTS
# Word On The Street NLP-Based Real Estate Recommender
WOTS is an NLP-based real-estate recommender to help home buyers to find their dream home in Seattle and for real estate agents to offer more relatable listings for their clients.

## Why WOTS?
The Seattle housing market continues to grow and real estate companies strive to use data to create more effective listings. Home buyers continued to seek a more advanced method for finding their dream home, beyond basic information such as square footage, number of bedrooms, etc. The WOTS recommender compares listings utilizing the rich text contained in their  descriptions and recommends homes of a similar style based upon the buyer's interest. In addition, WOTS compares neighborhoods based on your potential neighbors' reviews and recommends homes of similar style in alternative neighborhoods with a similar vibe.

## Data Source
The neighborhood reviews were scraped from streetadvisors.com parsed in to Mongo database in the format of reviews, neighborhood, raw html and url. The real-estate data was provided by flyhomes.com in csv format. In addition to the metadata(number of bedrooms, number of bathrooms, square-footage etc.),the listing dataset contained the geolocations and the text descriptions of the real-estate.

## Data Preparation
The geolocation of the listings were used to identify which neighborhoods they are located based on the City of Seattle defined neighborhood boundaries. Results showed inconsistencies between the realtor defined and city defined neighborhoods. In addition, a dictionary is created based on the streetadvisors.com defined neighborhood boundaries so that the reviews can be matched with the listing locations.
The common abbreviations ("BR", "BA", "FLR" etc.) in the real estate text description were replaced with the related words ("bedroom", "bathroom", "floor" etc.).

## Modeling
The recommender includes two separate data sources: neighborhood reviews and the listing text descriptions. After user inputs the metadata of number of minimum bedroom, number of minimum bathroom, property type, neighborhood and maximum price the model first and finds the matching options within the given neighborhood. Then, based on the selected property:
* Model recommends alternative neighborhoods based on the text similarities of the each neighborhood reviews. Model filters each neighborhood reviews and only keeps  the nouns and adjectives of each review using part-of-speech tag function (pos_tag) from NLTK library. Then, model calculates the Term Frequency - Inverse Document Frequency vectors (TF_IDF) for each neighborhood based on the filtered neighborhood reviews. Then model  calculates the cosine similarity for these neighborhoods and finds top-K most similar options. In the model K is set as 2.
* Model recommends alternative real-estate listing based on the text description similarities between the selected listing and the remaining listings within the selected and model recommended alternative neighborhoods. Similar to neighborhood recommender explained above, model find top-K real estates in each neighborhood based on the text description TF-IDF vector similarities.
Since the listing context is specific to the property features, the pos_tag function is not used to filter.

## Deployment
A webapp is created to show how this model can improve flyhomes.com website and help home buyers to find similar listings and displayed below.


![](img/wots_record.gif)

![](img/tools.png)
