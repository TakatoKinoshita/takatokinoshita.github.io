import calendar
import os
import tomllib
from pathlib import Path

import jinja2

FILE_LIST = ["index.html", "index_ja.html"]


def strftime(obj, fmt="%Y-%m-%d"):
    return obj.strftime(fmt)


def month_name(mon):
    return calendar.month_name[mon]


def main():
    data = {}
    for data_file in filter(lambda p: p.is_file(), Path("data").iterdir()):
        with open(data_file, "rb") as f:
            data |= tomllib.load(f)

    for papers, tags in zip(
            ["journal_en", "journal_ja", "conference_en", "conference_ja"],
            [("article", "en"), ("article", "ja"), ("inproceedings", "en"), ("inproceedings", "ja")]):
        if papers in data:
            for paper in data[papers]:
                if "type" not in paper:
                    paper["type"] = tags[0]
                if "lang" not in paper:
                    paper["lang"] = tags[1]

    loader = jinja2.FileSystemLoader("templates")
    env = jinja2.Environment(loader=loader)
    env.filters["strftime"] = strftime
    env.filters["month_name"] = month_name

    os.makedirs("docs", exist_ok=True)
    for file in FILE_LIST:
        template = env.get_template(file)
        with open(Path("docs", file), "w") as f:
            f.write(template.render(data))


if __name__ == "__main__":
    main()
