import requests

class TMDBPoster:
  def __init__(self):
      self.CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
      # see https://developers.themoviedb.org/3/movies/get-movie-images
      self.IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{tmdbid}/images?api_key={key}'
      self.MOVIE_DETAIL_PATTERN = 'https://api.themoviedb.org/3/movie/{tmdbid}?api_key={key}&language=zh-CN'
      self.KEY = '282533ba881379db7953301dee2ef238'
            
  def _get_json(self, url):
    r = requests.get(url)
    return r.json()
        
  def _download_images(self, urls, path='.', filename_prefix='poster'):
    
    for nr, url in enumerate(urls):
      r = requests.get(url)
      filetype = r.headers['content-type'].split('/')[-1]
      #filename = 'poster_{0}.{1}'.format(nr+1,filetype)
      filename = filename_prefix + '_{0}.{1}'.format(nr+1,filetype)
      filepath = os.path.join(path, filename)
      with open(filepath,'wb') as w:
        w.write(r.content)
  
  def get_movie_detail(self, tmdbid):
    detail = self._get_json(self.MOVIE_DETAIL_PATTERN.format(key=self.KEY, tmdbid=tmdbid))
    return detail

    
  def get_poster_url(self, file_path, size='w185'):
    # 通过 config api 取得 base_url 和 size
    # config = self._get_json(self.CONFIG_PATTERN.format(key=self.KEY))
    # base_url = config['images']['base_url']
    # sizes = config['images']['poster_sizes']
    base_url = 'http://image.tmdb.org/t/p/'
    poster_url = '{0}{1}{2}'.format(base_url, size, file_path)
    return poster_url
  
  def download_tmdb_posters(self, imdbid, count=None, outpath='.'):    
    urls = self.get_poster_urls(imdbid)
    if count is not None:
      urls = urls[:count]
    self._download_images(urls, outpath, imdbid)