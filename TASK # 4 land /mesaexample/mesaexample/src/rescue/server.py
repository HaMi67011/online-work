import mesa
from mesa.visualization.UserParam import UserSettableParameter
from rescue.model import Rescue
from .portrayal import wk1
from .agents import NUMBER_OF_CELLS

SIZE_OF_CANVAS_IN_PIXELS_X = 400
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "height": NUMBER_OF_CELLS,
    "width": NUMBER_OF_CELLS,
    "n_first_aid": UserSettableParameter(
        'slider',
        'number of first aid agents',
        5, #default
        1, #min
        20, #max
        1, #step
        description='n first aid and explorer'
    ),
    "n_people": UserSettableParameter(
    'slider',
    'number of people',
    5, #default
    1, #min
    20, #max
    1, #step
    description='number of people - fixed to 3'
    )           

}
grid = mesa.visualization.CanvasGrid(wk1, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)


server = mesa.visualization.ModularServer(
    Rescue, [grid], "Rescue people", simulation_params
)
