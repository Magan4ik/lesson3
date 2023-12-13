
from movies.parser_csv import MovieCSVReader, MovieDTO


class MovieFacade:
    def __init__(self, human_repositoty, genre_repository, movie_repository, movie_parser):
        self.human_repositoty = human_repositoty
        self.genre_repository = genre_repository
        self.movie_repository = movie_repository
        self.movie_parser: MovieCSVReader = movie_parser

    def create_movie(self, index: int = None):
        movie_dto_list = self.movie_parser.get_movie_dto_list()
        if not index:
            for movie_dto in movie_dto_list:
                self._create_movie_from_dto(movie_dto=movie_dto)
        else:
            self._create_movie_from_dto(movie_dto=movie_dto_list[index])

    def _create_movie_from_dto(self, movie_dto: MovieDTO):
        movie = self.movie_repository.get_movie_by_name(name=movie_dto.name)
        if movie:
            return
        self.movie_repository.create_movie(movie_dto=movie_dto)

        for star in movie_dto.stars:
            _, star_id = self.human_repositoty.get_human_by_full_name(full_name=f"{star.first_name} {star.last_name}")
            if not star_id:
                star_id = self.human_repositoty.create_human(human_dto=star)
            self.movie_repository.add_star(star_id=star_id, movie_name=movie_dto.name)

        for director in movie_dto.director:
            _, director_id = self.human_repositoty.get_human_by_full_name(full_name=f"{director.first_name} {director.last_name}")
            if not director_id:
                director_id = self.human_repositoty.create_human(human_dto=director)
            self.movie_repository.add_director(director_id=director_id, movie_name=movie_dto.name)

        for genre in movie_dto.genres:
            genre_name = self.genre_repository.get_genre_by_name(name=genre)
            if not genre_name:
                genre_name = self.genre_repository.create_genre(genre=genre)
            self.movie_repository.add_genre(genre_name=genre_name, movie_name=movie_dto.name)
