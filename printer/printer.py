

class TablePrinter():
    def __init__(self, outfile, alternating_row = True, alternating_column = False, styles = [None, "background-color:lightgrey"]):
        self.outfile = outfile
        self.alternating_row = alternating_row
        self.alternating_column = alternating_column
        self.in_cell = False
        self.in_row = False
        self.styles = styles
        self.cell_in_row = 0
        self.row = 0
        self.in_header = False
        self.outfile.write("<table>")

    def finish(self):
        self.close_row()
        self.outfile.write("</table>")

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

    def start_cell(self, text = None, attrs = None):
        if not self.in_row:
            self.start_row()
        self.close_cell()
        self.outfile.write("<td")
        if attrs:
            self.outfile.write(" " + attrs)
        else:
            counter = 0
            if self.alternating_row:
                counter += self.row
            if self.alternating_column:
                counter += self.cell_in_row 
            if self.styles[counter % len(self.styles)]:
                self.outfile.write(' style="' + self.styles[counter % len(self.styles)] + '"')
        self.outfile.write(">")
        self.in_cell = True
        self.cell_in_row += 1
        if text:
            self.write(text)

    def start_header_cell(self, text = None, attrs = None):
        self.close_cell()
        self.outfile.write("<th")
        if attrs:
            self.outfile.write(" " + attrs)
        else:
            counter = 0
            if self.alternating_row:
                counter += self.row
            if self.alternating_column:
                counter += self.cell_in_row 
            if self.styles[counter % len(self.styles)]:
                self.outfile.write(' style="' + self.styles[counter % len(self.styles)] + '"')
        self.outfile.write(">")
        self.in_cell = True
        self.in_header = True
        self.cell_in_row += 1
        if text:
            self.write(text)
    
    def close_cell(self):
        if self.in_cell:
            if self.in_header:
                self.outfile.write("</th>")
            else:
                self.outfile.write("</td>")
        self.in_cell = False
        self.in_header = False

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

        
        self.outfile.start_header_cell("Spieler")
        self.outfile.start_header_cell("Punkte")
        self.outfile.start_header_cell("&empty;-Perf.")
        #print(self.data["arenas"])
        for arena in self.data["arenas"]:
            start = arena["fullName"].find("iga")
            end = arena["fullName"].find("Team Battle")
            name = ""
            if start!=-1 and end!=-1:
                name = arena["fullName"][start+3:end]
            self.outfile.start_header_cell('<a href="https://lichess.org/tournament/'+ arena["id"] +'">' + name  + "</a>")
        self.outfile.close_row()

        for player in self.player_statistics:
            print(player["username"])
            if player["avg_performance"]>0:
                self.outfile.start_cell("<a href="+player["url"]+">"+player["username"]+"</a>")
                self.outfile.start_cell(str(player["total_points"]))
                self.outfile.start_cell(str(int(player["avg_performance"])))
                for tournament in player["tournaments"]:
                    if tournament != None:
                        color = None
                        if tournament["rank"] == 1:
                            color = 'style="background-color:gold"'
                        if tournament["rank"] == 2:
                            color = 'style="background-color:silver"'
                        if tournament["rank"] == 3:
                            color = 'style="background-color:#bf8970"'
                        self.outfile.start_cell(str(tournament["rank"])+" | ", color)
                        self.outfile.write(str(tournament["score"]))
                    else:
                        self.outfile.start_cell("-")

                self.outfile.close_row()
        self.outfile.finish()
         


