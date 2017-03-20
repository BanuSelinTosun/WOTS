import numpy as np
import pandas as pd
from reccomender import ListingReccomender

class ReccomnderSystem(object):
    def __init__(self,df_sample):
        self.df_sample = df_sample
        self.df_select = None

        self.reccomender_dictionary = None

        self.minbed = None
        self.maxbed = None
        self.minbath = None
        self.maxbath = None
        self.prop_type = None
        self.neighborhood = None


    def user_select(self, minbed, maxbed, minbath, maxbath, prop_type, neighborhood):
        self.minbed, self.maxbed = sorted([minbed,maxbed])
        self.minbath, self.maxbath = sorted([minbath,maxbath])
        self.prop_type = prop_type
        self.neighborhood = neighborhood

        self.df_select = self.df_sample[(self.df_sample['bed']<=self.maxbed) &
                                  (self.df_sample['bed']>=self.minbed) &
                                  (self.df_sample['bath']<=self.maxbath) &
                                  (self.df_sample['bed']>=self.minbath) &
                                  (self.df_sample['prop_type']==self.prop_type)&
                                  (self.df_sample['street_neighborhood']==self.neighborhood)]\
                                  [['id','remarks']]

        self.df_select.reset_index(drop=True,inplace=True)


    def home_reccomender_dict(self, minbed, maxbed, minbath, maxbath, prop_type,
                              neighborhood, alt=False, alt_id=None):
        ## user selection data frame df_select
        self.user_select(minbed,maxbed,minbath,maxbath,prop_type,neighborhood)

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
        else:

            self.df_select.reset_index(drop=True,inplace=True)

            rec=ListingReccomender(self.df_sample)
            self.reccomender_dictionary\
                    = rec.top_three_dictionary(self.df_select['remarks'].values,
                                               self.df_select['id'].values,
                                               alt=alt,
                                               alt_id=alt_id)
        return self.reccomender_dictionary
