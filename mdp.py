from collections import defaultdict


class MDP():
    """Class for representing a Gridworld MDP.

    States are represented as (x, y) tuples, starting at (1, 1).  It is assumed that there are
    four actions from each state (up, down, left, right), and that moving into a wall results in
    no change of state.  The transition model is specified by the arguments to the constructor (with
    probability prob_forw, the agent moves in the intended direction. It veers to either side with
    probability of (1-prob_forw)/2 each.  If the agent runs into a wall, it stays in place.

    EXCEPT FOR PRINT STATEMENTS, DO NOT CHANGE ANYTHING IN THIS CLASS
    """

    def __init__(self, num_rows, num_cols, rewards, terminals, prob_forw, reward_default=0.0):
        """
        Constructor for this MDP.

        Args:
            num_rows: the number of rows in the grid
            num_cols: the number of columns in the grid
            rewards: a dictionary specifying the reward function, with (x, y) state tuples as keys,
                and rewards amounts as values.  If states are not specified, their reward is assumed
                to be equal to the reward_default defined below
            terminals: a list of state (x, y) tuples specifying which states are terminal
            prob_forw: probability of going in the intended direction
            reward_default: reward for any state not specified in rewards
        """
        self.nrows = num_rows
        self.ncols = num_cols
        self.states = []
        for i in range(num_cols):
            for j in range(num_rows):
                self.states.append((i+1, j+1))
        self.rewards = rewards
        self.terminals = terminals
        self.prob_forw = prob_forw
        self.prob_side = (1.0 - prob_forw)/2
        self.reward_def = reward_default
        self.actions = ['up', 'right', 'down', 'left']

    def get_states(self):
        """Return a list of all states as (x, y) tuples."""
        return self.states

    def get_actions(self, state):
        """Return list of possible actions from each state."""
        return self.actions

    def get_successor_probs(self, state, action):
        """Returns a dictionary mapping possible successor states to their transition probabilities
        for the given state and action.
        """
        if self.is_terminal(state):
            return {}  # we cant move from terminal state since we end

        x, y = state
        succ_up = (x, min(self.nrows, y+1))
        succ_right = (min(self.ncols, x+1), y)
        succ_down = (x, max(1, y-1))
        succ_left = (max(1, x-1), y)

        succ__prob = defaultdict(float)
        if action == 'up':
            succ__prob[succ_up] = self.prob_forw
            succ__prob[succ_right] += self.prob_side
            succ__prob[succ_left] += self.prob_side
        elif action == 'right':
            succ__prob[succ_right] = self.prob_forw
            succ__prob[succ_up] += self.prob_side
            succ__prob[succ_down] += self.prob_side
        elif action == 'down':
            succ__prob[succ_down] = self.prob_forw
            succ__prob[succ_right] += self.prob_side
            succ__prob[succ_left] += self.prob_side
        elif action == 'left':
            succ__prob[succ_left] = self.prob_forw
            succ__prob[succ_up] += self.prob_side
            succ__prob[succ_down] += self.prob_side
        return succ__prob

    def get_reward(self, state):
        """Get the reward for the state, return default if not specified in the constructor."""
        return self.rewards.get(state, self.reward_def)

    def is_terminal(self, state):
        """Returns True if the given state is a terminal state."""
        return state in self.terminals


def value_iteration(mdp, gamma, epsilon):
    """Calculate the utilities for the states of an MDP.

    Args:
        mdp: An instance of the MDP class defined above, describing the environment
        gamma: the discount factor
        epsilon: the change threshold to use when determining convergence.  The function returns
            when none of the states have a utility whose change from the previous iteration is more
            than epsilon

    Returns:
        A python dictionary, with state (x, y) tuples as keys, and converged utilities as values.
    """

    S = mdp.get_states()
    U = {}
    for i in S:
        u = {i:0}
        U.update(u)
    count = 0
    while True:
        delta = 0
        Uprime = U.copy() #updated Utilities for the round
        print("Iteration: ", count)
        print("Utilities: \n", ascii_grid_utils(Uprime))
        count += 1
        for state in S:
            A = mdp.get_actions(state) # actions from this state
            Aprime = [] # empty list to store the actions possible from this state
            for action in A:
                # Probability of going to next state given current state and action  * U of next state
                U_of_s_prime = 0

                nextstates = mdp.get_successor_probs(state, action)
                for move, prob in nextstates.items(): #move is sprime, iterate through the items
                    expected_u_s = prob * U[move]
                    U_of_s_prime += expected_u_s
                #POLICY will be the argmax of the Prob(sprime|s,a)*U[sprime】
                Aprime.append(U_of_s_prime)

            print("policy: ", max(Aprime))
            return_value = mdp.get_reward(state) + gamma * max(Aprime)


            #update the Uprime with the new value at that state
            Uprime[state] = return_value

        delta = max(delta, change_in_U(mdp, Uprime, U))
        U = Uprime # set up next iteration
        if delta < epsilon:
            break
    return Uprime


def change_in_U(mdp, Uprime, U):
    # Helper function to get new delta for each iteration

    max_diff = 0
    for state in mdp.get_states():
        diff = Uprime[state] - U[state]
        if diff > max_diff:
            max_diff = diff
    return max_diff

def derive_policy(mdp, utility):
    """Create a policy from an MDP and a set of utilities for each state.

    Args:
        mdp: An instance of the MDP class defined above, describing the environment
        utility: A dictionary mapping state (x, y) tuples to a utility value (perhaps calculated
            from value iteration)

    Returns:
        policy: A dictionary mapping state (x, y) tuples to the optimal action for that state (one
            of 'up', 'down', 'left', 'right', or None for terminal states)
    """
    policy = {}

    for s in mdp.get_states():
        if mdp.is_terminal(s):
            policy[s] = None
        else:
            best_action = None
            best_utility = float('-inf')
            for a in mdp.get_actions(s):
                exp_util = sum([ prob*utility[s_p] for s_p, prob in mdp.get_successor_probs(s, a).items() ])
                if exp_util > best_utility:
                    best_utility = exp_util
                    best_action = a
            policy[s] = best_action
    return policy


def ascii_grid_utils(utility):
    """Return an ascii-art gridworld with utilities.

    Args:
        utility: A dictionary mapping state (x, y) tuples to a utility value
    """
    return ascii_grid(dict([ (k, "{:8.4f}".format(v)) for k, v in utility.items() ]))


def ascii_grid_policy(actions):
    """Return an ascii-art gridworld with actions.

    Args:
        actions: A dictionary mapping state (x, y) tuples to an action (up, down, left, right)
    """
    symbols = { 'up':'^^^', 'right':'>>>', 'down':'vvv', 'left':'<<<', None:' x ' }
    return ascii_grid(dict([ (k, "   " + symbols[v] + "  ") for k, v in actions.items() ]))


def ascii_grid(vals):
    """High-tech helper function for printing out values associated with a 3x2 MDP."""
    s = ""
    s += " _____________________  \n"
    s += "|          |          | \n"
    s += "| {} | {} | \n".format(vals[(1, 3)], vals[(2, 3)])
    s += "|__________|__________| \n"
    s += "|          |          | \n"
    s += "| {} | {} | \n".format(vals[(1, 2)], vals[(2, 2)])
    s += "|__________|__________| \n"
    s += "|          |          | \n"
    s += "| {} | {} | \n".format(vals[(1, 1)], vals[(2, 1)])
    s += "|__________|__________| \n"
    return s
