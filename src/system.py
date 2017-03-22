import numpy as np
import pandas as pd
from reccomender import ListingReccomender

class ReccomnderSystem(object):
    def __init__(self,df_sample,df_reviews):
        self.df_sample = df_sample
        self.df_reviews = df_reviews
        self.df_select = None

        self.reccomender_dictionary={}

        self.listings = None
        self.alt_neig_1 = None
        self.alt_neig_2 = None

        self.minbed = None
        self.maxbed = None
        self.minbath = None
        self.maxbath = None
        self.proptype = None

        self.neighborhood = None

        nrec = ListingReccomender(self.df_reviews)
        self.neighborhood_dict = nrec.top_three_dictionary(df_reviews['reviews'].values,
                                                      df_reviews['name'].values,
                                                      posttagged = True)

    def input_func(self,minbed, maxbed, minbath, maxbath, proptype, neighborhood):
        self.minbed, self.maxbed = sorted([minbed,maxbed])
        self.minbath, self.maxbath = sorted([minbath,maxbath])
        self.proptype = proptype
        self.neighborhood = neighborhood
        self.user_select(self.neighborhood)
        if self.df_select.shape[0] == 0:
            print 'Sorry, no match found. Please change your search options and try again :)'
        else :
            print self.df_select['id'].values.tolist()

    def user_select(self, neighborhood_):

        self.df_select = self.df_sample[(self.df_sample['bed']<=self.maxbed) &
                                  (self.df_sample['bed']>=self.minbed) &
                                  (self.df_sample['bath']<=self.maxbath) &
                                  (self.df_sample['bed']>=self.minbath) &
                                  (self.df_sample['proptype']==self.proptype)&
                                  (self.df_sample['street_neighborhood']==neighborhood_)]\
                                  [['id','remarks']]

        self.df_select.reset_index(drop=True,inplace=True)


## IF ONE
    def if_one(self):
        self.reccomender_dictionary[self.df_select['id'].values[0]]=[]

## IF TWO OR THREE
    def if_less_than_three(self):
        for i in range(self.df_select.shape[0]):
            self.reccomender_dictionary[self.df_select['id'].values[i]]\
                            = np.setdiff1d(self.df_select['id'].values,
                              self.df_select['id'].values[i]).tolist()
# IF THREE
    def if_more_than_three(self,alt_,alt_id_):
        rec=ListingReccomender(self.df_sample)
        self.reccomender_dictionary\
                = rec.top_three_dictionary(self.df_select['remarks'].values,
                                           self.df_select['id'].values,
                                           alt=alt_,
                                           alt_id=alt_id_)


## PART I - RETURN LISTINGS BASED ON USER'S SPECIFICATIONS
    def same_neighborhood_reccomender(self,alt_=False, alt_id_=None):

        self.user_select(self.neighborhood)

        if self.df_select.shape[0]==1:
            self.if_one()
        elif self.df_select.shape[0]<=3:
            self.if_less_than_three()
        else :
            self.if_more_than_three(alt_,alt_id_)

    def alt_neighborhood_reccomender(self,neighborhood_,alt_=False, alt_id_=None):

        self.user_select(neighborhood_)
        if self.df_select.shape[0]==0:
            self.reccomender_dictionary[alt_id_]=[]
        elif self.df_select.shape[0]<=2:
            self.reccomender_dictionary[alt_id_]= self.df_select['id'].values.tolist()
        else :
            self.if_more_than_three(alt_,alt_id_)

## PART II RETURN RECCOMENDED LISTINGS BASED ON USER'S SELECTIONS
    def listing_reccomender(self,selected_listing):
        self.result_dict={}
        self.alt_neig_1, self.alt_neig_2 = self.neighborhood_dict[self.neighborhood]

        for n in [self.neighborhood, self.alt_neig_1, self.alt_neig_2 ]:
            if n == self.neighborhood :
                self.same_neighborhood_reccomender(alt_=False, alt_id_=None)
                if len(self.reccomender_dictionary[selected_listing])!=0:
                    self.result_dict[n] = self.reccomender_dictionary[selected_listing]

            else:
                self.alt_neighborhood_reccomender(neighborhood_=n,
                                                  alt_=True,
                                                  alt_id_=selected_listing)
                if len(self.reccomender_dictionary[selected_listing])!=0:
                    self.result_dict[n] = self.reccomender_dictionary[selected_listing]
        print self.result_dict
