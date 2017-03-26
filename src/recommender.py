import pandas as pd
import numpy as np
import string
#NLP
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import pos_tag

class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        stemmer_porter = SnowballStemmer('english')
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: [stemmer_porter.stem(word) for word in analyzer(doc)]

class TextCleaning(object):

    def _fix_abrv(self,text_):
        '''
        INPUT:
        - text_: string

        OUTPUT: string

        Fix the abbrivations.
        '''
        return (text_.replace('\\n','')
                         .replace(' ba ',' bathroom ')
                         .replace(' bdrm ', ' bedroom ')
                         .replace(' br ', ' bedroom ')
                         .replace(' appls ', ' appliances ')
                         .replace(' appls ', ' appliances ')
                         .replace(' bdr ', ' bedroom ')
                         .replace(' flrs ', ' floors ')
                         .replace(' flr ', ' floor '))

    def _post_tag_nouns_adj(self,text_):
        '''
        INPUT:
        - text_: string
        OUTPUT: string, adjactives and nouns only

        Apply post_tag and return adjactves and nouns only
        '''
        return ' '.join([t[0] for t in pos_tag(text_.split())if t[1].startswith(('JJ','NN'))])

    def _remove_punctuations(self,text_):
        '''
        INPUT:
        - text_: string
        OUTPUT: string

        Removes punctuations
        '''
        punctuations_=set(string.punctuation)
        return ''.join(word for word in text_ if word not in punctuations_)

    def _remove_digits(self,text_):
        '''
        INPUT:
        - text_: string
        OUTPUT: string

        Removes digits
        '''
        return ' '.join(s for s in text_.split() if not any(c.isdigit() for c in s))

    def clean_text(self,text_list,post_tagged=False):
        '''
        INPUT:
        - text_list: list of numpy array strings
        OUTPUT: list of  numpy array strings

        Fix abbrivations, Remove punctuations,
        If post_tagged = True apply post_tagged and return Adj and Nouns only
        If post_tagged = False remove digits and return list of strings
        '''
        cleaned_text_list=[]
        for i in range(len(text_list)):
            review_fixed = self._fix_abrv(text_list[i])
            review_no_punc = self._remove_punctuations(review_fixed)
            if post_tagged==True:
                cleaned_text_list.append(self._post_tag_nouns_adj(review_no_punc))
            else:
                cleaned_text_list.append(self._remove_digits(review_no_punc))
        return cleaned_text_list


class Listingrecommender(object):
    def __init__(self,df_sample, combine_stopwords=True):
        self.df_sample = df_sample
        self.stopwords_= set(stopwords.words('english'))
        self.seattle_stopwords = [u'1st', u'2nd', u'3rd', u'alki', u'anne',
               u'arbor', u'area', u'atlantic', u'baker',
               u'ballard', u'bay', u'beach', u'beacon',
               u'belltown', u'bitter',
               u'blaine', u'blue', u'broadview', u'broadway', u'bryant',
               u'business', u'capitol', u'cedar', u'central', u'city', u'columbia',
               u'delridge', u'denny', u'district', u'downtown',
               u'east', u'eastlake', u'fairmount', u'fauntleroy', u'floor',
               u'floors', u'fremont', u'gatewood', u'genesee', u'georgetown',
               u'green', u'greenwood', u'haller', u'harrison', u'heights', u'high',
               u'highland', u'hill', u'hills', u'house', u'housing',
               u'interbay', u'international', u'lake', u'laurelhurst', u'leschi',
               u'licton', u'lower', u'madison', u'madrona', u'magnolia', u'mann',
               u'market', u'meadowbrook', u'minor', u'montlake', u'mount',
               u'neighborhood', u'north', u'northgate', u'olympic', u'park',
               u'phinney', u'pike', u'pioneer', u'point', u'portage', u'queen',
               u'rainier', u'ravenna', u'ridge', u'riverview', u'roxhill', u'sand',
               u'seattleadmiral', u'seaview', u'seward', u'south', u'springs',
               u'square', u'stevens', u'sunset', u'terrace', u'union',
               u'university', u'victory', u'wallingford', u'wedgeview', u'west',
               u'westlake', u'whittier', u'yesler']
        if combine_stopwords:
            self._add_stopwords()

    def _add_stopwords (self):
        '''
        INPUT: None

        OUTPUT: None

        add custom stop words).
        '''
        for word in self.seattle_stopwords:
            self.stopwords_.add(word)

    def top_three_dictionary(self, text_list,label_list, posttagged=False,
                            ngrammin=2, ngrammax=2, alt=False, alt_id=None):

        ## check if it is an alternative neighborhood
        if alt == True:
            alt_text = self.df_sample[self.df_sample['id']==alt_id]['remarks'].values
            text_list = np.append(text_list,alt_text)
            label_list = np.append(label_list,alt_id)


        ## get cleaned textreview
        cleaner=TextCleaning()
        textreview = cleaner.clean_text(text_list,post_tagged=posttagged)

        ## stemmed vectorizer
        Stemmed_Vectorizer=StemmedTfidfVectorizer(stop_words=self.stopwords_,
                                                  ngram_range=(ngrammin, ngrammin))
        Stemmed_Vectors=Stemmed_Vectorizer.fit_transform(textreview)
        Stemmed_Review_Vectors=Stemmed_Vectors.toarray()

        ## find 3 most similar items
        n=3
        similatiry_dict={}
        for i in range(len(label_list)):
            cos_sim = cosine_similarity(Stemmed_Review_Vectors[i:(i+1)], Stemmed_Review_Vectors)
            order = list(cos_sim.argsort()[0][::-1][1:n])
            top_three = label_list[order]
            similatiry_dict[label_list[i]]=top_three.tolist()

        return similatiry_dict
