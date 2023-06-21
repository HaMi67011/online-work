from rescue.agents import FirstAidRobot
from rescue.agents import ExplorerDrones
from rescue.agents import Person

def wk1(agent):
   """
   Determine which portrayal to use according to the type of agent.
   """
   if isinstance(agent,FirstAidRobot):
        return first_aid_robot_portrayal(agent)
   elif isinstance(agent, ExplorerDrones):
        return explorer_drones_portrayal(agent)
   elif isinstance(agent, Person):
        return person_portrayal(agent)

def first_aid_robot_portrayal(firstAidAgent):
 
    if firstAidAgent is None:
        raise AssertionError
    return {
        "Shape": "arrowHead",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": firstAidAgent.x,
        "y": firstAidAgent.y,
        "scale": 2,
        "heading_x": -1 if firstAidAgent.isBusy else 1,
        "heading_y":0,
        "Color": "red" if firstAidAgent.isBusy else "green",
    }

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
        "heading_y":0,
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
