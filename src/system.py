import numpy as np
import pandas as pd
from reccomender import ListingReccomender

class ReccomnderSystem(object):
    def __init__(self,df_sample,df_reviews):
        self.df_sample = df_sample
        self.df_reviews = df_reviews
        self.df_select = None

        self.reccomender_dictionary = None
        self.result_dict = None
        self.listings = None
        self.alt_neig_1 = None
        self.alt_neig_2 = None

        self.minbed = None
        self.maxbed = None
        self.minbath = None
        self.maxbath = None
        self.proptype = None
#       self.neighborhood = None

        nrec = ListingReccomender(self.df_reviews)
        self.neighborhood_dict = nrec.top_three_dictionary(df_reviews['reviews'].values,
                                                      df_reviews['name'].values,
                                                      posttagged = True)

    def user_select(self, minbed, maxbed, minbath, maxbath, proptype, neighborhood):
        self.minbed, self.maxbed = sorted([minbed,maxbed])
        self.minbath, self.maxbath = sorted([minbath,maxbath])
        self.proptype = proptype
#        self.neighborhood = neighborhood

        self.df_select = self.df_sample[(self.df_sample['bed']<=self.maxbed) &
                                  (self.df_sample['bed']>=self.minbed) &
                                  (self.df_sample['bath']<=self.maxbath) &
                                  (self.df_sample['bed']>=self.minbath) &
                                  (self.df_sample['proptype']==self.proptype)&
                                  (self.df_sample['street_neighborhood']==neighborhood)]\
                                  [['id','remarks']]

        self.df_select.reset_index(drop=True,inplace=True)

## PART I - RETURN LISTINGS BASED ON USER'S SPECIFICATIONS
    def home_reccomender_dict(self, minbed, maxbed, minbath, maxbath, proptype,
                              neighborhood, alt=False, alt_id=None):
        ## user selection data frame df_select
        self.user_select(minbed,maxbed,minbath,maxbath,proptype,neighborhood)

        ## check if there is any match
        if self.df_select.shape[0]==0:
            return 'Sorry, no match found. Please change your search options and try again :)'

        ## if there is only one return
        if self.df_select.shape[0]==1:
            return self.df_select

        ## check if there number of listing 2 or more
        elif self.df_select.shape[0]<=3:
            for i in range(self.df_select.shape[0]):
                self.reccomender_dictionary[self.df_select['id'].values[i]]\
                                = np.setdiff1d(self.df_select['id'].values,
                                  self.df_select['id'].values[i])
            self.listings = self.reccomender_dictionary.keys()
            return self.listings

        else:

            self.df_select.reset_index(drop=True,inplace=True)

            rec=ListingReccomender(self.df_sample)
            self.reccomender_dictionary\
                    = rec.top_three_dictionary(self.df_select['remarks'].values,
                                               self.df_select['id'].values,
                                               alt=alt,
                                               alt_id=alt_id)
            self.listings = self.reccomender_dictionary.keys()
            return self.listings

## PART II RETURN RECCOMENDED LISTINGS BASED ON USER'S SELECTIONS
    def listing_reccomender(self,selected_listing,neighborhood):

        _=self.home_reccomender_dict(self.minbed,
                                   self.maxbed,
                                   self.minbath,
                                   self.maxbath,
                                   self.proptype,
                                   neighborhood)
        self.result_dict={}
        self.selected_listing = selected_listing

        self.result_dict[neighborhood] = self.reccomender_dictionary[self.selected_listing]

        self.alt_neig_1, self.alt_neig_2 = self.neighborhood_dict[neighborhood]

        # alt_neig_1
        _= self.home_reccomender_dict(self.minbed,
                                      self.maxbed,
                                      self.minbath,
                                      self.maxbath,
                                      self.proptype,
                                      self.alt_neig_1,
                                      alt=True,
                                      alt_id=selected_listing)

        self.result_dict[self.alt_neig_1] = self.reccomender_dictionary.\
                                                    get(selected_listing,
                                                        'sorry, no match found')

        # alt_neig_2
        _= self.home_reccomender_dict(self.minbed,
                                      self.maxbed,
                                      self.minbath,
                                      self.maxbath,
                                      self.proptype,
                                      self.alt_neig_2,
                                      alt=True,
                                      alt_id=selected_listing)

        self.result_dict[self.alt_neig_2] = self.reccomender_dictionary.\
                                                    get(selected_listing,
                                                        'sorry, no match found')

        return self.result_dict
