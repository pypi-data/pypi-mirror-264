import math

class CHART:
    """
        Initializes the object with an optional granular flag.

        Parameters:
            granular (bool): A flag indicating if the object should be set to granular mode.

        Returns:
            None
    """
    def __init__(self, granular=False) -> None:
        self.granular = granular

    def plot_graph(self, values:list) -> None:
        """
            Generates a graph based on the values provided.

            Parameters:
                values (list): A list of lists containing coordinates for plotting the graph.

            Raises:
                TypeError: If values is not a list of lists or if coordinates are not numbers.

            Returns:
                None
        """
        for value in values:
            if type(value) != list:  raise TypeError("Values must be a list of lists")

            for iter, coord in enumerate(value):
                if type(coord) != int and type(coord) != float:  raise TypeError("coordinates must be a list of lists of numbers")
                value[iter] = round(coord)
                if self.granular == True:  value[iter] = value[iter] +1 if value[iter] % 2 != 0 else value[iter]

        yMax = max([coord[1] for coord in values])
        xMax = max([coord[0] for coord in values])
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

    def draw_bar(self, values:list, barWidth=10, space=5) -> None:
        """
            Generates a bar chart based on the provided values

            Parameters:
                - values (list): A list of lists where each inner list contains a string and an integer representing coordinates.
                - barWidth (int): The width of each bar in the chart.
                - space (int): The space between each bar in the chart.

            Returns:
                None
        """
        for value in values:
            if type(value) != list:  raise TypeError("Values must be a list of lists")
            if type(value[0]) != str or type(value[1]) != int:  raise TypeError("Coordinates must be a list of a string and an integer(in order)")

            for iter, coord in enumerate(value):
                if type(coord) == int and self.granular == True:  value[iter] = value[iter] +1 if value[iter] % 2 != 0 else value[iter]

        yMax = max([coord[1] for coord in values])
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

        next_coord = space
        for iter in range(0, yTop+1, step):
            pos = yTop - iter

            if pos in coordinates.keys():
                if type(coordinates[pos][0]) != list:  bar_list.append(coordinates[pos][1])
                else:
                    for l in coordinates[pos]:
                        bar_list.append(l[1])
                bar_list = sorted(bar_list)
            
            if pos % 10 == 0 and pos != 0:  chart += ' '*(labelWidth - 1 -len(str(pos))) + str(pos) + " +"
            elif pos == 0:
                chart += ' '*(labelWidth - 1 -len(str(pos))) + str(pos) + " +"
                for n in range(int(xTop/(barWidth + space))):
                    if n != len(values) -1:
                        if n == 0:  chart += f"{'-'*(round(barWidth/2) +space)}"
                        else:  chart += f"{'-'*(round(barWidth) +space)}"
                    else:
                        chart += f"{'-'*(barWidth +space)}--------\n"
                    next_coord = round(barWidth/2) + space
            else:  chart += f"{' ' *labelWidth}."


            if pos == 0:  continue
            plot = ''
            for k, bar in enumerate(bar_list):
                if k == 0:  plot += " "*(space) + "*"*barWidth
                else:  plot += " "*(bar -len(plot)) + "*"*barWidth
                if k == len(bar_list) -1:  plot += "\n"


            chart += plot

        print(chart)

    def draw_pict(self, values:list, symbol='|') -> None:
        """
            Generates a pictogram based on the values provided.
            
            Parameters:
                - values (list): A list of lists where each inner list represents a label and a numerical value.
                - symbol (str): The symbol to use for the pictogram. Default is '|'.
            
            Returns:
                None
        """
        for value in values:
            if type(value) != list:  raise TypeError("Values must be a list of lists")
            if type(value[0]) != str or (type(value[1]) != int and type(value[1]) != float):  raise TypeError("Coordinates must be a list of a string and an integer(in order)")

        labelWidth = max([len(coord[0]) for coord in values])
        pict = f"""{' ' *(labelWidth +1)}.\n{' ' *(labelWidth +1)}.\n{' ' *(labelWidth +1)}.\n"""

        for iter, value in enumerate(values):
            times = symbol *value[1] if self.granular == False else symbol *round(value[1]/2)
            pict += f"{' '*(labelWidth -len(value[0]))}{value[0]} +  {times}\n{' '*(labelWidth +1)}.\n"
            if iter == len(values) -1:  pict += f"{' '*(labelWidth +1)}."

        print(pict)

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return self.__str__