from rescue.agents import FarmingAgent
from rescue.agents import ExplorerDrones
from rescue.model import Tree,StrawberryCrop,Soil,River



def farming_agent_portrayal(agent):
    # Define the portrayal attributes for the FarmingAgent class
    # Modify the attributes based on your requirements
    return {
        "Shape": "circle",
        "Filled": "true",
        "Color": "green",
        "Layer": 0,
        "r": 0.5,
        "x": agent.x,
        "y": agent.y,
    }


def farming_portrayal(agent):
    """
    Determine which portrayal to use according to the type of agent.
    """
    if isinstance(agent, FarmingAgent):
        return farming_agent_portrayal(agent)
    elif isinstance(agent, ExplorerDrones):
        return explorer_drones_portrayal(agent)


def farm_portrayal(agent):
    if isinstance(agent, FarmingAgent):
        return {
            "Shape": "circle",  # Example shape, modify as needed
            "Filled": "true",
            "Color": "black",
            "Layer": 0,
            "r": 0.5,  # Example radius, modify as needed
            "x": agent.x,
            "y": agent.y,
        }
    elif isinstance(agent, ExplorerDrones):
        symbol = "X"  # Assign "X" as the symbol for all ExplorerDrones
        return {
            "Shape": "text",
            "Text": symbol,
            "Color": "red",
            "Layer": 0,
            "x": agent.x,
            "y": agent.y,
        }
    elif isinstance(agent, StrawberryCrop):
        return {
            "Shape": "rect",  # Example shape, modify as needed
            "Filled": "true",
            "Color": "red" if agent.color == "pink" else "green",  # Change the color based on the agent's color attribute
            "Layer": 0,
            "w": 1,  # Example width, modify as needed
            "h": 1,  # Example height, modify as needed
            "x": agent.x,
            "y": agent.y,
        }
    elif isinstance(agent, Soil):
        return {
            "Shape": "rect",  # Example shape, modify as needed
            "Filled": "true",
            "Color": "brown",
            "Layer": 0,
            "w": 1,  # Example width, modify as needed
            "h": 1,  # Example height, modify as needed
            "x": agent.x,
            "y": agent.y,
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
            "Shape": "rect",  # Example shape, modify as needed
            "Filled": "true",
            "Color": color,
            "Layer": 0,
            "w": 0.9,  # Example width, modify as needed
            "h": 0.9,  # Example height, modify as needed
            "x": agent.x,
            "y": agent.y,
        }
    elif isinstance(agent, River):
        return {
            "Shape": "rect",  # Example shape, modify as needed
            "Filled": "true",
            "Color": "blue",
            "Layer": 0,
            "w": 1,  # Example width, modify as needed
            "h": 1,  # Example height, modify as needed
            "x": agent.x,
            "y": agent.y,
        }
    else:
        return {}

def explorer_drones_portrayal(explorerDrone):
    if explorerDrone is None:
        raise AssertionError
    return {
        "Shape": "arrowHead",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": explorerDrone.x,
        "y": explorerDrone.y,
        "scale": 2,
        "heading_x": -1 if explorerDrone.isBusy else 1,
        "heading_y": 0,
        "Color": "blue" if explorerDrone.isBusy else "yellow",
    }

def person_portrayal(person):
    if person is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": person.x,
        "y": person.y,
        "Color": "red" if person.isSafe else "green",
    }
