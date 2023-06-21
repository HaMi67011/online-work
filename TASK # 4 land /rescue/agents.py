import mesa
import random

NUMBER_OF_CELLS = 50

class FarmingAgent(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

        self.x, self.y = pos
        
        self.state = "Idle"
        self.harvested = 0

    def step(self):
        action = self.make_decision()
        if action == "harvest":
            self.harvest()
        elif action == "move_fw":
            self.move_fw()
        elif action == "move_bw":
            self.move_bw()
        elif action == "wait":
            self.wait()

    def make_decision(self):
        action = "wait"

        if self.state == "Idle":
            if self.can_harvest():
                action = "harvest"
            else:
                next_position = (self.x + 1, self.y)
                if not self.model.grid.is_cell_empty(next_position):
                    action = "move_fw"
        else:
            if self.x - 1 == 0:
                action = "move_bw"
            else:
                action = "move_fw"

        return action

    def harvest(self):
        self.state = "Harvesting"
        self.harvested += 1

    def move_fw(self):
        self.state = "Moving"
        self.x += 1
        self.model.grid.move_agent(self, (self.x, self.y))

    def move_bw(self):
        self.state = "Moving"
        self.x -= 1
        self.model.grid.move_agent(self, (self.x, self.y))

    def wait(self):
        self.state = "Idle"

    def can_harvest(self):
        # Example condition for harvesting strawberries from trees in soil
        if self.model.grid.is_cell_empty((self.x, self.y)):
            return False
        
        contents = self.model.grid.get_cell_list_contents((self.x, self.y))
        for agent in contents:
            if isinstance(agent, TreeAgent):
                return True
        return False

    def get_harvested_amount(self):
        return self.harvested


class ExplorerDrones(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

        self.x, self.y = pos
        self.state = "Idle"

    def step(self):
        action = self.make_decision()
        if action == "move_fw":
            self.move_fw()
        elif action == "move_bw":
            self.move_bw()
        elif action == "wait":
            self.wait()

    def make_decision(self):
        action = "wait"

        if self.state == "Idle":
            next_position = (self.x + 1, self.y)
            if not self.model.grid.is_cell_empty(next_position):
                action = "move_fw"
        else:
            if self.x - 1 == 0:
                action = "move_bw"
            else:
                action = "move_fw"

        return action

    def move_fw(self):
        self.state = "Moving"
        self.x += 1
        self.model.grid.move_agent(self, (self.x, self.y))

    def move_bw(self):
        self.state = "Moving"
        self.x -= 1
        self.model.grid.move_agent(self, (self.x, self.y))

    def wait(self):
        self.state = "Idle"


class TreeAgent(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.x, self.y = pos

    def step(self):
        # Implement the behavior of the tree agent
        pass