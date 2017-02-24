import datetime as dt
import json
import requests
from prettytable import PrettyTable

def constuct_scoreboard_url(date=None):
    if date == None:
        date = dt.datetime.today().strftime("%Y%m%d")

    return "http://data.nba.net/data/10s/prod/v2/{}/scoreboard.json".format(date)


def build_scoreboard(game_json):
    quarter_list = ["Q1", "Q2", "Q3", "Q4", "OT1", "OT2", "OT3"]
    # build headers
    if len(game_json["vTeam"]["linescore"]) > 0:
        t = PrettyTable(["Team"] + quarter_list[:len(game_json["vTeam"]["linescore"])] + ["Final"])

        v_quarter_score = list()

        h_quarter_score = list()

        for score in game_json["vTeam"]["linescore"]:
            v_quarter_score.append(score["score"])

        for score in game_json["hTeam"]["linescore"]:
            h_quarter_score.append(score["score"])

        t.add_row([game_json["vTeam"]["triCode"]] + v_quarter_score + [game_json["vTeam"]["score"]])
        t.add_row([game_json["hTeam"]["triCode"]] + h_quarter_score + [game_json["hTeam"]["score"]])

    else:
        # if the game hasn't started yet, build the table with 0s in all the col
        t = PrettyTable(["Team", "Q1", "Q2", "Q3", "Q4", "Score"])
        t.add_row([game_json["vTeam"]["triCode"], 0, 0, 0, 0, 0])
        t.add_row([game_json["hTeam"]["triCode"], 0, 0, 0, 0, 0])

    return t

def get_scoreboard_json(scoreboard_url):
    r = requests.get(scoreboard_url)

    games_json = json.loads(r.text)

    # TODO Make this print out the date which the games were played on
    print("There are {} game(s) on".format(len(games_json["games"])))

    for game in games_json["games"]:
        print (build_scoreboard(game))
        if game["isGameActivated"]:
            print("*****Game is Currently ongoing*****")
            print("Current Time is {}".format(game["clock"]))

        else:
            print("Final Score: {} {} - {} {}".format(game["vTeam"]["triCode"],
                                                      game["vTeam"]["score"],
                                                      game["hTeam"]["triCode"],
                                                      game["hTeam"]["score"]))

        print ("\n")


if __name__ == "__main__":
    get_scoreboard_json(constuct_scoreboard_url())
