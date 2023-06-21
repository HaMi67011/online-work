import random

farm_width = 10
farm_height = 10
num_strawberries = 20

class FarmEnvironment:
    def __init__(self):
        self.grid = [[None for _ in range(farm_width)] for _ in range(farm_height)]
        self.agent_location = None
        self.agent_picked_count = 0
        self.agent_total_count = 0
        self.agent_reward = 0

        for _ in range(num_strawberries):
            x = random.randint(0, farm_width - 1)
            y = random.randint(0, farm_height - 1)
            self.grid[y][x] = "strawberry"

    def reset(self):
        self.agent_location = (0, 0)
        self.agent_picked_count = 0
        self.agent_total_count = 0
        self.agent_reward = 0

    def get_agent_location(self):
        return self.agent_location

    def get_agent_picked_count(self):
        return self.agent_picked_count

    def get_agent_total_count(self):
        return self.agent_total_count

    def get_agent_reward(self):
        return self.agent_reward

    def is_valid_location(self, x, y):
        return 0 <= x < farm_width and 0 <= y < farm_height

    def get_state(self):
        x, y = self.agent_location
        return (x, y, self.agent_picked_count)

    def take_action(self, action):
        x, y = self.agent_location
        dx, dy = action

        new_x = x + dx
        new_y = y + dy

        if self.is_valid_location(new_x, new_y):
            self.agent_location = (new_x, new_y)

            if self.grid[new_y][new_x] == "strawberry":
                self.agent_reward += 10
                self.agent_picked_count += 1

            self.agent_total_count += 1

        return self.get_state(), self.agent_reward, self.agent_picked_count == num_strawberries

class FarmRobotAgent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 0.1
        self.alpha = 0.5
        self.gamma = 0.9

    def get_action(self, state):
        if random.random() < self.epsilon or state not in self.q_table:
            action = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Random action
        else:
            q_values = self.q_table[state]
            max_q = max(q_values.values())
            best_actions = [a for a, q in q_values.items() if q == max_q]
            action = random.choice(best_actions)
        return action

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in [(0, 1), (0, -1), (1, 0), (-1, 0)]}

        max_q = max(self.q_table[next_state].values()) if next_state in self.q_table else 0
        old_q = self.q_table[state][action]
        new_q = old_q + self.alpha * (reward + self.gamma * max_q - old_q)
        self.q_table[state][action] = new_q


env = FarmEnvironment()
agent = FarmRobotAgent()
num_episodes = 1000

for episode in range(num_episodes):
    env.reset()
    state = env.get_state()

    while True:
        action = agent.get_action(state)
        next_state, reward, done = env.take_action(action)
        agent.update_q_table(state, action, reward, next_state)

        if done:
            break

        state = next_state

test_episodes = 10

for episode in range(test_episodes):
    env.reset()
    state = env.get_state()

    while True:
        action = agent.get_action(state)
        next_state, reward, done = env.take_action(action)

        if done:
            break

        state = next_state

    print("Episode:", episode + 1)
    print("Total picked strawberries:", env.get_agent_picked_count())
    print("Total reward:", env.get_agent_reward())
    print()
