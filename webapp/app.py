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
column_names = ['bed','bath','address','neighborhood','price'] # add remarks later maybe
recsys =S.ReccomnderSystem(df_sample,df_reviews)


app = Flask(__name__)

@app.route('/', methods =['GET'])
def index():
    return render_template('wos.html')

@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    minbed,maxbed,minbath,maxbath,proptype,neighborhood = (user_data['minbed'],
                                                          user_data['maxbed'],
                                                          user_data['minbath'],
                                                          user_data['maxbath'],
                                                          user_data['proptype'],
                                                          user_data['neighborhood'])

    return _return_selected(minbed,maxbed,minbath,maxbath,proptype,neighborhood)


def _return_selected(minbed,maxbed,minbath,maxbath,proptype,neighborhood):
    selected_list=recsys.input_func(minbed, maxbed, minbath, maxbath, proptype, neighborhood)
    if type(selected_list)==list:
        df = df_sample[df_sample['id'].isin(selected_list)][column_names]

        return jsonify(df.to_html(index=False, classes='table'))
    else:
        return "Sorry, no match found. Please change your search options and try again :)"


def _plot_table(df_sample,selected_list):
    df_plot = df_sample[df_sample['id'].isin(selected_list)]
    return dfs[['price','latitude','longitude']].values.tolist()

def _lat_lng(df_sample,selected_list):
    lat = np.mean(df_sample['latitude'][df_sample['id'].isin(selected_list)].values)
    lng = np.mean(df_sample['longitude'][df_sample['id'].isin(selected_list)].values)
    return (lat,lng)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)
