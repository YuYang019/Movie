from surprise import Dataset
from surprise import Reader
from surprise.model_selection  import train_test_split
import pandas as pd

class CFData:
  def __init__(self, df_rating, test_ratio=0.2, df_id_name_table=None, test=False):
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(df_rating, reader)
    self.data = data
    
    if test:
      self.trainset, self.testset = train_test_split(data=data, test_size=test_ratio)
    else:
      self.trainset = data.build_full_trainset()

    if df_id_name_table is not None:
      # 建立字典map
      self.__dict_id_to_name = df_id_name_table.groupby('movieId')['title'].apply(lambda x: x.tolist()).to_dict()
      self.__dict_name_to_id = df_id_name_table.groupby('title')['movieId'].apply(lambda x: x.tolist()).to_dict()

  def convert_name_to_id(self, item_name):
    # 从字典里查找电影名对应的id
    if (item_name not in self.__dict_name_to_id or len(self.__dict_name_to_id[item_name]) > 1):
      return None
    return self.__dict_name_to_id[item_name][0]
  
  def convert_id_to_name(self, item_id):
    # 从字典里查找电影id对应的名称
    if (item_id not in self.__dict_id_to_name or len(self.__dict_id_to_name[item_id]) > 1):
      return None
    return self.__dict_id_to_name[item_id][0]
