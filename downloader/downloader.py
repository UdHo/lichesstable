import requests
import logging
import http.client
import json
import os.path
import glob, os

class Downloader:
    baseurl = "https://lichess.org/api/"
    team = "schachfreunde-berlin-1903"

    def get(self, url, cache = True, decode = True):
        path = ''.join(e for e in url if e.isalnum())
        path = "cache/" + path
        if os.path.isfile(path):
            print("Using cached: " + url)
            f = open(path,"r")
            if decode:
                return [json.loads(line) for line in iter(f.read().splitlines())]
            else:
                return f.read()
        req = requests.get(url)
        print("Download: " + url)
        if req.status_code == 200:
            if cache:
                f = open(path,"w")
                f.write(req.text)
                f.close()
            if decode:
                return [json.loads(line) for line in iter(req.text.splitlines())]
            else:
                return req.text
        print(url + " download failed")

    def read_cached(self, filename):
        print("Reading cached " + filename)
        f = open(filename,"r")
        return [json.loads(line) for line in iter(f.read().splitlines())]

    def download_team_arenas(self):
        return self.get(self.baseurl + "team/" + self.team + "/arena",False)

    def download_team_players(self):
        return self.get(self.baseurl + "team/" + self.team + "/users",False)

    def download_arena_result(self, tournament):
        result = self.get(self.baseurl + "tournament/" + tournament+ "/results")
        return result

    def download_arena_games(self, tournament):
        result = self.get(self.baseurl + "tournament/" + tournament+ "/games", True, False)

    def download_arena_team_result(self, tournament):
        result = self.get(self.baseurl + "tournament/" + tournament+ "/teams")
        return result
   
def get_data(team="schachfreunde-berlin-1903"):
    downloader = Downloader()
    http.client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    players = downloader.download_team_players()

    arenas = [a for a in filter(lambda a: ("Lichess Qua" in a["fullName"]) or ("Bundesliga" in a["fullName"]), downloader.download_team_arenas())]
    arena_team_results = [ downloader.download_arena_team_result(tournament) for tournament in map(lambda a: a["id"],arenas)]
    arena_results = [ downloader.download_arena_result(tournament) for tournament in map(lambda a: a["id"],arenas)]
    games = [downloader.download_arena_games(tournament) for tournament in map(lambda a: a["id"], arenas)]

    arena_results =[downloader.read_cached(f) for f in glob.glob("cache/*tourna*results")]

    result = {"arenas": arenas, "player_results": arena_results, "team_members": players}
    return result

