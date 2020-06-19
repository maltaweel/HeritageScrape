'''
Created on Jun 18, 2020

@author: mark
'''
import os
from os import listdir
import collections
from collections import Counter
from nltk.tokenize import word_tokenize 

import csv

from afinn import Afinn
from sklearn.metrics.cluster.tests.test_supervised import score_funcs


class Sentiment:
    afinn = Afinn()
    def get_affinity_score(self, tweet):
        
        score=0
        
        if len(tweet)>0:
            score=self.afinn.score(tweet) / len(tweet)
            return score
        else:
            return score
            
   
   
    def loadData(self):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        directory=os.path.join(pn,'modified')
        output_directory=os.path.join(pn,'sentiment')

        try:
            for f in listdir(directory):
                rows=[]
                
                if '.csv' not in f:
                    continue
                
                i=0
                texts=[]
                with open(os.path.join(directory,f),'r') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    for row in reader:
                        text=row['Text']
                        score=self.get_affinity_score(text)
                        
                        row['Score']=score
                        
                        rows.append(row)
                        
                        twords=word_tokenize(text)
                        for tt in twords:
                            texts.append(tt)
                
                word_counts = Counter(texts)
                
                t=word_counts.most_common(10)
                
                self.most_common_output(t,os.path.join(output_directory,'common_ten'+"_"+f))
                fle=os.path.join(output_directory,'sentiment'+"_"+f)       
                self.output(rows,fle)
                
        except IOError:
            print ("Could not read file:", csvfile)
    
    def most_common_output(self,t,fileOutput):
        
        fieldnames=[]
        
        output={}
        for l, d in t:
            fieldnames.append(l)
            output[l]=d
           
            
        
        with open(fileOutput, 'wt') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
            writer.writerow(output)
           
        
    def output(self,data,fileOutput):
        fieldnames = ['Datetime','ID','Score','Link','Text','Username','Retweets','Hashtags','Geolocation']
        with open(fileOutput, 'wt') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
        
            for f in data:
                writer.writerow({'Datetime': str(f['Datetime']),
                             'ID':str(f['ID']),'Score':str(f['Score']),'Link':str(f['Link']),
                             'Text':str(f['Text']),'Username':str(f['Username']),'Retweets':str(f['Retweets']),'Hashtags':str(f['Hashtags']),
                              'Geolocation':str(f['Geolocation'])})
    
    def run(self):
        self.loadData()
        print('Finished')

if __name__ == '__main__':
    s=Sentiment()
    s.run()