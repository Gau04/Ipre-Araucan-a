from mesa import Model
from mesa import time
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from params import *

from colonos import Colono
from nativos import Nativo
from aldea import Aldea

import numpy as np

class Araucania(Model):

    def __init__(self):
        self.verbose = False
        self.current_id = 0

        self.num_colonos = NUM_COLONOS
        self.num_nativos = NUM_NATIVOS
        self.schedule = time.RandomActivation(self)
        self.grid = MultiGrid(WIDTH, HEIGHT, False)
        self.celdas_ocupadas_colonos = set()
        self.celdas_batallas = np.zeros((WIDTH, HEIGHT))

        # Creando colonos
        x = 0
        y = HEIGHT - 1

        for i in range(self.num_colonos):
            colono = Colono(self.next_id(), (x,y), self)
            self.schedule.add(colono)
            self.grid.place_agent(colono, (x, y))

            x += 1

        ids_aldeas = []
        aldeas = []
        
        
        # Creando Aldeas
        for i in range (NUM_CIUDADES):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            aldea = Aldea(self.next_id(), (x,y),self)
            self.schedule.add(aldea)
            self.grid.place_agent(aldea, (x, y))
            #print(aldea.pos, "posaldea")
            ids_aldeas += [aldea.unique_id]
            aldeas += [aldea]

        # Creando Nativos
        num_actual = 0
        num_aldeas = 5
        aldea_nativo=aldeas[0]

        for i in range(self.num_nativos):

            if num_actual==num_aldeas-1:
                num_actual=0
            possible_steps = aldea_nativo.model.grid.get_neighborhood(
                aldea_nativo.pos,
                moore=True,
                include_center=False)
            pos_nativo = aldea_nativo.random.choice(possible_steps)
            nativo = Nativo(self.next_id(), pos_nativo, CULTURA, self, aldeas[num_actual])
            self.schedule.add(nativo)
            self.grid.place_agent(nativo, pos_nativo)
            num_actual += 1
            aldea_nativo = aldeas[num_actual]
        
        
        self.datacollector = DataCollector(
            {
                "Nativos": lambda m: len([nativo for agent in m.schedule.agents if isinstance(agent, Nativo)]),
                "Colonos": lambda m: len([colono for agent in m.schedule.agents if isinstance(agent, Colono)]),
                "Aldeas": lambda m: len([aldea for agent in m.schedule.agents if isinstance(agent, Aldea)])
            }
        )
        
        self.datacollector.collect(self)

    def llegan_colonos(self):
        x = 0
        y = HEIGHT - 1

        for i in range(self.num_colonos):
            colono = Colono(self.next_id(), (x,y), self)
            self.schedule.add(colono)
            self.colocar_colono(colono, x, y)

            x += 1
        return
    
    def colocar_colono(self, colono, x, y):
        self.grid.place_agent(colono, (x, y))
        self.celdas_ocupadas_colonos.add((x, y))

    def step(self):
        if self.schedule.time%TASA_COLONOS==0 and self.schedule.time!=0:
            self.llegan_colonos()
        self.schedule.step()
        

        if self.verbose:
            self.datacollector.collect(self)
            print(
                [
                    self.schedule.time,
                    print(self.datacollector.get_model_vars_dataframe())
                ]
            )

    