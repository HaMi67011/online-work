import matplotlib.pyplot as plt

# Assuming you have collected data on time steps and crop picking statistics for each robot
robot_data = {
    "robot1": {
        "time_steps": [10, 15, 20, 25, 30],  # Time steps taken by robot1 in different runs
        "crops_picked": [50, 60, 55, 70, 65],  # Number of crops picked by robot1 in different runs
    },
    "robot2": {
        "time_steps": [12, 14, 16, 18, 20],  # Time steps taken by robot2 in different runs
        "crops_picked": [55, 50, 65, 60, 55],  # Number of crops picked by robot2 in different runs
    },
}

# Indicator 1: Time taken to pick the crops
plt.figure(figsize=(8, 6))
for robot, data in robot_data.items():
    plt.plot(data["time_steps"], label=robot)

plt.xlabel("Run")
plt.ylabel("Time Steps")
plt.title("Time Taken to Pick Crops")
plt.legend()
plt.show()

# Indicator 2: Efficiency of crop picking
plt.figure(figsize=(8, 6))
for robot, data in robot_data.items():
    efficiency = [crops / max(data["crops_picked"]) for crops in data["crops_picked"]]
    plt.plot(efficiency, label=robot)

plt.xlabel("Run")
plt.ylabel("Efficiency")
plt.title("Efficiency of Crop Picking")
plt.legend()
plt.show()

