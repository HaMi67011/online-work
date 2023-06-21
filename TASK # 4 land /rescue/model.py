import mesa
import numpy as np
import random
import uuid
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid, MultiGrid

def pending_plots(model):
    return len([a for a in model.schedule.agents if a.state != "Done"])


class FarmModel(Model):
    def __init__(self, num_robots, num_drones, width, height):
        self.num_robots = num_robots
        self.num_drones = num_drones
        self.width = width
        self.height = height
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.datacollector = None
        self.grid_state = []
        self.running = True

        # Create robots
        for i in range(self.num_robots):
            robot = PickerRobot(str(uuid.uuid4()), self)
            self.schedule.add(robot)
            self.grid.place_agent(robot, self.find_empty_cell())

        # Create drones
        for i in range(self.num_drones):
            drone = ExplorerDrone(str(uuid.uuid4()), self)
            self.schedule.add(drone)
            self.grid.place_agent(drone, self.find_empty_cell())

        # Create trees
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < 0.2:
                    tree = Tree(str(uuid.uuid4()), self)
                    self.schedule.add(tree)
                    self.grid.place_agent(tree, (x, y))

        # Create soil
        for x in range(self.width):
            for y in range(self.height):
                soil = Soil(str(uuid.uuid4()), self)
                self.schedule.add(soil)
                self.grid.place_agent(soil, (x, y))

        # Create river
        for x in range(self.width):
            river = River(str(uuid.uuid4()), self)
            self.schedule.add(river)
            self.grid.place_agent(river, (x, 0))

        self.datacollector = None
        self.grid_state = []
        self.running = True

    def find_empty_cell(self):
        empty_cells = [cell for cell in self.grid.empties if self.grid.is_cell_empty(cell)]
        if empty_cells:
            return random.choice(empty_cells)
        else:
            return None

    def get_grid_state(self):
        state = []
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell_contents = self.grid.get_cell_list_contents((x, y))
                cell_state = {
                    "x": x,
                    "y": y,
                    "agents": [
                        {"agent_type": type(agent).__name__, "unique_id": agent.unique_id}
                        for agent in cell_contents
                    ],
                }
                state.append(cell_state)
        return state
    
    def step(self):
        self.schedule.step()
        self.grid_state.append(self.get_grid_state())

        if self.all_trees_pink():
            self.running = False

    def all_trees_pink(self):
        trees = [agent for agent in self.schedule.agents if isinstance(agent, Tree)]
        return all(tree.color == "pink" for tree in trees)


class PickerRobot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = 0
        self.location = None
        self.picked_strawberries = []
        self.pink_strawberry_count = 0
        self.selected_pink_strawberries = 0
        self.selected_trees = 0

    def move(self):
        if self.location is None:
            return

        possible_moves = self.model.grid.get_neighborhood(
            self.location, moore=True, include_center=False
        )
        if possible_moves:
            new_location = random.choice(possible_moves)
            self.model.grid.move_agent(self, new_location)
            self.location = new_location

    def pick_strawberries(self):
        cell_contents = self.model.grid.get_cell_list_contents(self.location)
        trees = [agent for agent in cell_contents if isinstance(agent, Tree)]
        strawberries = [agent for agent in cell_contents if isinstance(agent, StrawberryCrop)]

        for tree in trees:
            if tree.color == "pink":
                self.pink_strawberry_count += 1
                self.selected_trees += 1
                tree.count_pink_strawberry += 1

        for strawberry in strawberries:
            if strawberry.color == "pink":
                self.picked_strawberries.append(str(strawberry.unique_id))
                self.selected_pink_strawberries += 1
                self.model.grid.remove_agent(strawberry)

    def step(self):
        self.move()
        self.pick_strawberries()


class ExplorerDrone(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.location = None

    def set_random_location(self):
        empty_cells = self.model.grid.empties
        if empty_cells:
            self.location = random.choice(empty_cells)

    def move(self):
        if self.location is None:
            return

        possible_moves = self.model.grid.get_neighborhood(
            self.location, moore=True, include_center=False
        )
        if possible_moves:
            new_location = random.choice(possible_moves)
            self.model.grid.move_agent(self, new_location)
            self.location = new_location

    def step(self):
        if self.location is None:
            self.set_random_location()
        else:
            self.move()


class Tree(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.time_to_convert = random.randint(0, 100)
        self.color = "green"
        self.count_pink_strawberry = 0

    def convert_to_strawberry(self):
        if self.time_to_convert == 0 and self.color == "green":
            self.model.grid.remove_agent(self)
            strawberry = StrawberryCrop(str(uuid.uuid4()), self.model, age=1)
            self.model.grid.place_agent(strawberry, self.pos)
            self.model.schedule.add(strawberry)

    def step(self):
        self.convert_to_strawberry()
        self.time_to_convert = max(self.time_to_convert - 1, 0)


class StrawberryCrop(Agent):
    def __init__(self, unique_id, model, age):
        super().__init__(unique_id, model)
        self.age = age
        self.color = "pink"

    def step(self):
        pass


class Soil(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class River(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
