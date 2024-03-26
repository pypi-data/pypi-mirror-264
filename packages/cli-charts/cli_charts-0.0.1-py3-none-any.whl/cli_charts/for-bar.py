import math

class CHART:
    def __init__(self, granular=False) -> None:
        self.granular = granular

    def plot_graph(self, values:list):
        for value in values:
            if type(value) != list:  raise TypeError("Values must be a list of lists")

            for iter, coord in enumerate(value):
                if type(coord) != int and type(coord) != float:  raise TypeError("coordinates must be a list of lists of numbers")
                value[iter] = round(coord)
                if self.granular == True:  value[iter] = value[iter] +1 if value[iter] % 2 != 0 else value[iter]

        yMax = max([cord[1] for cord in values])
        xMax = max([cord[0] for cord in values])
        yTop = math.ceil(yMax / 10) * 10
        xTop = math.ceil(xMax / 10) * 10
        labelWidth = len(str(yMax)) +1
        step = 2 if self.granular == True else 1
        coordinates = {}
        graph = f"""{' ' *labelWidth}.\n{' ' *labelWidth}.\n{' ' *labelWidth}.\n"""

        for value in values:
            if value[1] not in coordinates.keys():  coordinates[value[1]] = value[0]
            else:
                if type(coordinates[value[1]]) == list:  coordinates[value[1]].append(value[0])
                else:  coordinates[value[1]] = [coordinates[value[1]],value[0]]

                coordinates[value[1]] = sorted(coordinates[value[1]])

        for iter in range(0, yTop+1, step):
            pos = yTop - iter
            if pos % 10 == 0 and pos != 0:  graph += ' '*(labelWidth - 1 -len(str(pos))) + str(pos) + " +"
            elif pos == 0:
                graph += ' '*(labelWidth - 1 -len(str(pos))) + str(pos) + " +"
                for n in range(int(xTop/10)):
                    if n*10 !=( xTop -10):  graph += "---------+"
                    else:
                        graph += "---------+---\n"
                        for n in range(int(xTop/10)):
                            if n == 0:  graph += f"{' ' *labelWidth}         {(n*10) +10}"
                            else:  graph += f"        {(n*10) +10}"
            else:  graph += f"{' ' *labelWidth}."

            if pos in coordinates.keys():
                if type(coordinates[pos]) == list:
                    coords = coordinates[pos]
                    plot = ''
                    for k, n in enumerate(coords):
                        if k == 0:  plot += " "*(coords[k] - 1) + "*"
                        else:  plot += " "*((coords[k] -len(plot)) -1) + "*"
                        if k == len(coords) -1:  plot += "\n"

                    graph += plot
                else:
                    graph += " "*(coordinates[pos] -1) + "*\n"
            else:
                graph += f'{' ' *labelWidth}\n'

        print(graph)

    def draw_bar(self, values:list, barWidth=10, space=5):
        for value in values:
            if type(value) != list:  raise TypeError("Values must be a list of lists")
            if type(value[0]) != str or type(value[1]) != int:  raise TypeError("Coordinates must be a list of a string and an integer(in order)")

            for iter, coord in enumerate(value):
                if type(coord) == int and self.granular == True:  value[iter] = value[iter] +1 if value[iter] % 2 != 0 else value[iter]

        yMax = max([cord[1] for cord in values])
        xMax = (barWidth + space) *len(values)
        yTop = math.ceil(yMax / 10) * 10
        xTop = math.ceil(xMax / 10) * 10
        labelWidth = len(str(yMax)) +1
        step = 2 if self.granular == True else 1
        coordinates = {}
        bar_list = []
        chart = f"""{' ' *labelWidth}.\n{' ' *labelWidth}.\n{' ' *labelWidth}.\n"""

        next_coord = space
        for value in values:
            if value[1] not in coordinates.keys():  coordinates[value[1]] = [value[0], next_coord]
            else:
                if type(coordinates[value[1]][0]) != list:  coordinates[value[1]] = [coordinates[value[1]], [value[0], next_coord]]
                else:  coordinates[value[1]].append([value[0], next_coord])

            next_coord = next_coord + barWidth + space
        print(coordinates)

        next_coord = space
        for iter in range(0, yTop+1, step):
            pos = yTop - iter
            if pos % 10 == 0 and pos != 0:  chart += ' '*(labelWidth - 1 -len(str(pos))) + str(pos) + " +"
            elif pos == 0:
                chart += ' '*(labelWidth - 1 -len(str(pos))) + str(pos) + " +"
                for n in range(int(xTop/(barWidth + space))):
                    print(n, xTop, xMax)
                    if n != len(values) -1:
                        if n == 0:  chart += f"{'-'*(round(barWidth/2) +space)}"
                        else:  chart += f"{'-'*(round(barWidth) +space)}"
                    else:
                        chart += f"{'-'*(barWidth +space)}--------\n"
                        for n in range(int(xTop/(barWidth + space))):
                            if n == 0:  chart += f"{' ' *labelWidth}         {
                                values[n][0]}"
                            else:  chart += f"{' '*(barWidth +space)}{values[n][0]}"
                    next_coord = round(barWidth/2) + space
            else:  chart += f"{' ' *labelWidth}."

            if pos in coordinates.keys():
                if type(coordinates[pos][0]) != list:  bar_list.append(coordinates[pos][1])
                else:
                    for l in coordinates[pos]:
                        bar_list.append(l[1])
                bar_list = sorted(bar_list)

                plot = ''
                current = 0
                for n in range(xMax):
                    if pos == 0:  continue
                    if n == coordinates[pos][1]:
                        print(n)
                        plot += f"{" "*n}{"*"*barWidth}"
                        for n in range(xMax):
                            if n > len(plot):
                                if n in bar_list:
                                    plot += "*"*barWidth
                                    current = n
                                elif n not in bar_list and n > current +barWidth:  plot += " "
                    if n == xMax -1:  plot += '\n'
            # for k, bar in enumerate(bar_list):
            #     print(bar)
            #     if k == 0:  plot += " "*(coordinates[bar][1]) + "*"*barWidth
            #     else:  plot += " "*(bar -len(plot)) + "*"*barWidth
            #     if k == len(bar_list) -1:  plot += "\n"

            chart += plot

        print(chart)


    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return self.__str__
    

chart1 = CHART()
chart2 = CHART(True)
chart1.plot_graph([[15.3,4.9], [21.3,6.7], [26.4,8.4], [29.4,9.4], [34,10.8]])
chart2.plot_graph([[15.3,4.9], [21.3,6.7], [26.4,8.4], [29.4,9.4], [34,10.8]])

chart = CHART()
chart.draw_bar([['A', 25], ['B', 40], ['C', 10], ['D', 20], ['E', 100]], space=7)