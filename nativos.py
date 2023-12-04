from mesa import Agent
from params import *
import random
from colonos import Colono

class Nativo(Agent):

    def __init__(self, unique_id, pos, cultura, model, aldea):
        super().__init__(unique_id, model)
        
        self.cultura = cultura
        self.pos = pos
        self.reproducirse = REPRODUCCION
        self.aldea = aldea
        self.cultura = self.aldea.cultura

    def move(self):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        x1, y1 = new_position
        x2, y2 = self.aldea.pos
        distance = abs(x1-x2) + abs(y1-y2)
        old_pos = (x1, y1)
        
        self.model.grid.move_agent(self, new_position)
        self.pos = new_position

        if distance>10:
            self.model.grid.move_agent(self, old_pos)
            self.pos = old_pos
        
    def reproduccion(self):
        posibilidades = [0, 1]

        eleccion = random.choices(posibilidades, weights = (1 - self.reproducirse, self.reproducirse), k = 1)

        if 0 in eleccion:
            return

        else:
            nativo = Nativo(self.model.next_id(), self.pos, 0.5 * self.cultura, self.model, self.aldea) 
            self.model.schedule.add(nativo)
            self.model.grid.place_agent(nativo, self.pos)
            self.reproducirse = self.reproducirse * 0.25 

    def batalla(self):
        ### SELECCIONAR COLONO, DECIDIR HUIR O PELEAR, CONTAR NATIVOS, REPETIR ESTO EN EL ARCHIVO DE COLONOS
        cellmates_nativo = self.model.grid.get_cell_list_contents([self.pos])
        colonos = [obj for obj in cellmates_nativo if isinstance(obj, Colono)]
        if len(colonos) > 0: 
            colono = self.random.choice(colonos)
            #contar nativos
            cellmates_nativo = self.model.grid.get_cell_list_contents([self.pos])
            nativos_cercanos = [obj for obj in cellmates_nativo if isinstance(obj, Nativo)]
            num_nativos_cercanos = len(nativos_cercanos)

            # contar colonos
            cellmates_colono = colono.model.grid.get_cell_list_contents([self.pos])
            colonos_cercanos = [obj for obj in cellmates_colono if isinstance(obj, Colono)]
            num_colonos_cercanos = len(colonos_cercanos)

            if num_nativos_cercanos > 1.4 * num_colonos_cercanos: ### cambiar el numero por un parametro
              posibilidades = [0, 1]
              eleccion = random.choices(posibilidades, weights = (0.2, 0.8), k = 1) ### cambiar esto por un parametro
              if 0 in eleccion: ### nativo gana, muere colono
                colono.model.grid.remove_agent(colono)
                colono.model.schedule.remove(colono)
            

              else: ###colono gana, muere nativo
                colono.model.grid.remove_agent(self)
                for nativo in nativos_cercanos:
                    nativo.aldea.cultura += 0.1
                colono.model.schedule.remove(self)
            
            else: ###colono gana, muere nativo
                colono.model.grid.remove_agent(self)
                colono.model.schedule.remove(self)
                for nativo in nativos_cercanos:
                    nativo.aldea.cultura += 0.1
            return
        
        else:
            return
        

    def step(self):
        cultura = self.cultura
        reproducirse = self.reproducirse
        total = cultura + reproducirse
        cultura /= total
        reproducirse /= total

        weights = [1, reproducirse, cultura]
        actions = [self.move, self.reproduccion, self.batalla]
        action = self.random.choices(actions, weights=weights, k=1)[0]

        ### añadiendo la batalla a la celda correspondiente
        if action == self.batalla:
            posicion_batalla = self.pos
            self.model.celdas_batallas[posicion_batalla] += 1
        action()