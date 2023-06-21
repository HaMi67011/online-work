import random
import uuid
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter

#this pickerrobots not working
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
            self.pos = new_location  # Update the pos attribute
        else:
            self.pos = self.location

    def pick_strawberries(self):
        if self.location is None:
            return

        cell_contents = self.model.grid.get_cell_list_contents([self.location])
        strawberries = [obj for obj in cell_contents if isinstance(obj, StrawberryCrop)]
        if strawberries and isinstance(strawberries[0], StrawberryCrop):
            pink_strawberries = [s for s in strawberries if s.color == "pink"]
            if pink_strawberries:
                picked_strawberry = random.choice(pink_strawberries)
                picked_strawberry.color = "green"
                self.picked_strawberries.append(picked_strawberry)
                self.pink_strawberry_count += 1
                self.selected_pink_strawberries += 1
            else:
                trees = [t for t in strawberries if isinstance(t, Tree)]
                if trees:
                    picked_tree = random.choice(trees)
                    self.picked_strawberries.append(picked_tree)
                    self.selected_trees += 1

    def get_selected_pink_strawberry_count(self):
        return self.selected_pink_strawberries

    def get_selected_tree_count(self):
        return self.selected_trees
    
    def get_accuracy(self):
        if self.selected_pink_strawberries + self.selected_trees > 0:
            return self.selected_pink_strawberries / (self.selected_pink_strawberries + self.selected_trees)
        else:
            return 0

    # New method to calculate efficiency
    def get_efficiency(self):
        if self.age > 0:
            return self.pink_strawberry_count / self.age
        else:
            return 0

    def step(self):
        self.age += 1
        self.move()
        self.pick_strawberries()

#this exploredrone not working
class ExplorerDrone(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.location = None
        self.pos = None

    def set_random_location(self):
        empty_cells = self.model.grid.empties
        if empty_cells:
            self.location = random.choice(empty_cells)
            self.pos = self.location

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
            self.pos = new_location  # Update the pos attribute
        else:
            self.pos = self.location

    def step(self):
        if self.location is None:
            self.set_random_location()
        else:
            self.move()


class Tree(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.time_to_convert = random.randint(0, 100)  # Random value between 0 and 100
        self.color = "green"
        self.count_pink_strawberry = 0

    def convert_to_strawberry(self):
        if self.time_to_convert == 0 and self.color == "green":
            self.model.grid.remove_agent(self)  # Remove the tree agent from the grid
            strawberry = StrawberryCrop(str(uuid.uuid4()), self.model, age=1)  # Create a new StrawberryCrop agent
            self.model.grid.place_agent(strawberry, self.pos)  # Place the StrawberryCrop agent in the same position
            self.model.schedule.add(strawberry)  # Add the StrawberryCrop agent to the schedule

    def step(self):
        self.convert_to_strawberry()
        self.time_to_convert -= 1 if self.time_to_convert > 0 else 0


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


class FarmModel(Model):
    def __init__(self, num_robots, num_drones, width, height):
        self.num_robots = num_robots
        self.num_drones = num_drones
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.total_picked_strawberries = 0
        self.grid_state = []
        self.all_trees_pink = False 

        # Place soil rows
        for x in range(width):
            for y in range(height):
                soil = Soil(str(uuid.uuid4()), self)
                self.grid.place_agent(soil, (x, y))

        # Create and add robots to the schedule
        for i in range(self.num_robots):
            robot = PickerRobot(str(uuid.uuid4()), self)
            self.schedule.add(robot)
            empty_cell = self.find_empty_cell()
            if empty_cell:
                self.grid.place_agent(robot, empty_cell)
                robot.location = empty_cell

        # Create and add drones to the schedule
        for i in range(self.num_drones):
            drone = ExplorerDrone(str(uuid.uuid4()), self)
            self.schedule.add(drone)
            empty_cell = self.find_empty_cell()
            if empty_cell:
                self.grid.place_agent(drone, empty_cell)
                drone.location = empty_cell

        # Create strawberry crops randomly across the farm
        for _ in range(8):
            age = random.randint(1, 10)
            strawberry = StrawberryCrop(str(uuid.uuid4()), self, age)
            empty_cell = self.find_empty_cell()
            if empty_cell:
                self.grid.place_agent(strawberry, empty_cell)
                self.schedule.add(strawberry)

        # Create tree columns
        tree_columns = 6  # Modify the number of tree columns
        column_spacing = width // (tree_columns + 1)
        tree_x_positions = [(col + 1) * column_spacing for col in range(tree_columns)]

        for x in tree_x_positions:
            for y in range(height):
                tree = Tree(str(uuid.uuid4()), self)
                self.grid.place_agent(tree, (x, y))

        # Create river
        river_x = width // 2  # Place the river in the middle column
        for y in range(height):
            river = River(str(uuid.uuid4()), self)
            self.grid.place_agent(river, (river_x, y))

        self.datacollector = DataCollector(
            model_reporters={
                "Total Picked Strawberries": "total_picked_strawberries",
                "Selected Pink Strawberries": lambda m: sum(
                    [robot.get_selected_pink_strawberry_count() for robot in m.schedule.agents if
                     isinstance(robot, PickerRobot)]
                ),
                "Selected Trees": lambda m: sum(
                    [robot.get_selected_tree_count() for robot in m.schedule.agents if
                     isinstance(robot, PickerRobot)]
                ),
                # Accuracy of the model
                "Accuracy": lambda m: sum(
                    [robot.get_accuracy() for robot in m.schedule.agents if isinstance(robot, PickerRobot)]
                ) / len([robot for robot in m.schedule.agents if isinstance(robot, PickerRobot)]),
                # Efficiency of the model
                "Efficiency": lambda m: sum(
                    [robot.get_efficiency() for robot in m.schedule.agents if isinstance(robot, PickerRobot)]
                ) / len([robot for robot in m.schedule.agents if isinstance(robot, PickerRobot)]),
            }
        )


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
        self.datacollector.collect(self)
        self.grid_state.append(self.get_grid_state())

        if self.all_trees_pink:
            self.running = False




def farm_portrayal(agent):
    #this instance not working
    if isinstance(agent, PickerRobot):
        return {
            "Shape": "circle",
            "Filled": "true",
            "Color": "black",
            "Layer": 0,
            "r": 0.5,
            "x": agent.pos[0],
            "y": agent.pos[1],
        }
    #this instance not working
    elif isinstance(agent, ExplorerDrone):
        symbol = "X"  # Assign "X" as the symbol for all ExplorerDrones
        return {
            "Shape": "text",
            "Text": symbol,
            "Color": "red",
            "Layer": 0,
            "x": agent.pos[0],
            "y": agent.pos[1],
        }
    elif isinstance(agent, StrawberryCrop):
        return {
            "Shape": "pin",
            "Filled": "true",
            "Color": "red" if agent.color == "pink" else "green",  # Change the color to red or green based on the agent's color attribute
            "Layer": 0,
            "r": 0.5,
            "x": agent.pos[0],
            "y": agent.pos[1],
        }
    elif isinstance(agent, Soil):
        return {
            "Shape": "rect",
            "Filled": "true",
            "Color": "brown",
            "Layer": 0,
            "w": 1,
            "h": 1,
            "x": agent.pos[0],
            "y": agent.pos[1],
        }
    elif isinstance(agent, Tree):
        color = "green"
        if agent.time_to_convert > 0:
            agent.step()
        if agent.time_to_convert == 0:
            color = "pink"  # Represent the converted tree as a brown soil
            agent.color = color
            agent.count_pink_strawberry += 1
            print(agent.count_pink_strawberry)

        return {
            "Shape": "rect",
            "Filled": "true",
            "Color": color,
            "Layer": 0,
            "w": 0.9,
            "h": 0.9,
            "x": agent.pos[0],
            "y": agent.pos[1],
            
        }
    elif isinstance(agent, River):
        return {
            "Shape": "rect",
            "Filled": "true",
            "Color": "blue",
            "Layer": 0,
            "w": 1,
            "h": 1,
            "x": agent.pos[0],
            "y": agent.pos[1],
        }
    else:
        return {}


def count_portrayal(agent):
    if isinstance(agent, Tree):
        return {
            "Shape": "text",
            "Text": str(agent.count_pink_strawberry),
            "Color": "black",
            "Layer": 0,
            "x": 0.5,
            "y": agent.pos[1],
        }
    else:
        return {}


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
    "Farm Model",
    model_params=model_params,
)
server.port = 8521
server.max_steps = 100
server.running = True  # Add a running attribute to the server
server.launch()
