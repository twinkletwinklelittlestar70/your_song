"""
    Single instance to store all music data
"""

import pandas as pd
import pickle
import random
from anytree import Node, RenderTree
import time

class RecEngine():
    ''' Recommend music to users from our music list.'''
  
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
        # Load the artist, song name and genre table
        with open("./data/artist_pickle.dat", "rb") as f:
            self.name_artist_genre = pickle.load(f)
        # Load the origin table
        self.origin_data = pd.read_csv("./data/genres_v3.csv", encoding='utf-8', quotechar='"')
    
        pass
    
    def get_list_by_genre (self, genre, artist_list=[], number=10):
        '''
            get_list_by_genre   根据音乐风格获取推荐列表。
            @genre{str} 风格；
            @artist_list{[str]} 歌手列表; 优先返回列表中歌手的相似歌曲；
            @number{int} 推荐歌曲数
        '''
        print('Recommendation by genre', genre)
        genre_map = {"popular":0, "rock":1, "folk":2, "hiphop":3, "rnb":4, "jazz":5, "electronic":6, "classical": 7, "absolutemusic":8}
        
        df = pd.DataFrame(self.name_artist_genre)
        genre = genre.lower().replace(' ', '')

        df_mask = df['genre'] == genre_map[genre]
        filtered_df = df[df_mask] # 从core中过滤出指定风格的歌
        
        # 从风格中优先选择指定歌手
        MAX_NUM_OF_ARTIST = 3
        df_artist_mask = filtered_df['artist'].isin(artist_list)
        filtered_df_by_artist = filtered_df[df_artist_mask] # 相同风格中再过滤出指定歌手
        artist_id_list = filtered_df_by_artist.index.values.tolist()
        if len(artist_id_list) > MAX_NUM_OF_ARTIST: # 指定歌手总共取3个
            artist_random_list = random.sample(artist_id_list, MAX_NUM_OF_ARTIST)
        else:
            artist_random_list = artist_id_list
        
        print('len artist_random_list', len(artist_random_list))
        
        number = number - len(artist_random_list) # 减去歌手列表
        id_list = filtered_df.index.values.tolist()

        print('按风格获取的id_list, 范围是', len(id_list), id_list[0], '-', id_list[-1]) # core的index从0开始，origin_data的index从2开始
        random_id_list = random.sample(id_list, number)
        # [9172, 45, 6515, 6951, 7282, 7049, 6753, 6218, 6771, 6641]

        print('按歌手推荐的数量:', len(artist_random_list), ' 按随机推荐的数量', len(random_id_list))
        random_id_list = artist_random_list + random_id_list

        # random_id_list = list(map(lambda x: x+2 , random_id_list)) # id 转换成index，变成从2开始

        recomment_list = self._get_data_by_name_list(id_list=random_id_list)
        print('recommend list:', recomment_list)

        if len(recomment_list) == 0:
            print('Warning: No recommend data. Please check your paramters')

        return recomment_list

    
    def get_list_by_song (self, song_id=None, song_name='', number=10, mode=0):
        '''
            get_list_by_song   Recommend by song。
            @song_id{int} specify song id
            @song_name{str} specify song name; if id and name both sepecified, use song name in priosity.
            @number{int} The recommend list length
            @mode{bool} 1: Using greedy Search; 0: Top 10 base on similarities;
        '''

        if song_id is None and song_name == '':
            print('Warning: sond_id or song_name should be specify when calling get_list_by_song')
            return []
        
        # use name in priosity
        if len(song_name) > 0:
            data_list = self._get_data_by_name_list(name_list=[song_name])
            song_id = data_list[0]['id']
            print('Find the specific song', data_list[0])

        nmf_features = self.nmf_features
        song_name_list = self.song_name # name list of songs
        name = song_name_list.values.tolist()[song_id][0]
        print('Recommendation by song', name, ' id=', song_id)

        current_music = nmf_features[song_id,:]
        similarities = nmf_features.dot(current_music)

        df = pd.DataFrame(nmf_features)
        x = df.join(song_name_list)
        df = pd.pivot_table(x, x[[0,1,2,3,4,5]],["Song-Names"]) # for indexing song_name to our df

        if mode == 0: # Top 10 base on similarities
            value = df.loc[name] # name是歌名
            similarities = df.dot(value)
            top_similarities = similarities.nlargest(number)
            print("Top 10 recommendations for given music are:", top_similarities)
            name_list = top_similarities.index.values.tolist() # 取出前n个匹配歌的行索引，即为歌名
        else: # Using informed search
            self.df = df
            self.current_name = name
            # time1 = time.time()
            self.build_tree(height=number)
            # time2 = time.time()
            name_list = self._search_tree(self.root_node)
            # time3 = time.time()
            # print('Time cost building tree', time2 - time1, 'Time cost searching tree', time3 - time2)
        
        recomment_list = self._get_data_by_name_list(name_list=name_list)
        print('recommend list:', recomment_list)

        if len(recomment_list) == 0:
            print('Warning: No recommend data. Please check your paramters')
        return recomment_list
    
    def _get_data_by_name_list (self, name_list=[], id_list=[]):
        '''
            private function. To build the return data structure
            Map song name to other data like artist,link,mode...
            
            @id_list{list} 
            @name_list{list} 
        '''
        
        df = pd.DataFrame(self.origin_data)
        print('shape', df.shape)
        return_list = []

        if len(id_list) > 0:
            print('list id we found', id_list)
            for item in id_list:
                index = item
                uri = df.at[index, 'uri']
                url = 'https://open.spotify.com/' + uri.split(':')[1] + '/' + uri.split(':')[2]# https://open.spotify.com/track/2Vc6NJ9PW9gD9q343XFRKx
                name = df.at[index, 'song_name']
                genre = df.at[index, 'genre']
                mode = df.at[index, 'mode']
                artist = df.at[index, 'artist']
                return_list.append({
                    "name": name,
                    "uri": uri,
                    "url": url,
                    "artist": artist,
                    "id": index,
                    "genre": genre,
                    "mode": mode,
                })
        elif len(name_list) > 0:
            for name in name_list:
                filtered_row = df[df['song_name'] == name] # match song row
                match_list = filtered_row.index.values.tolist()
                if len(match_list) == 0:
                    print('Warning: Cannot find this song in our library', name)
                    continue
                index = match_list[0] # song name should not be duplicated. so get the first one in match list;
                uri = filtered_row.at[index, 'uri'] # spotify:track:2vc6nj9pw9gd9q343xfrkx
                url = 'https://open.spotify.com/' + uri.split(':')[1] + '/' + uri.split(':')[2]# https://open.spotify.com/track/2Vc6NJ9PW9gD9q343XFRKx
                genre = filtered_row.at[index, 'genre']
                mode = filtered_row.at[index, 'mode']
                artist = filtered_row.at[index, 'artist']
                return_list.append({
                    "name": name,
                    "uri": uri,
                    "url": url,
                    "artist": artist,
                    "id": index,
                    "genre": genre,
                    "mode": mode,
                })
        else:
            print('Warning: No paramters when calling get_data_by_name_list.', name_list, id_list)

        return return_list

    def _get_children_song (self, df, name, number=10):
        # print('Looking for similar songs', name)
        value = df.loc[name]
        similarities = df.dot(value)
        mylist = similarities.nlargest(number + 1)
        name_list = mylist.index.values.tolist()

        # delete the song itself
        if name in name_list:
            name_list.remove(name)
        
        # get similarity
        similarity_list = []
        for name in name_list:
            similarity_list.append(mylist[name])
        
        # print('result for search', name_list)
        return name_list, similarity_list
    
    def build_tree (self, height=5, node=None):
        TREE_HEIGHT = height # height of tree, also the number of recommand song
        SUB_NODE_NUMBER = 3 # Trinomial tree

        if node == None:
            node = Node(self.current_name) # Root node
            self.root_node = node

        if node.depth >= TREE_HEIGHT - 1: # 4
            # print(RenderTree(self.root_node))
            return

        name_list, similarity_list = self._get_children_song(self.df, node.name, number=TREE_HEIGHT)
        
        # filter ancestor name from name_list. 
        ancestors_list = list(node.ancestors)
        ancestors_name = list(map(lambda n: n.name, ancestors_list))
        
        # De-duplication. Remove name in the ancestors_list. 
        for name in ancestors_name:
            if name in name_list:
                name_list.remove(name)

        # build subnodes
        for index, song in enumerate(name_list[:SUB_NODE_NUMBER]):
            subnode = Node(song, sim=similarity_list[index], parent=node)
            self.build_tree(height=TREE_HEIGHT, node=subnode)
        
        return 
    
    def _search_tree (self, node):

        if node.is_leaf:
            return [node.name]
        
        # Find the node who has max sim value among children
        max_node = None
        max_similarity = 0
        for child in node.children:
            if child.sim > max_similarity:
                max_similarity = child.sim
                max_node = child

        return [max_node.name] + self._search_tree(max_node)
    

rec_engine = RecEngine()