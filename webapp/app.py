from __future__ import division
import pandas as pd
import numpy as np
import system as S
import gmplot
from flask import Flask, render_template,request,jsonify

df_reviews=pd.read_csv('data/street_reviews.csv')
df_reviews.drop('Unnamed: 0', axis=1, inplace=True)
df_sample=pd.read_csv('data/data_seattle.csv')
df_sample.drop('Unnamed: 0', axis=1, inplace=True)
column_names = ['bed','bath','address','street_neighborhood','price']
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


def _return_selected(minbed, minbath, proptype, neighborhood, maxprice):
    selected_list=recsys.input_func(minbed, minbath, proptype, neighborhood, maxprice)
    if type(selected_list)==list:
        df = df_sample[df_sample['id'].isin(selected_list)][column_names]
        df=df.head(5)

        return jsonify({
            'table' : df.to_html(index=False, classes='table'),
            'loc_list':_create_location_list(df_sample,selected_list),
            'lat_long':_lat_lng(df_sample,selected_list)

            })
    else:
        return jsonify({'table' : 'Sorry, no match found. Please change your search options and try again :)'})


def _create_location_list(df_sample,selected_list):
    df_plot = df_sample[df_sample['id'].isin(selected_list)]
    return df_plot[['price','latitude','longitude']].values.tolist()

def _lat_lng(df_sample,selected_list):
    lat = np.mean(df_sample['latitude'][df_sample['id'].isin(selected_list)].values)
    lng = np.mean(df_sample['longitude'][df_sample['id'].isin(selected_list)].values)
    return {'lat':lat,'lng':lng}


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)
