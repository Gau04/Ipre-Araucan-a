from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from params import *

from colonos import Colono
from nativos import Nativo
from aldea import Aldea
from model import Araucania



def araucania_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if type(agent) is Colono:

        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#FF9999"

    elif type(agent) is Nativo:

        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#00FF00"

    elif type(agent) is Aldea: ### REVISAR COLORES

        portrayal["Color"] = ["#19cf2b", "#19cf2b"]
        portrayal["stroke_color"] = "##19cf2b"

    return portrayal

canvas_element = CanvasGrid(araucania_portrayal, WIDTH, HEIGHT, 500, 500)

server = ModularServer(
    Araucania, [canvas_element], "Conflicto Social en la Araucania"
)
server.port = 8521