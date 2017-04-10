from __future__ import division
import pandas as pd
import numpy as np
import system as S
import gmplot
from flask import Flask, render_template,request,jsonify

df_reviews=pd.read_csv('data/street_reviews.csv')
df_reviews.drop('Unnamed: 0', axis=1, inplace=True)
df_sample=pd.read_csv('data/data_active_clean.csv')
df_sample.drop('Unnamed: 0', axis=1, inplace=True)
column_names = ['id','bed','bath','address','street_neighborhood','price']
new_col_names = ['ID','Bedroom','Batroom', 'Address', "Neighborhood", "Price"]
recsys =S.RecommenderSystem(df_sample,df_reviews)


app = Flask(__name__)

@app.route('/', methods =['GET'])
def index():
    return render_template('wots.html')

@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    minbed, minbath, proptype, neighborhood, maxprice = (
                                                          user_data['minbed'],
                                                          user_data['minbath'],
                                                          user_data['proptype'],
                                                          user_data['neighborhood'],
                                                          user_data['maxprice']
                                                          )

    return _return_selected(minbed, minbath, proptype, neighborhood, maxprice)


@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    listing_id = int(user_data)
    return _recommend(listing_id)


def _return_selected(minbed, minbath, proptype, neighborhood, maxprice):
    """ Returns real-estate listing table and locations (latitudes and longitudes)
    ARGS:
        minbed (int) = minimum number of bedroom
        minbath (int) = minimum number of bathroom
        proptype (string) = property type
        neighborhood (string) = neighborhood name
        maxprice (int) = maxiumum real-estate listing price

    RETURNS:
        table (html) : listing table
        loc_list (list) : list of 'id','latitude','longitude','url' of the tabulated listings
        lat_long (dict) : central 'latitude','longitude' of tabulated listings
    """

    selected_list=recsys.input_func(minbed, minbath, proptype, neighborhood, maxprice)
    if type(selected_list)==list:
        df = df_sample[df_sample['id'].isin(selected_list)][column_names]
        df.sort_values('price',ascending=True,inplace=True)
        df['price'] = df['price'].apply(lambda x: '${:,.0f}'.format(x))
        df.columns = new_col_names
        df=df.head(7)

        return jsonify({
            'table' : df.to_html(index=False, classes='table'),
            'loc_list':_create_location_list(df_sample,selected_list),
            'lat_long':_lat_lng(df_sample,selected_list)

            })
    else:
        return jsonify({'table' : 'Sorry, no match found. Please change your search options and try again :)'})


def _create_location_list(df_sample,selected_list):
    """ Returns real-estate listing table and locations (latitudes and longitudes)
    ARGS:
        df_sample (DataFrame) = real-estate listing data frame
        selected_list (int) = user selected listing id

    RETURNS:
        (list) : list of 'id','latitude','longitude','url' of the selected listing
    """
    df_plot = df_sample[df_sample['id'].isin(selected_list)]
    df_plot['price'] = df_plot['price'].apply(lambda x: '${:,.0f}'.format(x))
    df_plot['id'] = df_plot['id'].apply(lambda x : str(x))
    return df_plot[['id','latitude','longitude','url']].values.tolist()

def _lat_lng(df_sample,selected_list):
    """
    ARGS:
        df_sample (DataFrame) = real-estate listing data frame
        selected_list (int) = user selected listing id

    RETURNS:
        (dict) : central 'latitude','longitude' of tabulated listings
    """
    lat = np.mean(df_sample['latitude'][df_sample['id'].isin(selected_list)].values)
    lng = np.mean(df_sample['longitude'][df_sample['id'].isin(selected_list)].values)
    return {'lat':lat,'lng':lng}

def _recommend(listing_id):
    """
    ARGS:
    listing_id (int) : selected listing id

    RETURNS:
        table (html) : recommended listing table
        loc_list (list) : list of 'id','latitude','longitude','url' of the tabulated listings
        lat_long (dict) : central 'latitude','longitude' of tabulated listings
    """
    selected_list = recsys.listing_recommender(listing_id)
    if type(selected_list)==list:
        df = df_sample[df_sample['id'].isin(selected_list)][column_names]
        df.sort_values('price',ascending=True,inplace=True)
        df['price'] = df['price'].apply(lambda x: '${:,.0f}'.format(x))
        df.columns = new_col_names
        df=df.head(7)
        return jsonify({
            'table' : df.to_html(index=False, classes='table'),
            'loc_list':_create_location_list(df_sample,selected_list),
            'lat_long':_lat_lng(df_sample,selected_list)

            })
    else:
        return jsonify({'table' : 'Sorry, no match found. Please change your search options and try again :)'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)
