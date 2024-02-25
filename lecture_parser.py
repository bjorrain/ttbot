import yaml


class Lecture:

    def __init__(self, id: str, subjects, places: dict):
        self.id = id.split("_")
        self.tostr = ""
        if len(self.id) == 1:
            self.tostr = self.id[0]
        else:
            self.tostr = f"""
{self.id[0]}: {self.id[1]}
Где: {places[subjects[self.id[1]][self.id[0]]['place']]['name']}
Аудитория: {subjects[self.id[1]][self.id[0]]['auditory']}
"""
    def __str__(self):
        return self.tostr
    def __repr__(self) -> str:
        return self.tostr