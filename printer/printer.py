

class TablePrinter():
    def __init__(self, outfile, alternating_row = True, alternating_column = False, color1 = None, color2 = "#d3d3d3"):
        self.outfile = outfile
        self.alternating_row = alternating_row
        self.alternating_column = alternating_column
        self.in_cell = False
        self.in_row = False
        self.cell_in_row = 0
        self.row = 0

    def start_row(self):
        self.close_row()
        self.outfile.write("<tr>")
        self.in_row =True
        self.row += 1
        self.cell_in_row = 0
    
    def close_row(self):
        if self.in_row:
            self.outfile.write("</tr>")
        self.in_row = False

    def start_cell(self):
        self.close_cell()
        self.outfile.write("<td>")
        self.in_cell = True
        self.cell_in_row += 1
    
    def close_cell(self):
        if self.in_cell:
            self.outfile.write("</td>")
        self.in_cell = False

    def write(self,text):
        if not self.in_cell:
            self.start_cell()
        self.outfile.write(text)



        


class Printer():
    def __init__(self, data, player_statistics):
        self.data = data
        self.player_statistics = player_statistics
        self.outfile = TablePrinter(open("out","w"))

    def print_player_table(self):
        self.player_statistics.sort(key=lambda a: a["total_points"],reverse=True)

        self.outfile.write("<table><tr>")
        
        self.outfile.write("<th>Spieler</th>")
        self.outfile.write("<th>Punkte</th>")
        self.outfile.write("<th>&empty;-Perf.</th>")
        print(self.data["arenas"])
        for arena in self.data["arenas"]:
            start = arena["fullName"].find("iga")
            end = arena["fullName"].find("Team Battle")
            name = ""
            if start!=-1 and end!=-1:
                name = arena["fullName"][start+3:end]
            self.outfile.write('<th><a href="https://lichess.org/tournament/'+ arena["id"] +'">' + name  + "</a></th>")
        self.outfile.write("</tr>")


        for player in self.player_statistics:
            print(player["username"])
            if player["avg_performance"]>0:
                self.outfile.write("<tr><td>")
                self.outfile.write("<a href="+player["url"]+">"+player["username"]+"</a>")
                self.outfile.write("</td><td>")
                self.outfile.write(str(player["total_points"]))
                self.outfile.write("</td><td>")
                self.outfile.write(str(int(player["avg_performance"])))
                for tournament in player["tournaments"]:
                    if tournament != None:
                        color = ""
                        if tournament["rank"] == 1:
                            color = 'style="background-color:gold"'
                        if tournament["rank"] == 2:
                            color = 'style="background-color:silver"'
                        if tournament["rank"] == 3:
                            color = 'style="background-color:#bf8970"'
                        self.outfile.write("</td><td "+color+">")
                        self.outfile.write(str(tournament["rank"])+" | ")
                        self.outfile.write(str(tournament["score"]))
                    else:
                        self.outfile.write("</td><td>-")



                self.outfile.write("</td></tr>")



        self.outfile.write("</table>")
         


