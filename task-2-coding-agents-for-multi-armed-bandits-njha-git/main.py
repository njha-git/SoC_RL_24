# Write code which will run all the different bandit agents together and:
# 1. Plot a common cumulative regret curves graph
# 2. Plot a common graph of average reward curves

import numpy as np
from base import Agent, MultiArmedBandit
import matplotlib.pyplot as plt
from epsilon_greedy import EpsilonGreedyAgent
from ucb import UCBAgent
from klucb import KLUCBAgent
from thompson import ThompsonSamplingAgent


if __name__ == "__main__":
    #S2
    # Init Bandit
    TIME_HORIZON = 30_000
    bandit = MultiArmedBandit(np.array([0.23,0.55,0.76,0.44]))
    agents = []
    agents.append(EpsilonGreedyAgent(TIME_HORIZON, bandit))
    agents.append(UCBAgent(TIME_HORIZON, bandit))
    agents.append(KLUCBAgent(TIME_HORIZON, bandit))
    agents.append(ThompsonSamplingAgent(TIME_HORIZON, bandit))

    # Loop
    for i in range(TIME_HORIZON):
        for agent in agents:
            agent.give_pull()

    

    # Plot curves
    plt.figure(figsize=(8,4))
    for agent in agents:
        # Create an index for timesteps
        timesteps = np.arange(1, len(agent.rewards) + 1)

        # Average out self.rewards
        avg_rewards = [np.mean(agent.rewards[0:T+1]) for T in range(agent.time_to_run)]

        # Plot the data
        plt.plot(timesteps, avg_rewards, linestyle='-', label="Agent{}".format(agents.index(agent)))

    # Formatting
    plt.title('Average Reward Over Time', fontsize=16)
    plt.xlabel('Timesteps', fontsize=14)
    plt.ylabel('Meanagentard Value upto timestep t', fontsize=14)
    plt.grid(True, which='both', linestyle='-', linewidth=0.5)
    # plt.xticks(timesteps)  # Show all timesteps as x-axis ticks
    # plt.yticks(np.arange(0, max(self.rewards) + 5, step=5))

    # Add legend
    plt.legend(loc='upper left', fontsize=12)

    # Tight layout to ensure there's no clipping of labels
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    for agent in agents:
        counts = agent.count_memory
        indices = np.arange(len(counts))

        # Plot the data
        plt.bar(indices, counts, edgecolor='black', label="Agent{}".format(agents.index(agent)))

    # Formatting
    plt.title('Counts per Category', fontsize=16)
    plt.xlabel('Arm', fontsize=14)
    plt.ylabel('Pull Count', fontsize=14)
    plt.grid(axis='y', linestyle='-')  # Add grid lines for the y-axis
    plt.xticks(indices, [f'Category {i+1}' for i in indices], rotation=45, ha='right')
    # plt.yticks(np.arange(0, max(counts) + 2, step=2))

    # Tight layout to ensure there's no clipping of labels
    plt.tight_layout()
    plt.legend()

    # Show plot
    plt.show()

    bandit.plot_cumulative_regret()

    #S2
    p_vals = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
    regret = []
    for p in p_vals:
        bandit = MultiArmedBandit(np.array([p, p+0.1]))
        agents = []
        agents.append(EpsilonGreedyAgent(TIME_HORIZON, bandit))
        agents.append(UCBAgent(TIME_HORIZON, bandit))
        agents.append(KLUCBAgent(TIME_HORIZON, bandit))
        agents.append(ThompsonSamplingAgent(TIME_HORIZON, bandit))

        # Loop
        for i in range(TIME_HORIZON):
            for agent in agents:
                agent.give_pull()

        temp = []
        for agent in agents:
            temp.append(agent.bandit.cumulative_regret_array[-1])
        regret.append(temp)
    
    x = [i+1 for i in range(17)]
    regret = np.array(regret)
    plt.plot(x, regret[:,0], label="epsilon greedy")
    plt.plot(x, regret[:,1], label="UCB")
    plt.plot(x, regret[:,2], label="KLUCB")
    plt.plot(x, regret[:,3], label="Thompson")
    plt.legend()
    plt.show()
