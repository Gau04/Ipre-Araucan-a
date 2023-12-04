from mesa import Agent
from params import *

class Aldea(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.cultura = CULTURA 
    
    def step(self):
        return