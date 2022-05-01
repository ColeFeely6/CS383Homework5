import mdp
import traceback

#TODO Change the given example to see what's wrong

"""
Carefully read the Homework 5 Coding pdf to understand what to implement in
this file. Replace the None values with the correct values as per those instructions.

Example of how to construct an MDP object is included at the bottom.
"""
def q1_and_2():
    """
    Replace the None values here based on the questions in the PDF.
    DO NOT change anything besides these None values when you submit.
    However, you may add print statements if it helps.
    """
    print('\n'+('─' * 50))
    print("Question 1 and 2")
    gridworld = mdp.MDP(3, 2,
                    rewards={
                        (1, 1): -1,
                        (1, 2): -5,
                        (2, 1): -1,
                        (2, 2): -1,
                        (2, 3): -1,
                        (3, 1): -1,
                        (1, 3): 10,
                              },
                    terminals=[(1, 3), (2, 3)],
                    prob_forw=0.8)
    EPSILON = 0.01
    discount_factor = 0.9
    utilities, policy = gen_results(gridworld, discount_factor, EPSILON)

    num_convergance_utility= 10
    num_convergance_policy= 6

    return {"gridworld": gridworld, "EPSILON": EPSILON,
        "discount_factor": discount_factor, "utilities": utilities,
        "policy": policy, "convergance_utility": num_convergance_utility,
        "convergance_policy": num_convergance_policy}

def q3():
    """
    Replace the None values here based on the questions in the PDF.
    DO NOT change anything besides these None values when you submit.
    However, you may add print statements if it helps.
    """
    print('\n'+('─' * 50))
    print("Question 3")
    gridworld = mdp.MDP(3, 2,
                        rewards={
                            (1, 1): -1,
                            (1, 2): -100,
                            (2, 1): -1,
                            (2, 2): -1,
                            (2, 3): -1,
                            (3, 1): -1,
                            (1, 3): 10,
                        },
                        terminals=[(1, 3), (2, 3)],
                        prob_forw=0.8)
    EPSILON = 0.01
    discount_factor = 0.9
    utilities, policy = gen_results(gridworld, discount_factor, EPSILON)

    """
    Enter one of the following answer choices below: "a", "b", "c", "d"
    """
    changed_policy_answer = 'b'

    return {"gridworld": gridworld, "EPSILON": EPSILON,
        "discount_factor": discount_factor,"utilities": utilities,
        "policy": policy, "letter_answer": changed_policy_answer}

def q4():
    """
    Replace the None values here based on the questions in the PDF.
    DO NOT change anything besides these None values when you submit.
    However, you may add print statements if it helps.
    """
    print('\n'+('─' * 50))
    print("Question 4")
    gridworld = None
    EPSILON = None
    discount_factor = None
    utilities, policy = gen_results(gridworld, discount_factor, EPSILON)

    """
    Enter one of the following answer choices below: "a", "b", "c", "d"
    """
    changed_policy_answer = None

    return {"gridworld": gridworld, "EPSILON": EPSILON,
        "discount_factor": discount_factor,"utilities": utilities,
        "policy": policy, "letter_answer": changed_policy_answer}

def q5():
    """
    Replace the None values here based on the questions in the PDF.
    DO NOT change anything besides these None values when you submit.
    However, you may add print statements if it helps.
    """
    print('\n'+('─' * 50))
    print("Question 5")
    gridworld = None
    EPSILON = None
    discount_factor = None
    utilities, policy = gen_results(gridworld, discount_factor, EPSILON)

    """
    Enter one of the following answer choices below: "a", "b", "c", "d"
    """
    changed_policy_answer = None

    return {"gridworld": gridworld, "EPSILON": EPSILON,
        "discount_factor": discount_factor,"utilities": utilities,
        "policy": policy, "letter_answer": changed_policy_answer}


##########################
def gen_results(emdeepee, gamma, epsilon):
    """Calculate the utilities for the states of an MDP and create a policy from
    an MDP and a set of utilities for each state.

    You many change what this file prints to clean up your output. But, DO NOT
    change how it works and what it returns.

    Args:
        emdeepee: An instance of the MDP class defined above, describing the environment
        gamma: the discount factor
        epsilon: the change threshold to use when determining convergence.  The function returns
            when none of the states have a utility whose change from the previous iteration is more
            than epsilon

    Returns:
        utility: A dictionary mapping state (x, y) tuples to a utility value (perhaps calculated
            from value iteration)
        policy: A dictionary mapping state (x, y) tuples to the optimal action for that state (one
            of 'up', 'down', 'left', 'right', or None for terminal states)
    """
    if emdeepee == None or gamma == None or epsilon == None:
        print("At least one of emdeepee, gamma, or epsilon was None in gen_results.")
        return None, None
    utilities = mdp.value_iteration(emdeepee, gamma, epsilon)
    try:
        print(mdp.ascii_grid_utils(utilities))
        print()
        policy = mdp.derive_policy(emdeepee, utilities)
        print(mdp.ascii_grid_policy(policy))
    except:
        if utilities == None:
            print("Your value iteration returns None in gen_results.")
        else:
            print("Error Traceback:")
            print('―' * 10)
            print(traceback.format_exc(),'―' * 10)
            print("\nYour value iteration is likely returning the wrong format.")
        return None, None

    return utilities, policy


if __name__ == "__main__":
    """
    You may change the code here as the autograder will not run it.
    We provide an example so you can see the general functionality of the
    question functions.

    By default we run all the question functions, so you will get an output even
    if you haven't started one of them.
    """
    ##########################
    "***Usage example***"
    print("Given Example")
    gridworld_example = mdp.MDP(3, 2,
                    rewards={
                        (1, 1): -1,
                        (1, 2): -5,
                        (2, 1): -1,
                        (2, 2): -1,
                        (2, 3): -1,
                        (3, 1): -1,
                        (1, 3): 10,
                              },
                    terminals=[(1, 3), (2, 3)],
                    prob_forw=0.8)
    EPSILON = 0.01
    discount_factor = 0.9
    utilities = gen_results(gridworld_example, discount_factor, EPSILON)

    ##########################
    q1_and_2_results = q1_and_2()
    q3_results = q3()
    q4_results = q4()
    q5_results = q5()
    "***OPTIONAL CODE HERE***"
