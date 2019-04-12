import surprise as surp
from surprise.model_selection import cross_validate
import pandas as pd

class CFModel:
  def __init__(self, model, *args, **kwargs):
    self.model = model(*args, **kwargs)
  
  def fit(self, data_train):
    self.model.fit(data_train)

  def test(self, data):
    cross_validate(self.model, data, measures=['RMSE'], cv=5, verbose=True)
  
  def get_similar_item(self, item_id, n_neighbor):
    # 调用model自带方法，将movieId转换成model内部id
    input_inner_id = self.model.trainset.to_inner_iid(item_id)

    # 如果model为KNN，会带有get_neighbors方法
    # 如果是SVD，就没有这个方法，调用自己写的方法
    if 'sim' in dir(self.model):
      neighbor_inner_id = self.model.get_neighbors(input_inner_id, k=n_neighbor)
      # 遍历neighbors，将内部id再转回为movieId，返回
      return [self.model.trainset.to_raw_iid(inner_id) for inner_id in neighbor_inner_id]
    else:
      return self.__get_top_similarities(input_inner_id, n_neighbor)

  def __get_top_similarities(self, item_inner_id, k):
    # 矩阵分解模型，获取top-k相似item
    # from sklearn.metrics.pairwise import cosine_similarity
    from math import sqrt

    # 欧氏距离？计算两电影的隐特征向量的距离
    def cosine_distance(vector_a, vector_b):
      ab = sum([i*j for (i, j) in zip(vector_a, vector_b)])
      a2 = sum([i*i for i in vector_a])
      b2 = sum([i*i for i in vector_b])
      eta = 1./10**9
      return 1.0 - ab/sqrt((a2+eta)*(b2+eta))

    item_vector = self.model.qi[item_inner_id]
    similarity_table = []

    for other_inner_id in self.model.trainset.all_items():
      if other_inner_id == item_inner_id:
        continue
      # 获取其他movie的向量
      other_inner_vector = self.model.qi[other_inner_id]
      # 计算相似度
      similarity_table.append((
        cosine_distance(other_inner_vector, item_vector),
        self.model.trainset.to_raw_iid(other_inner_id)
      ))
    
    # 升序
    similarity_table.sort()

    if k > len(similarity_table):
      return [i[1] for i in similarity_table]
    else:
      return [i[1] for i in similarity_table[0:k]]

