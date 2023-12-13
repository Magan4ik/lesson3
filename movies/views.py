from django.shortcuts import render

from movies.facades import MovieFacade
from movies.parser_csv import MovieCSVReader
from movies.repositories import HumanDjangoORMRepository, GenreDjangoORMRepository, MovieDjangoORMRepository


# Create your views here.
def test(request):
    movie_facade = MovieFacade(
        human_repositoty=HumanDjangoORMRepository,
        genre_repository=GenreDjangoORMRepository,
        movie_repository=MovieDjangoORMRepository,
        movie_parser=MovieCSVReader(csv_name="movies.csv")
    )
    #movie_facade.create_movie()
    return render(request, "movies/movie_list.html")
