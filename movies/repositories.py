from typing import Optional

from movies.models import Human, Genre, Movie
from movies.parser_csv import HumanDTO, MovieDTO, MovieShortDTO

from django.forms.models import model_to_dict


class HumanDjangoORMRepository:

    @classmethod
    def get_human_by_full_name(cls, full_name: str):
        first_name, last_name = full_name.split(" ")
        human = Human.objects.filter(first_name=first_name, last_name=last_name).first()
        if not human:
            return None, None
        return cls._map_model_to_dto(human=human), human.pk

    @classmethod
    def _map_model_to_dto(cls, human: Human):
        return HumanDTO(
            first_name=human.first_name,
            last_name=human.last_name,
            profession=human.profession
        )

    @classmethod
    def create_human(cls, human_dto: HumanDTO) -> int:
        human = Human.objects.create(**human_dto._asdict())
        return human.pk


class GenreDjangoORMRepository:

    @classmethod
    def get_genre_by_name(cls, name: str) -> Optional[str]:
        genre = Genre.objects.filter(genre=name).first()
        if not genre:
            return None
        return genre.genre

    @classmethod
    def create_genre(cls, genre: str) -> str:
        gen = Genre.objects.create(genre=genre)
        return gen.genre


class MovieDjangoORMRepository:

    @classmethod
    def get_movie_by_name(cls, name: str) -> Optional[MovieDTO]:
        movie = Movie.objects.filter(name=name).first()
        if not movie:
            return None
        return cls._map_model_to_dto(movie=movie)

    @classmethod
    def _map_model_to_dto(cls, movie: Movie) -> MovieDTO:
        genre_list = list()
        for genre in movie.genres.all():
            genre_list.append(genre.genre)

        star_list = list()
        for star in movie.stars.all():
            human = HumanDTO(
                first_name=star.first_name,
                last_name=star.last_name,
                proffesion=star.proffesion
            )
            star_list.append(human)

        director_list = list()
        for director in movie.director.all():
            human = HumanDTO(
                first_name=director.first_name,
                last_name=director.last_name,
                proffesion=director.proffesion
            )
            director_list.append(human)

        return MovieDTO(
            name=movie.name,
            year=movie.year,
            runtime=movie.runtime,
            rating=movie.rating,
            votes=movie.votes,
            meta_score=movie.meta_score,
            gross=movie.gross,
            genres=genre_list,
            certification=movie.certification,
            director=director_list,
            stars=star_list,
            description=movie.description
        )

    @classmethod
    def create_movie(cls, movie_dto: MovieDTO) -> int:
        movie_dict = movie_dto._asdict()
        movie_dict.pop("genres", None)
        movie_dict.pop("director", None)
        movie_dict.pop("stars", None)
        movie = Movie.objects.create(**movie_dict)
        return movie.pk

    @classmethod
    def add_star(cls, star_id: int, movie_name: str):
        star = Human.objects.filter(pk=star_id).first()
        movie = Movie.objects.filter(name=movie_name).first()
        if star not in movie.stars.all():
            movie.stars.add(star)

    @classmethod
    def add_director(cls, director_id: int, movie_name: str):
        director = Human.objects.filter(pk=director_id).first()
        movie = Movie.objects.filter(name=movie_name).first()
        if director not in movie.director.all():
            movie.director.add(director)

    @classmethod
    def add_genre(cls, genre_name: str, movie_name: str):
        genre = Genre.objects.filter(genre=genre_name).first()
        movie = Movie.objects.filter(name=movie_name).first()
        if genre not in movie.genres.all():
            movie.genres.add(genre)
