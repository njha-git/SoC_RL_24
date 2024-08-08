import numpy as np
import argparse
import matplotlib.pyplot as plt
import random

class FootballMDP:
    def __init__(self, p, q, opponent_policy):
        self.p = p
        self.q = q
        self.opponent_policy = self.load_policy(opponent_policy)
        self.states = self.initialize_states()
        self.actions = list(range(10))
        self.goal_positions = [13, 14]  # Goal is at squares 13 and 14

    def load_policy(self, policy_name):
        if policy_name == 'greedy':
            return self.greedy_policy
        elif policy_name == 'park':
            return self.park_policy
        elif policy_name == 'random':
            return self.random_policy

    def initialize_states(self):
        states = []
        for b1 in range(1, 17):
            for b2 in range(1, 17):
                for r in range(1, 17):
                    for ball in [1, 2]:
                        states.append((b1, b2, r, ball))
        return states

    def get_coordinates(self, position):
        return (position - 1) // 4, (position - 1) % 4

    def get_position(self, x, y):
        return x * 4 + y + 1

    def transition(self, state, action):
        b1, b2, r, ball = state
        if action in [0, 1, 2, 3]:  # Movement for B1
            return self.move(b1, action, ball == 1, state)
        elif action in [4, 5, 6, 7]:  # Movement for B2
            return self.move(b2, action - 4, ball == 2, state)
        elif action == 8:  # Pass
            return self.pass_ball(state)
        elif action == 9:  # Shoot
            return self.shoot(state)
        return []

    def move(self, player_pos, direction, has_ball, state):
        b1, b2, r, ball = state
        x, y = self.get_coordinates(player_pos)
        if direction == 0:  # Left
            y -= 1
        elif direction == 1:  # Right
            y += 1
        elif direction == 2:  # Up
            x -= 1
        elif direction == 3:  # Down
            x += 1

        if x < 0 or x > 3 or y < 0 or y > 3:
            return [((b1, b2, r, ball), 1.0)]  # Out of bounds, episode ends

        new_pos = self.get_position(x, y)

        if has_ball:
            success_prob = 1 - 2 * self.p
            fail_prob = 2 * self.p
            if new_pos == r:
                return [((b1, b2, r, ball), 0.5 - self.p), ((b1, b2, r, ball), 0.5 + self.p)]
            return [((new_pos if ball == 1 else b1, new_pos if ball == 2 else b2, r, ball), success_prob),
                    ((b1, b2, r, ball), fail_prob)]
        else:
            success_prob = 1 - self.p
            fail_prob = self.p
            return [((new_pos if ball == 1 else b1, new_pos if ball == 2 else b2, r, ball), success_prob),
                    ((b1, b2, r, ball), fail_prob)]

    def pass_ball(self, state):
        b1, b2, r, ball = state
        x1, y1 = self.get_coordinates(b1 if ball == 1 else b2)
        x2, y2 = self.get_coordinates(b2 if ball == 1 else b1)
        distance = max(abs(x1 - x2), abs(y1 - y2))
        pass_prob = self.q - 0.1 * distance

        if r == self.get_position((x1 + x2) // 2, (y1 + y2) // 2):
            pass_prob /= 2

        return [((b2 if ball == 1 else b1, b1 if ball == 1 else b2, r, 2 if ball == 1 else 1), pass_prob),
                (state, 1 - pass_prob)]

    def shoot(self, state):
        b1, b2, r, ball = state
        x, y = self.get_coordinates(b1 if ball == 1 else b2)
        goal_prob = self.q - 0.2 * (3 - x)

        if r in [self.get_position(2, 2), self.get_position(2, 3)]:
            goal_prob /= 2

        return [((b1, b2, r, ball), goal_prob), (state, 1 - goal_prob)]

    def reward(self, state, action):
        b1, b2, r, ball = state
        if b1 in self.goal_positions or b2 in self.goal_positions:
            return 1  # Goal scored
        return 0

    def is_terminal(self, state, action):
        b1, b2, r, ball = state
        return b1 in self.goal_positions or b2 in self.goal_positions or state in self.transition(state, action)

    def greedy_policy(self, state):
        b1, b2, r, ball = state
        target = b1 if ball == 1 else b2
        target_x, target_y = self.get_coordinates(target)
        r_x, r_y = self.get_coordinates(r)

        if r_x < target_x:
            return [6]  # Move down
        elif r_x > target_x:
            return [2]  # Move up
        elif r_y < target_y:
            return [5]  # Move right
        elif r_y > target_y:
            return [4]  # Move left
        return [random.choice([4, 5, 6, 7])]  # Random move

    def park_policy(self, state):
        return [random.choice([2, 6])]  # Move up or down in front of the goal

    def random_policy(self, state):
        return [random.choice([4, 5, 6, 7])]  # Random move

def value_iteration(mdp, discount_factor=1.0, theta=1e-6):
    V = np.zeros(len(mdp.states))
    while True:
        delta = 0
        for state_index, state in enumerate(mdp.states):
            v = V[state_index]
            V[state_index] = max([sum([prob * (mdp.reward(state, action) + discount_factor * V[mdp.states.index(next_state)])
                                       for next_state, prob in mdp.transition(state, action)])
                                  for action in mdp.actions])
            delta = max(delta, abs(v - V[state_index]))
        if delta < theta:
            break
    return V

def policy_from_value_function(mdp, V):
    policy = np.zeros(len(mdp.states), dtype=int)
    for state_index, state in enumerate(mdp.states):
        policy[state_index] = np.argmax([sum([prob * (mdp.reward(state, action) + V[mdp.states.index(next_state)])
                                              for next_state, prob in mdp.transition(state, action)])
                                         for action in mdp.actions])
        print(policy)
    return policy

def simulate(mdp, policy, num_episodes=1000):
    wins = 0
    for _ in range(num_episodes):
        state = random.choice(mdp.states)  # Start from a random state
        while not mdp.is_terminal(state, action):
            action = policy[mdp.states.index(state)]
            state = random.choices(*zip(*mdp.transition(state, action)))[0]
            if state in mdp.goal_positions:
                wins += 1
                break
        print(wins / num_episodes)
    return wins / num_episodes

# Command line arguments
parser = argparse.ArgumentParser(description='2v1 Football MDP')
parser.add_argument('--p', type=float, required=True, help='Skill level p')
parser.add_argument('--q', type=float, required=True, help='Skill level q')
parser.add_argument('--policy', type=str, required=True, choices=['greedy', 'park', 'random'], help='Opponent policy')
args = parser.parse_args()

# Create MDP instance
print(args.p, args.q, args.policy)
mdp = FootballMDP(args.p, args.q, args.policy)

# Compute the value function
V = value_iteration(mdp)

# Compute the optimal policy
policy = policy_from_value_function(mdp, V)

# Simulate the game
win_rate = simulate(mdp, policy)
print(f"Expected win rate: {win_rate}")

# Generate graphs for different p and q values
def generate_graphs():
    p_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    q_fixed = 0.7
    probabilities_p = []

    for p in p_values:
        mdp = FootballMDP(p, q_fixed, args.policy)
        V = value_iteration(mdp)
        initial_state = mdp.states.index((5, 9, 8, 1))
        probabilities_p.append(V[initial_state])

    plt.figure()
    plt.plot(p_values, probabilities_p)
    plt.xlabel('p values')
    plt.ylabel('Probability of Winning')
    plt.title('Probability of Winning for different p values with q=0.7')
    plt.show()

    q_values = [0.6, 0.7, 0.8, 0.9, 1.0]
    p_fixed = 0.3
    probabilities_q = []

    for q in q_values:
        mdp = FootballMDP(p_fixed, q, args.policy)
        V = value_iteration(mdp)
        initial_state = mdp.states.index((5, 9, 8, 1))
        probabilities_q.append(V[initial_state])

    plt.figure()
    plt.plot(q_values, probabilities_q)
    plt.xlabel('q values')
    plt.ylabel('Probability of Winning')
    plt.title('Probability of Winning for different q values with p=0.3')
    plt.show()

generate_graphs()
