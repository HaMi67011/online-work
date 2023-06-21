import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter


class PickerRobot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = 0
        self.location = None
        self.picked_strawberries = []

    def move(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.location, moore=True, include_center=False
        )
        new_location = random.choice(possible_moves)
        self.model.grid.move_agent(self, new_location)
        self.location = new_location

    def pick_strawberries(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.location])
        strawberries = [obj for obj in cell_contents if isinstance(obj, StrawberryCrop)]
        if strawberries:
            oldest_strawberry = min(strawberries, key=lambda s: s.age)
            self.picked_strawberries.append(oldest_strawberry)
            self.model.grid.remove_agent(oldest_strawberry)
            self.model.total_picked_strawberries += 1

    def step(self):
        self.age += 1
        self.move()
        self.pick_strawberries()


class ExplorerDrone(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.location = None

    def move(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.location, moore=True, include_center=False
        )
        new_location = random.choice(possible_moves)
        self.model.grid.move_agent(self, new_location)
        self.location = new_location

    def step(self):
        self.move()


class StrawberryCrop(Agent):
    def __init__(self, unique_id, model, age):
        super().__init__(unique_id, model)
        self.age = age

    def step(self):
        pass


class FarmModel(Model):
    def __init__(self, num_robots, num_drones, width, height):
        self.num_robots = num_robots
        self.num_drones = num_drones
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.total_picked_strawberries = 0

        # Create and add robots to the schedule
        for i in range(self.num_robots):
            robot = PickerRobot(i, self)
            self.schedule.add(robot)
            empty_cell = self.grid.find_empty()
            self.grid.place_agent(robot, empty_cell)
            robot.location = empty_cell

        # Create and add drones to the schedule
        for i in range(self.num_drones):
            drone = ExplorerDrone(i + num_robots, self)
            self.schedule.add(drone)
            empty_cell = self.grid.find_empty()
            self.grid.place_agent(drone, empty_cell)
            drone.location = empty_cell

        # Create strawberry crops randomly across the farm
        for _ in range(8):
            age = random.randint(1, 10)
            strawberry = StrawberryCrop(self.schedule.get_agent_count(), self, age)
            empty_cell = self.grid.find_empty()
            self.grid.place_agent(strawberry, empty_cell)
            self.schedule.add(strawberry)

        self.datacollector = DataCollector(
            model_reporters={"Total Picked Strawberries": "total_picked_strawberries"}
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


def farm_portrayal(agent):
    if isinstance(agent, PickerRobot):
        return {"Shape": "circle", "Filled": "true", "Color": "red", "Layer": 0, "r": 0.5}
    elif isinstance(agent, ExplorerDrone):
        return {"Shape": "rect", "Filled": "true", "Color": "blue", "Layer": 0, "w": 0.9, "h": 0.9}
    elif isinstance(agent, StrawberryCrop):
        age = agent.age
        color = (1 - age / 10, 0, 0)  # Color gradient from green (young) to red (old)
        return {"Shape": "rect", "Filled": "true", "Color": color, "Layer": 0, "w": 0.9, "h": 0.9}
    else:
        return None


farm_canvas = CanvasGrid(farm_portrayal, 30, 30, 600, 600)

model_params = {
    "num_robots": UserSettableParameter("slider", "Number of Robots", 10, 1, 20),
    "num_drones": UserSettableParameter("slider", "Number of Drones", 5, 1, 10),
    "width": 30,
    "height": 30,
}

server = ModularServer(
    FarmModel,
    [farm_canvas],
    "Farm Simulation",
    model_params,
)

server.port = 8521
server.max_steps = 1000  # Set the maximum number of steps to run the model
server.launch()

