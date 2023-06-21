import random
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from .model import FarmModel
from .portrayal import portray_cell, portray_robot, portray_drone

SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "width": UserSettableParameter(
        'slider',
        'Number of columns',
        50,  # default
        10,  # min
        100,  # max
        1,  # step
        description='Number of columns in the grid'
    ),
    "height": UserSettableParameter(
        'slider',
        'Number of rows',
        50,  # default
        10,  # min
        100,  # max
        1,  # step
        description='Number of rows in the grid'
    ),
    "num_robots": UserSettableParameter(
        'slider',
        'Number of robots',
        4,  # default
        1,  # min
        10,  # max
        1,  # step
        description='Number of robots in the simulation'
    ),
    "num_drones": UserSettableParameter(
        'slider',
        'Number of drones',
        3,  # default
        1,  # min
        10,  # max
        1,  # step
        description='Number of drones in the simulation'
    )
}

grid = CanvasGrid(portray_cell, simulation_params["width"], simulation_params["height"],
                  SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)

server = ModularServer(
    FarmModel, [grid], "Farm Model", simulation_params
)
 
