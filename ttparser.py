import yaml
from lecture_parser import Lecture


def generate_timetable(weekday: int, week: int, group: str, places: dict):
    with open(f"known_groups/{group}/{group}_{weekday}_tt.yml") as f:
        rules = yaml.safe_load(f)
    subjects = yaml.safe_load(open(f"known_groups/{group}/{group}_subjects.yml"))
    out = []
    for i in rules[weekday]:
        for key in i.keys():
            if key.count(",") > 0:
                if str(week) in key.split(","):
                    out.append(i[key])
            elif len(key.split("-")) == 2:
                weeks = [int(i) for i in key.split("-")]
                if weeks[0] <= week <= weeks[1]:
                    out.append(i[key])
            elif key == str(week):
                out.append(i[key])
            elif key == "even" and week % 2 == 0:  
                out.append(i[key])
            elif key == "odd" and week % 2 == 1:
                out.append(i[key])
            elif key == "every":
                out.append(i[key])
    out = [
        Lecture(id, subjects, places) for id in out
    ]
    print(out)
    return f"""
9:20: {out[0]}
11:00: {out[1]}
13:30: {out[2]}
15:10: {out[3]}
    """