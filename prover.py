import subprocess
import os
import time

# Directory where Prover9 is located
PROVER9_PATH = '/mnt/c/Users/hozas/OneDrive/De toate/facultate/AI/labs/LADR-2009-11A/bin/prover9'

def puzzle(i, j):
    """
    Puzzle function that modifies the input file based on the user's selected answer (j),
    and then calls Prover9 to determine if the answer is correct.
    """
    # Run the prover and return whether the answer is correct
    return run_prover9(i, j)

def run_prover9(i, j):
    """
    Dynamically generates input files for Prover9 with a single goal and runs it.
    """
    file_in = f'theorem{i}_temp.in'  # Temporary file to avoid modifying the base file
    file_out = f'theorem{i}.out'

    # Generate content based on the selected question and goal
    input_file_content = get_theorem_content(i, j)

    # Write the input file
    with open(file_in, 'w') as f:
        f.write(input_file_content)

    # Run Prover9
    sys_operation = f"\"{PROVER9_PATH}\" < {file_in} > {file_out}"
    print(f"Running command: {sys_operation}")

    try:
        subprocess.run(sys_operation, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Prover9: {e}")
        return False

    # Check the output
    return search_in_file(file_out, 'THEOREM PROVED', 'SEARCH FAILED')

def get_theorem_content(theorem_number, goal):
    """
    Dynamically generates the content for a theorem's input file with the selected goal.
    """
    assumptions = load_assumptions(f"theorem{theorem_number}.in")

    if theorem_number == 1:
        if goal == 1:
            goal_content = 'formulas(goals).\n    l1.\nend_of_list.\n'
        elif goal == 2:
            goal_content = 'formulas(goals).\n    l2.\nend_of_list.\n'
        elif goal == 3:
            goal_content = 'formulas(goals).\n    l3.\nend_of_list.\n'
        else:
            raise ValueError("Invalid goal value for theorem1")

    elif theorem_number == 2:
        if goal == 1:
            goal_content = 'formulas(goals).\n    kills(jack, tuna).\nend_of_list.\n'
        elif goal == 2:
            goal_content = 'formulas(goals).\n    kills(curiosity, tuna).\nend_of_list.\n'
        else:
            raise ValueError("Invalid goal value for theorem2")

    else:
        raise ValueError(f"Theorem {theorem_number} not implemented")

    return assumptions + goal_content

def load_assumptions(file_name):
    """Reads only the assumptions from the specified file, filtering out goals."""
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

        # Filter out any existing goal sections
        assumptions = []
        in_goals_section = False
        for line in lines:
            if 'formulas(goals)' in line:
                in_goals_section = True
            elif 'end_of_list.' in line and in_goals_section:
                in_goals_section = False
            elif not in_goals_section:
                assumptions.append(line)

        return ''.join(assumptions)

    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
        raise

def search_in_file(file_name, correct_answer, wrong_answer):
    """Searches for the answer in the output file and returns True if correct_answer is found."""
    with open(file_name, "r") as file:
        for line in file:
            if correct_answer in line:
                return True
            if wrong_answer in line:
                return False
    return False
