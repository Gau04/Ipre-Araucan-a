from mesa import Agent
import random
from params import *

class Colono(Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

        self.pos = pos
        self.reproducirse =  REPRODUCCION

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        # Calcula la cantidad de celdas ocupadas por colonos en la vecindad
        celdas_ocupadas_vecindad = sum(1 for pos in possible_steps if pos in self.model.celdas_ocupadas_colonos)
        # Calcula las probabilidades de movimiento ponderadas por la ocupación de celdas
        probabilities = [1.0 if pos in self.model.celdas_ocupadas_colonos else 0.5 for pos in possible_steps]
        probabilities = [prob / sum(probabilities) for prob in probabilities]
        # Elige una nueva posición según las probabilidades
        new_position = self.random.choices(possible_steps, weights=probabilities, k=1)[0]
        # Mueve al colono y actualiza la posición y el conjunto de celdas ocupadas
        self.model.grid.move_agent(self, new_position)
        self.pos = new_position
        self.model.celdas_ocupadas_colonos.add(new_position)  # Agrega la nueva posición

    def step(self):
        self.move()
        return