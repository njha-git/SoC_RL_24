import numpy as np
from base import Agent, MultiArmedBandit
import matplotlib.pyplot as plt


class KLUCBAgent(Agent):
    # Add fields 

    def __init__(self, time_horizon, bandit:MultiArmedBandit,): 
        # Add fields
        super().__init__(time_horizon, bandit)
        self.bandit : MultiArmedBandit = bandit
        self.reward_memory = np.zeros(len(bandit.arms))
        self.count_memory = np.zeros(len(bandit.arms))
        self.time_step = 0

    def KLfun(self, p, q):
        if p==1:
            return p*np.log(p/q)
        elif p==0:
            return (1-p)*np.log((1-p)/(1-q))
        return p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q))
        
    def solve_q(self, rhs, p_a):
        if p_a == 1:
            return 1
        
        q =np.arange(p_a, 1, 0.001)
        lhs = []
        for e in q:
            lhs.append(self.KLfun(p_a, e))
        lhs_array = np.array(lhs)
        lhs_rhs = lhs_array-rhs
        lhs_rhs[lhs_rhs <= 0] = np.inf
        min_i = lhs_rhs.argmin()
        return q[min_i]


    def give_pull(self):
        klucb = np.zeros(len(self.reward_memory))
        for i in range(len(self.reward_memory)):
            p_a = self.reward_memory[i]/(self.count_memory[i]+1e-06)
            rhs = min(1, (np.log(self.time_step)+3*np.log(np.log(self.time_step)))/(self.count_memory[i]+1e-05))
            klucb[i] = self.solve_q(rhs, p_a)

        best_arm = np.argmax(klucb)
        reward = self.bandit.pull(best_arm)
        self.reinforce(reward, best_arm)

    def reinforce(self, reward, arm):
        self.count_memory[arm] += 1
        self.reward_memory[arm] += reward
        self.time_step += 1
        self.rewards.append(reward)
 
    def plot_arm_graph(self):
        counts = self.count_memory
        indices = np.arange(len(counts))

        # Plot the data
        plt.figure(figsize=(12, 6))
        plt.bar(indices, counts, color='skyblue', edgecolor='black')

        # Formatting
        plt.title('Counts per Category', fontsize=16)
        plt.xlabel('Arm', fontsize=14)
        plt.ylabel('Pull Count', fontsize=14)
        plt.grid(axis='y', linestyle='-')  # Add grid lines for the y-axis
        plt.xticks(indices, [f'Category {i+1}' for i in indices], rotation=45, ha='right')
        # plt.yticks(np.arange(0, max(counts) + 2, step=2))

        # Annotate the bars with the count values
        for i, count in enumerate(counts):
            plt.text(i, count + 0.5, str(count), ha='center', va='bottom', fontsize=12, color='black')

        # Tight layout to ensure there's no clipping of labels
        plt.tight_layout()

        # Show plot
        plt.show()


# Code to test
if __name__ == "__main__":
    # Init Bandit
    TIME_HORIZON = 10_000
    bandit = MultiArmedBandit(np.array([0.23,0.55,0.76,0.44]))
    agent = KLUCBAgent(TIME_HORIZON, bandit) ## Fill with correct constructor

    # Loop
    for i in range(TIME_HORIZON):
        agent.give_pull()

    # Plot curves
    agent.plot_reward_vs_time_curve()
    agent.plot_arm_graph()
    bandit.plot_cumulative_regret()
