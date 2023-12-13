from typing import NamedTuple, Literal

import pandas as pd


class HumanDTO(NamedTuple):
    first_name: str
    last_name: str
    profession: Literal["star", "director"]


class MovieDTO(NamedTuple):
    name: str
    year: int
    runtime: int
    rating: float
    votes: int
    meta_score: float
    gross: float
    genres: list[str]
    certification: str
    director: list[HumanDTO]
    stars: list[HumanDTO]
    description: str

class MovieShortDTO(NamedTuple):
    name: str
    year: int
    runtime: int
    rating: float
    description: str


class MovieCSVReader:
    def __init__(self, csv_name: str):
        self.df = pd.read_csv(csv_name)

    def get_movie_dto_list(self) -> list[MovieDTO]:
        self.fill_nan_values()
        movie_list = list()
        for index in range(len(self.df)):
            movie_list.append(self.parse_csv_to_dto_by_index(index=index))

        return movie_list

    def fill_nan_values(self):
        self.df["Certification"].fillna("Not Rated", inplace=True)
        self.df["MetaScore"].fillna(-1., inplace=True)
        self.df["Gross"].fillna(-1., inplace=True)

    def parse_csv_to_dto_by_index(self, index: int):
        return MovieDTO(
            name=self.df["Movie Name"][index],
            year=self.df["Year of Release"][index],
            runtime=self.df["Run Time in minutes"][index],
            rating=self.df["Movie Rating"][index],
            votes=self.df["Votes"][index],
            meta_score=self.df["MetaScore"][index],
            gross=self.df["Gross"][index],
            genres=self.convert_str_list_to_python_list("Genre", index=index),
            certification=self.df["Certification"][index],
            director=self.get_human_dto_list(proff="Director", index=index),
            stars=self.get_human_dto_list(proff="Stars", index=index),
            description=self.get_description(index=index)
        )

    def convert_str_list_to_python_list(self, column: str, index: int) -> list[str]:
        col: str = self.df[column][index]
        col = col.replace("['", "")
        col = col.replace("']", "")
        if "," in col:
            col_list = col.split("', '")
        else:
            col_list = [col]

        for i in range(len(col_list)):
            col_list[i] = col_list[i].strip()
        return col_list

    def get_human_dto_list(self, proff: Literal["Stars", "Director"], index: int) -> list[HumanDTO]:
        human_list = self.convert_str_list_to_python_list(proff, index=index)
        dto_list = list()
        for h in human_list:
            name = h.split(" ")
            first_name = name[0]
            if len(name) == 1:
                last_name = ""
            else:
                last_name = name[1]

            if proff == "Stars":
                profession: Literal["star"] = "star"
            else:
                profession: Literal["director"] = "director"
            dto = HumanDTO(
                first_name=first_name,
                last_name=last_name,
                profession=profession
            )
            dto_list.append(dto)

        return dto_list

    def get_description(self, index: int):
        word_list = self.convert_str_list_to_python_list(column="Description", index=index)
        return ' '.join(word_list)

