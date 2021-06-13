

class Processor():
    def __init__(self, data):
        self.data = data

    def get_player_statistics(self):
        players = []
        for player in self.data["team_members"]:
            tournaments = []
            medals = [0,0,0]
            for tournament_result in self.data["player_results"]:
                player_tournament = None
                for result in tournament_result:
                    if result["username"] == player["username"] and "performance" in result:
                        player_tournament = { "rank": result["rank"], "score": result["score"], "performance": result["performance"] }
                        if result["rank"] <= 3:
                            medals[result["rank"] -1 ] += 1
                tournaments.append(player_tournament)
            total_points = sum([ t["score"]  for t in filter(lambda a: a is not None, tournaments) ])
            turniere = sum([ 1  for t in filter(lambda a: a is not None, tournaments) ])

            avg_performance = 0
            if len([t for t in tournaments if t!=None])!=0:
                avg_performance = sum([ t["performance"]  for t in filter(lambda a: a is not None, tournaments) ])/sum([ 1  for t in filter(lambda a: a is not None, tournaments) ])
            players.append({"turniere": turniere, "username": player["username"], "tournaments": tournaments, "url": player["url"], "total_points": total_points, "avg_performance": avg_performance, "medals": medals})

        return players

