import numpy as np
import pandas as pd
from recommender import Listingrecommender

class RecommenderSystem(object):
    def __init__(self,df_sample,df_reviews):
        """
        INPUT:
        -df_sample: sample listing data set
        -df_reviews:neighborhood reviews data set

        ATTRIBUTES:
        - df_select:selected listings based on number of minimum bedroom.
                    number of minimum bathroom, property type, neighborhood
                    and maximum price
        - recommender_dictionary: recomended listings;
                               keys=neighborhood, values=listing id
        - class_freq: the frequency of each class in the data
        - p: the number of features
        """
        self.df_sample = df_sample
        self.df_reviews = df_reviews
        self.df_select = None

        self.recommender_dictionary={}

#        self.listings = None
        self.alt_neig_1 = None
        self.alt_neig_2 = None

        self.minbed = None
        self.minbath = None
        self.proptype = None
        self.neighborhood = None
        self.maxprice = None

        nrec = Listingrecommender(self.df_reviews)
        self.neighborhood_dict = nrec.top_three_dictionary(df_reviews['reviews'].values,
                                                      df_reviews['name'].values,
                                                      postagged = True)

    def input_func(self,minbed, minbath, proptype, neighborhood, maxprice):
        '''
        INPUT
        -minbed: int
        -minbath: int
        -proptype : string
        -neighborhood: string
        -maxprice: int


        OUTPUT:
        -similatiry_dict : list of int (matching listing ids)
        '''
        self.minbed = minbed
        self.minbath = minbath
        self.proptype = proptype
        self.neighborhood = neighborhood
        self.maxprice = maxprice
        self.user_select(self.neighborhood)

        if self.df_select.shape[0] == 0:
            print 'Sorry, no match found. Please change your search options and try again :)'
        else :
            return self.df_select['id'].values.tolist()

    def user_select(self, neighborhood_):
        '''
        INPUT
        -neighborhood_: string

        OUTPUT:
        NONE
        '''

        self.df_select = self.df_sample[(self.df_sample['bed']>=self.minbed) &
                                  (self.df_sample['bed']>=self.minbath) &
                                  (self.df_sample['proptype']==self.proptype)&
                                  (self.df_sample['street_neighborhood']==neighborhood_)&
                                  (self.df_sample['price']<=self.maxprice)]\
                                  [['id','remarks']]

        self.df_select.reset_index(drop=True,inplace=True)


## IF ONE
    def if_one(self):
        '''
        INPUT: NONE
        OUTPUT: NONE
        (updates the recommender_dictionary with an empty list if there is only
        one listing available in the alternative neighborhood)
        '''
        self.recommender_dictionary[self.df_select['id'].values[0]]=[]

## IF TWO OR THREE
    def if_less_than_three(self):
        '''
        INPUT: NONE
        OUTPUT: NONE
        (updates the recommender_dictionary with one or two listings if there is
        only two three available listings in the alternative neighborhood)
        '''
        for i in range(self.df_select.shape[0]):
            self.recommender_dictionary[self.df_select['id'].values[i]]\
                            = np.setdiff1d(self.df_select['id'].values,
                              self.df_select['id'].values[i]).tolist()
# IF THREE
    def if_more_than_three(self,alt_,alt_id_):
        '''
        INPUT:
        -alt_ :  TRUE if it is an alternative neighborhood
        -altid_: the id of the selected listing in the alternative neighborhood
        OUTPUT: NONE
        (updates the recommender_dictionary with two other similar listings in
        the alternative neighborhood)
        '''
        rec=Listingrecommender(self.df_sample)
        self.recommender_dictionary\
                = rec.top_three_dictionary(self.df_select['remarks'].values,
                                           self.df_select['id'].values,
                                           alt=alt_,
                                           alt_id=alt_id_)


## PART I - User Input
    def same_neighborhood_recommender(self,alt_=False, alt_id_=None):
        self.user_select(self.neighborhood)

        if self.df_select.shape[0]==1:
            self.if_one()
        elif self.df_select.shape[0]<=3:
            self.if_less_than_three()
        else :
            self.if_more_than_three(alt_,alt_id_)

    def alt_neighborhood_recommender(self,neighborhood_,alt_=False, alt_id_=None):

        self.user_select(neighborhood_)
        if self.df_select.shape[0]==0:
            self.recommender_dictionary[alt_id_]=[]
        elif self.df_select.shape[0]<=2:
            self.recommender_dictionary[alt_id_]= self.df_select['id'].values.tolist()
        else :
            self.if_more_than_three(alt_,alt_id_)

## PART II Recomend other listings based on the selected one
    def listing_recommender(self,selected_listing):
        #update the neighborhood
        self.neighborhood = self.df_sample['street_neighborhood']\
                           [self.df_sample['id']==selected_listing].values[0]

        self.result_dict={}
        self.alt_neig_1, self.alt_neig_2 = self.neighborhood_dict[self.neighborhood]

        for n in [self.neighborhood, self.alt_neig_1, self.alt_neig_2 ]:
            if n == self.neighborhood :
                self.same_neighborhood_recommender(alt_=False, alt_id_=None)
                if len(self.recommender_dictionary[selected_listing])!=0:
                    self.result_dict[n] = self.recommender_dictionary[selected_listing]

            else:
                self.alt_neighborhood_recommender(neighborhood_=n,
                                                  alt_=True,
                                                  alt_id_=selected_listing)
                if len(self.recommender_dictionary[selected_listing])!=0:
                    self.result_dict[n] = self.recommender_dictionary[selected_listing]

        resultlist = [item for sublist in self.result_dict.values() for item in sublist]
        resultlist.insert(0,selected_listing)
        return resultlist
