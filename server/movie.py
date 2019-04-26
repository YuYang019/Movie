#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import random
import time
from concurrent import futures
from surprise import SVD, KNNBaseline

from CF.CFModel import CFModel
from CF.CFData import CFData
from CF.CFMovieSystem import CFMovieSystem, is_number
from CF.TMDBPoster import TMDBPoster

_df_movie = pd.read_csv('./data/movies.csv')
_df_rating = pd.read_csv('./data/ratings.csv')
# movieId imdbId tmdbId
_df_links = pd.read_csv('./data/links.csv')

_df_data = _df_rating[['userId', 'movieId', 'rating']]
_df_id_name_table = _df_movie[['movieId', 'title']]

# 初始化cf系统
def _init_system(model='svd'):
  data_movie = CFData(_df_data, df_id_name_table=_df_id_name_table)

  if model == 'svd':
    Model = SVD
  elif model == 'knn':
    Model = KNNBaseline
    
  model = CFModel(Model)
  model.fit(data_movie.trainset)
  model.test(data_movie.data)
  cf_system = CFMovieSystem(model, data_movie)

  return cf_system

# 获取排序后的评分次数大于阈值的所有电影
def _get_sorted_rating_count(threshold=30):
  movie_data = _df_data.merge(_df_id_name_table, on='movieId')
  rating_count = pd.DataFrame(movie_data.groupby(['movieId', 'title'])['rating'].mean())
  rating_count['count'] = pd.DataFrame(movie_data.groupby(['movieId', 'title'])['rating'].count())
  rating_count = rating_count[rating_count['count'] > threshold].sort_values(by='count', ascending=False)
  return rating_count

def _get_imdb_id(movie_id):
  return _df_links[_df_links['movieId']==movie_id].iloc[0]['imdbId']

def _get_tmdb_id(movie_id):
  return _df_links[_df_links['movieId']==movie_id].iloc[0]['tmdbId']

class MovieSystem:
  def __init__(self):
    self.system = _init_system()
    self.rating_count = _get_sorted_rating_count()
    self.tmbd_poster = TMDBPoster()

  def predict(self, name_or_id, k=5):
    return self.system.get_recommended_movies(name_or_id, k)
  
  def get_movie_detail(self, name_or_id):
    if is_number(name_or_id):
      movie_id = int(name_or_id)
    else:
      movie_id = self.system.cf_data.convert_name_to_id(name_or_id)
  
    tmdb_id = _get_tmdb_id(movie_id)
    movie_detail = self.tmbd_poster.get_movie_detail(tmdb_id)

    # 找不到资源
    if 'status_code' in movie_detail:
      if movie_detail['status_code'] == 34:
        return {
          'id': int(movie_id),
          'poster_url': '',
          'detail': {
            'title': name_or_id
          }
        }
    
    dict = {}
    dict['id'] = int(movie_id)
    dict['detail'] = movie_detail
    if 'poster_path' in movie_detail:
      dict['poster_url'] = self.tmbd_poster.get_poster_url(movie_detail['poster_path'])
    else:
      dict['poster_url'] = ''

    return dict

  def get_random_movies(self, k=15):
    rating_count = self.rating_count
    rows_num = rating_count.shape[0]
    res = []
    # 从n行里随机取k个
    # or use pandas.DataFrame.sample(n)
    selected_rows = random.sample(range(rows_num - 1), k)

    print('get random movie')

    start = time.time()

    # 多线程请求
    executor = futures.ThreadPoolExecutor(k)
    for i in selected_rows:
      row = rating_count.iloc[i]
      id = row.name[0]
      detail = executor.submit(self.get_movie_detail, id)
      res.append(detail)
    futures.wait(res)
    print('time: ', time.time() - start)
    res = [ r.result() for r in res]

    executor.shutdown()  # 销毁

    return res
  
  def _test(self):
    _movie_name = 'Forrest Gump (1994)'
    print(self.predict(_movie_name))


if __name__ == '__main__':
  system = MovieSystem()
  system._test()
    