from flask import Flask
from flask import request
from flask import jsonify
import random
from movie import MovieSystem

app = Flask(__name__)

movie_system = MovieSystem()

@app.route('/')
def hello_world():
  return 'Hello World!'

# 默认处理get请求
@app.route('/movies')
def get_movies():
  data = movie_system.get_random_movies()
  return jsonify(data)

'''
  id: rating
  {
    '1231': 4.5,
    '3212': 5.0,
    '2731': 1.0,
    '9211': 3.5,
  }
'''
@app.route('/recommend', methods=['POST'])
def recommend_movies():
  
  def get_top_list(data, k):
    high = []
    equal = []
    low = []
    list = []
    mean = 0

    for id in data:
      mean += data[id]
      list.append((id, data[id]))
    mean = mean / len(list)

    high_num = 0
    equal_num = 0
    low_num = 0
    for movie in list:
      if movie[1] > mean:
        high.append(movie)
        high_num += 1
      elif movie[1] == mean:
        equal.append(movie)
        equal_num += 1
      else:
        low.append(movie)
        low_num += 1
    
    result = []
    if (high_num >= k):
      return high
    else:
      result += high
      # 剩余个数
      surplus = k - high_num
      if (equal_num >= surplus):
        # 如果与平均数相同评分电影个数 >= 剩余个数，剩下的就从这里面随机取
        result += random.sample(equal, surplus)
        return result
      else:
        # 否则，先取完equal，再取low
        result += equal
        surplus = surplus - equal_num
        # 对剩下的low进行排序，取完
        low.sort(key=lambda x: x[1], reverse=True)
        result += low[:surplus]
        return result

  def checkMovies(movies, all_movies):
    for movie in movies:
      if movie in all_movies:
        return True
    return False
  
  # 从前往后取电影，而不是随机
  def get_movies(similar_movies, all_movies, num):
    result = []
    index = 0
    while num > 0:
      movie = similar_movies[index]
      if movie in all_movies:
        index += 1
      else:
        result.append(movie)
        num -= 1
        index += 1
    return result

  data = request.get_json(request.data)
  top_list = get_top_list(data, 5)
  top_list.sort(key=lambda x: x[1], reverse=True)

  print(top_list)
  print('begin')

  all_movies = []
  if len(top_list) > 10:
    top_list = top_list[:10]
    for movie in top_list:
      id = movie[0]
      similar_movies = movie_system.predict(id, k=10)
      temp = get_movies(similar_movies, all_movies, 1)
      all_movies += temp
  elif len(top_list) > 5:
    surplus = 10 - len(top_list)
    for index in range(len(top_list)):
      movie = top_list[index]
      id = movie[0]
      similar_movies = movie_system.predict(id, k=10)
      # 基本思想是，每个先取1个，剩下的从头取
      # 由于总数为10个，且top_list长度 > 5，这个问题可以转换成，每个要么取1个，要么取2个
      # 那么肯定是排在前面的取2个，后面的取1个，排在前面多少呢，就是surplus
      if index < surplus:
        temp = get_movies(similar_movies, all_movies, 2)
      else:
        temp = get_movies(similar_movies, all_movies, 1)
      all_movies += temp
  elif len(top_list) == 5:
    for movie in top_list:
      id = movie[0]
      similar_movies = movie_system.predict(id, k=10)
      temp = get_movies(similar_movies, all_movies, 2)
      all_movies += temp
  
  print(all_movies)

  res = []
  for movie_name in all_movies:
    detail = movie_system.get_movie_detail(movie_name)
    res.append(detail)

  return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)