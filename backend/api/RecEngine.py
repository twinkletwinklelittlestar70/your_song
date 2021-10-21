"""
    Single instance to store all recommend list
"""
import pandas as pd
import pickle

class RecEngine():
    ''' Recommend music to users from our mucic list.'''
  
    def __init__(self):
        ''' Load the whole music list. And do the feature caculations.'''
        # Load the song name list
        with open("./data/name_pickle.dat", "rb") as f:
            self.song_name = pickle.load(f)
        # Load the core data list (origin features)
        with open("./data/core_pickle.dat", "rb") as f:
            self.core = pickle.load(f)
        # Load the nmf features list (normalized)
        with open("./data/nmf_pickle.dat", "rb") as f:
            self.nmf_features = pickle.load(f)
    
        pass
    
    def get_list_by_genre (self, genre, artist_list, number=10):
  
        return []
    
    def get_list_by_song (self, song_id, number=10):
        nmf_features = self.nmf_features
        song_name = self.song_name # name list of songs
        name = song_name.values.tolist()[song_id][0]
        print('current music name: ', name)

        current_music = nmf_features[song_id,:]
        similarities = nmf_features.dot(current_music)

        df = pd.DataFrame(nmf_features)
        x = df.join(song_name)
        df = pd.pivot_table(x, x[[0,1,2,3,4,5]],["Song-Names"]) # for indexing song_name to our df

        print("Top 10 recommendations for given music are:")
        value = df.loc[name]
        similarities = df.dot(value)
        mylist = similarities.nlargest(10)
        print(format(mylist))
        mylistName = mylist.index.values.tolist() # 取出行索引，即为歌名

        # TODO: 从歌名映射到 歌名+歌手+链接
        
        return mylistName

rec_engine = RecEngine()