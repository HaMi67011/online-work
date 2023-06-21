import mesa
import numpy as np
from rescue.agents import FirstAidRobot
from rescue.agents import ExplorerDrones
from rescue.agents import Person
from .agents import DONE
from mesa.space import SingleGrid, MultiGrid


def pending_person(model):
        return len([a for a in model.schedule.agents if isinstance(a,Person) and a.state != DONE])


class Rescue(mesa.Model):
    def __init__(self, n_first_aid=4, n_people=3, width=50, height=50,seed=123):
        """
            * Set schedule defining model activation
            * Sets the number of agents as per user input
            * Sets the grid space of the model
            * Create n First agent, Explorer agents as required and place them randomly on the edge of the left side of the 2D space.
            * Create m People as required and place them randomly within the model
        """
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.n_first_aid = n_first_aid
        self.n_explorer_agent = n_first_aid
        self.n_people = n_people
        # Use a simple grid, where edges wrap around.
        self.grid = mesa.space.Grid(width, height, torus=True)


        self.tick = 0
        y_s = []
        for n in range(self.n_first_aid):
            heading = (1, 0)
            #append element in vector 
            x = 1
            y = 1
            while True:
                y = self.random.randint(1,height-1)
                if self.grid.is_cell_empty((x,y)):
                    break
            
            y_s.append(y)
            pr = FirstAidRobot(n,(x,y),self)
            self.schedule.add(pr)            
            self.grid.place_agent(pr,(x,y))
        
        for n in range(self.n_explorer_agent):
            heading =(1,0)
            x=1
            y=1
            while True:
                y = self.random.randint(1,height-1)
                if self.grid.is_cell_empty((x,y)):
                    break

            y_s.append(y)
            b = ExplorerDrones(self.random.randint(900,5000),(x,y),self)
            self.schedule.add(b)            
            self.grid.place_agent(b,(x,y))


        for n in range(self.n_people):
            
            while True:
                x = self.random.randint(4,width-1)
                y = self.random.choice(y_s)
                if self.grid.is_cell_empty((x,y)):
                    break

            p = Person(n+self.random.randint(50,100),(x,y),self)
            self.schedule.add(p)            
            self.grid.place_agent(p,(x,y))
        self.running = True
        
        self.datacollector = mesa.DataCollector(
            model_reporters={"pending_person": pending_person}, agent_reporters={"state": "state"}
        )

    def step(self):
        """
        * Run while there are alive people, otherwise stop running model.
        """
        self.tick = self.tick + 1
        if pending_person(self) > 0:
            self.schedule.step()
        else:
           self.running = False
        print("running...",self.tick)
        self.datacollector.collect(self)

 