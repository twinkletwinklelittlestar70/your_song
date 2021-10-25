"""
    Single instance to store all recommend list
"""
import pandas as pd
import pickle
import random

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
        # Load the origin table
        self.origin_data = pd.read_csv("./data/genres_v2.csv", encoding='utf-8', quotechar='"')
    
        pass
    
    def get_list_by_genre (self, genre, artist_list, number=10):
        print('Recommendation by genre', genre)
        genre_map = {"undergroundrap":0, "darktrap":1, "hiphop":2, "trance":3, "trap":4, "techhouse":5, "dnb":6, "psytrance": 7, "techno":8, "hardstyle":9, "rnb":10, "trapmetal":11, "rap":12, "emo":13, "pop":14}
        df = pd.DataFrame(self.core)
        genre = genre.lower().replace(' ', '')

        df_mask = df['genre'] == genre_map[genre]
        filtered_df = df[df_mask] # 从core中过滤出指定风格的歌

        id_list = filtered_df.index.values.tolist()
        random_id_list = random.sample(id_list, number)
        recomment_list = self.get_data_by_name_list(id_list=random_id_list)

        print('recommend list:', recomment_list)
        return recomment_list
    
    def get_list_by_song (self, song_id, number=10):
        nmf_features = self.nmf_features
        song_name = self.song_name # name list of songs
        name = song_name.values.tolist()[song_id][0]
        print('Recommendation by song', name, ' id=', song_id)

        current_music = nmf_features[song_id,:]
        similarities = nmf_features.dot(current_music)

        df = pd.DataFrame(nmf_features)
        x = df.join(song_name)
        df = pd.pivot_table(x, x[[0,1,2,3,4,5]],["Song-Names"]) # for indexing song_name to our df

        # print("Top 10 recommendations for given music are:", df)
        value = df.loc[name]
        similarities = df.dot(value)
        name_list = similarities.nlargest(number).index.values.tolist() # 取出前n个匹配歌的行索引，即为歌名
        recomment_list = self.get_data_by_name_list(name_list=name_list)
        print('recommend list:', recomment_list)
        return recomment_list
    
    def get_data_by_name_list (self, name_list=[], id_list=[]):
        '''
            从歌名映射到需要返回的数据结构 歌名+歌手+链接
        '''
        
        df = pd.DataFrame(self.origin_data)
        print('shape', df.shape)
        return_list = []

        if len(id_list) > 0:
            for item in id_list:
                if item < 2: # 防止越界访问
                    print('Warning: Error id for origin_data', item)
                    item = 2
                index = item - 2 # cvs中第一行数据是从index=2开始
                uri = df.at[index, 'uri']
                url = 'https://open.spotify.com' + uri.split(':')[1].replace(':', '/')# https://open.spotify.com/track/2Vc6NJ9PW9gD9q343XFRKx
                name = df.at[index, 'song_name']
                genre = df.at[index, 'genre']
                mode = df.at[index, 'mode']
                artists = ['Unkown']
                return_list.append({
                    "name": name,
                    "uri": uri,
                    "url": url,
                    "artists": artists,
                    "id": index,
                    "genre": genre,
                    "mode": mode,
                })
        elif len(name_list) > 0:
            for name in name_list:
                filtered_row = df[df['song_name'] == name] # 匹配歌曲行
                index = filtered_row.index.values.tolist()[0] # 访问原始数据的行索引，这里默认歌曲不会重名。直接取过滤后第一首。
                uri = filtered_row.at[index, 'uri'] # spotify:track:2vc6nj9pw9gd9q343xfrkx
                url = 'https://open.spotify.com' + uri.split(':')[1].replace(':', '/')# https://open.spotify.com/track/2Vc6NJ9PW9gD9q343XFRKx
                genre = filtered_row.at[index, 'genre']
                mode = filtered_row.at[index, 'mode']
                artists = ['Unkown']
                return_list.append({
                    "name": name,
                    "uri": uri,
                    "url": url,
                    "artists": artists,
                    "id": index,
                    "genre": genre,
                    "mode": mode,
                })
        else:
            print('Warning: No paramters when calling get_data_by_name_list.', name_list, id_list)

        return return_list

rec_engine = RecEngine()