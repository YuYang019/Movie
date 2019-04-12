def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    pass 

  return False

class CFMovieSystem:
  def __init__(self, cf_model, cf_data):
    self.cf_model = cf_model
    self.cf_data = cf_data
  
  def get_recommended_movies(self, name_or_id, k=10):
    if is_number(name_or_id):
      movie_id = int(name_or_id)
    else:
      movie_id = self.cf_data.convert_name_to_id(name_or_id)

    movie_neighbor_name = [self.cf_data.convert_id_to_name(id) for id in self.cf_model.get_similar_item(movie_id, k)]
    movie_neighbor_id = [self.cf_data.convert_name_to_id(name) for name in movie_neighbor_name]

    return movie_neighbor_name
