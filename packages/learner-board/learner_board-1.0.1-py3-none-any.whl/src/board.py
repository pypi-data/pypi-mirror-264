import requests
import argparse
from datetime import datetime

import prettytable


def get_url(space_id, page_no=1):
    return f"https://api.learnerhub.net/v1/products/{space_id}/issues?select_type=all&page={page_no}&order_type=created&order_action=desc"


def to_issue_url(space_id, issue_id):
    return f"https://www.learnerhub.net/#/spaces/{space_id}/issues/{issue_id}"


def format_datetime(_datetime):
    dt = datetime.strptime(_datetime, "%Y-%m-%dT%H:%M:%S.%f%z")
    # formatted_time = dt.strftime("%m/%d %H:%M:%S")
    formatted_time = dt.strftime("%m/%d ")
    return formatted_time + str(dt.weekday() + 1)


def main():
    argparser = argparse.ArgumentParser(prog="lboard")
    argparser.add_argument(
        "spaceid", type=int, help="you can find it in space's url, generally a number"
    )
    argparser.add_argument(
        "-p", "--page_count", type=int, default=7, help="pages to fetch"
    )

    args = argparser.parse_args()

    spaceid = args.spaceid
    pagecount = args.page_count

    table = prettytable.PrettyTable(["S", "Date", "Title"])
    table.align["Title"] = "c"
    for page_no in range(1, 1 + pagecount):
        response = requests.get(get_url(spaceid,page_no))
        issuses = response.json().get("data", [])
        count = 0
        for item in issuses:
            solved, essence = item["is_solve"], item["essence"]
            if solved and not essence:
                count += 1
                continue
            if count > 0:
                table.add_row(["", "", f"+ {count}"])
                count = 0
            table.add_row(
                [
                    ("" if solved else "?") + ("✔" if essence else ""),
                    format_datetime(item["created_at"]),
                    item["title"],
                ]
            )
            if not item["is_solve"]:
                table.add_row(["", "", "🔗 " + to_issue_url(spaceid,item["id"])])
    print(table)


if __name__ == "__main__":
    main()
