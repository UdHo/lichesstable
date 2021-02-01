import requests
import json

class Downloader:
    baseurl = "https://lichess.org/api/"
#    team = "schachfreunde-berlin-1903"
    team = "schachfreunde-1974-heinsberg-ev"
    def get(self, url):
        req = requests.get(url)
        print("Download: " + url)
        if req.status_code == 200:
            return [json.loads(line) for line in iter(req.text.splitlines())]
        print(url + " download failed")


    def download_team_arenas(self):
        return self.get(self.baseurl + "team/" + self.team + "/arena")

    def download_team_players(self):
        return self.get(self.baseurl + "team/" + self.team + "/users")

    def download_arena_result(self, tournament):
        return self.get(self.baseurl + "tournament/" + tournament+ "/results")

    def download_arena_team_result(self, tournament):
        return self.get(self.baseurl + "tournament/" + tournament+ "/teams")
   
def get_data(team="schachfreunde-berlin-1903"):
    downloader = Downloader()

    players = downloader.download_team_players()

    #arenas = [a for a in filter(lambda a: "Lichess Qua" in a["fullName"], downloader.download_team_arenas())]
    arenas = [a for a in filter(lambda a: "Limburg" in a["fullName"], downloader.download_team_arenas())]
    arena_team_results = [ downloader.download_arena_team_result(tournament) for tournament in map(lambda a: a["id"],arenas)]
    arena_results = [ downloader.download_arena_result(tournament) for tournament in map(lambda a: a["id"],arenas)]

    return {"arenas": arenas, "team_results": arena_team_results, "player_results": arena_results, "team_members": players}

if __name__ == "__main__":
    print(get_data())
