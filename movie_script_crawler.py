import requests
from bs4 import BeautifulSoup
import random
import shutil
import os


class MovieScriptCrawler:
    URL = 'https://www.imsdb.com/'
    NUM_PER_GENRE = 10
    SAVE_PATH = 'scripts'
    GENRES = [
        'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama',
        'Family', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
        'Romance', 'Sci-Fi', 'Short', 'Thriller', 'War', 'Western',
    ]

    def get_movies_by_genre(self, genre):
        url = self.URL + 'genre/{genre}'.format(genre=genre)
        html = requests.get(url).text
        bs = BeautifulSoup(html, 'html5lib')

        movies = []
        for a_tag in bs.find_all('a'):
            title = a_tag.get('title')
            if title and title != 'The Internet Movie Script Database':
                movies.append(a_tag.text)
        return movies

    def get_script(self, movie):
        url = self.URL + 'scripts/{}.html'.format(movie.replace(' ', '-'))
        html = requests.get(url).text
        bs = BeautifulSoup(html, 'html5lib')

        for pre in bs.find_all('pre'):
            if 'FADE' in pre.text:
                return pre.text

        raise Exception

    def save_script(self, path, script):
        file = open(self.SAVE_PATH + path, 'w')
        file.write(script)
        file.close()

    def clean(self):
        try:
            shutil.rmtree(self.SAVE_PATH)
        except Exception:
            pass

    def run(self):
        self.clean()
        os.mkdir(self.SAVE_PATH)
        for genre in self.GENRES:
            os.mkdir(self.SAVE_PATH + '/{}'.format(genre))
            movies = self.get_movies_by_genre(genre)
            random.shuffle(movies)
            count = 0
            print(genre)
            for movie in movies:
                try:
                    script = self.get_script(movie)
                    self.save_script('/{}/{}.txt'.format(genre, movie), script)
                except Exception:
                    continue
                print('    -' + movie)
                count += 1
                if count >= self.NUM_PER_GENRE:
                    break


if __name__ == '__main__':
    MovieScriptCrawler().run()
