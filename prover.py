import subprocess
import os
import time

PROVER9_PATH = '/mnt/c/Users/hozas/OneDrive/De toate/facultate/AI/labs/LADR-2009-11A/bin/prover9'
MACE4_PATH = '/mnt/c/Users/hozas/OneDrive/De toate/facultate/AI/labs/LADR-2009-11A/bin/mace4'

# Puzzle function that modifies the input file based on the user's selected answer (j), and then calls Prover9/Mace4 to determine if the answer is correct.
def puzzle(i, j):
    if i == 3:
        return run_mace4(i, j)
    else:
        return run_prover9(i, j)

# Dynamically generates input files for Prover9 with a single goal and runs it.
def run_prover9(i, j):

    file_in = f'theorem{i}_temp.in'  # Temporary file to avoid modifying the base file
    file_out = f'theorem{i}.out'

    # Generate content based on the selected question and goal
    input_file_content = get_theorem_content(i, j)

    # Write the input file
    with open(file_in, 'w') as f:
        f.write(input_file_content)

    # Run Prover9
    sys_operation = f"\"{PROVER9_PATH}\" < {file_in} > {file_out}"
    print(f"Running Prover9 with command: {sys_operation}")

    try:
        subprocess.run(sys_operation, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Prover9: {e}")
        return False
    finally:
        # Clean up temporary input file
        try:
            os.remove(file_in)
        except FileNotFoundError:
            pass

    # Check the output
    return search_in_file(file_out, 'THEOREM PROVED', 'SEARCH FAILED')

# Dynamically generates input files for Mace4 with a single goal and runs it.
def run_mace4(i, j):
    file_in = f'theorem{i}_temp.in'
    file_out = f'theorem{i}.out'

    input_file_content = get_theorem_content(i, j)

    with open(file_in, 'w') as f:
        f.write(input_file_content)

    mace4_command = [MACE4_PATH, '-f', file_in]

    try:
        result = subprocess.run(
            mace4_command, 
            capture_output=True,  # Capture both stdout and stderr
            text=True,
            timeout=60
        )

        # Write output to file
        with open(file_out, 'w') as output_file:
            output_file.write(result.stdout)

        # Print full output for debugging
        print("Mace4 Output:", result.stdout)
        print("Mace4 Error:", result.stderr)

        # Check return code
        #return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"Mace4 timed out for theorem {i}")
        return False
    except Exception as e:
        print(f"Error executing Mace4: {e}")
        return False

    # After the process finishes, verify the selected answer
    return verify_selected_answer(file_out, j)

# Dynamically generates the content for a theorem's input file with the selected goal.
def get_theorem_content(theorem_number, goal):
    
    assumptions = load_assumptions(f"theorem{theorem_number}.in")

    if theorem_number == 1:
        if goal == 1:
            goal_content = 'formulas(goals).\n l1.\n end_of_list.\n'
        elif goal == 2:
            goal_content = 'formulas(goals).\n l2.\n end_of_list.\n'
        elif goal == 3:
            goal_content = 'formulas(goals).\n l3.\n end_of_list.\n'
        else:
            raise ValueError("Invalid goal value for theorem 1")

    elif theorem_number == 2:
        if goal == 1:
            goal_content = 'formulas(goals).\n kills(jack, tuna).\n end_of_list.\n'
        elif goal == 2:
            goal_content = 'formulas(goals).\n kills(curiosity, tuna).\n end_of_list.\n'
        else:
            raise ValueError("Invalid goal value for theorem 2")
    
    elif theorem_number == 3:
        return assumptions

    elif theorem_number == 4:
        if goal == 1:
            goal_content = 'formulas(goals).\n killer(joplin).\n end_of_list.\n'
        elif goal == 2:
            goal_content = 'formulas(goals).\n killer(grieg).\n end_of_list.\n'
        elif goal == 3:
            goal_content = 'formulas(goals).\n killer(strauss).\n end_of_list.\n'
        elif goal == 4:
            goal_content = 'formulas(goals).\n killer(gershwin).\n end_of_list.\n'
        else:
            raise ValueError("Invalid goal value for theorem 4")
        
    elif theorem_number == 5:
        if goal == 1:
            goal_content = 'formulas(goals).\n M_A.\n end_of_list.\n'
        elif goal == 2:
            goal_content = 'formulas(goals).\n M_C.\n end_of_list.\n'
        elif goal == 3:
            goal_content = 'formulas(goals).\n M_B.\n end_of_list.\n'
        else:
            raise ValueError("Invalid goal value for theorem 5")
        
    elif theorem_number == 6:
        if goal == 1:
            goal_content = 'formulas(goals).\n victim(a).\n end_of_list.\n'
        elif goal == 2:
            goal_content = 'formulas(goals).\n victim(ah).\n end_of_list.\n'
        elif goal == 3:
            goal_content = 'formulas(goals).\n victim(s).\n end_of_list.\n' 
        elif goal == 4:
            goal_content = 'formulas(goals).\n victim(d).\n end_of_list.\n'
        elif goal == 5:
            goal_content = 'formulas(goals).\n victim(ab).\n end_of_list.\n' 
        else:
            raise ValueError("Invalid goal value for theorem 6")

    else:
        raise ValueError(f"Theorem {theorem_number} not implemented")

    return assumptions + goal_content

# Reads only the assumptions from the specified file, filtering out goals.
def load_assumptions(file_name):
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

# Searches for the answer in the output file and returns True if correct_answer is found.
def search_in_file(file_name, correct_answer, wrong_answer):
    with open(file_name, "r") as file:
        for line in file:
            if correct_answer in line:
                return True
            if wrong_answer in line:
                return False
    return False

# Verifies if the selected answer is correct based on the Mace4 output model.
def verify_selected_answer(file_name, selected_answer):
    
    # Define the mapping of answers to nationality strings
    nationality_mapping = {
        1: 'Brit',
        2: 'Swede',
        3: 'Dane',
        4: 'Norwegian',
        5: 'German'
    }

    # Validate the selected answer
    if selected_answer not in nationality_mapping:
        raise ValueError(f"Invalid answer selection. Must be between 1 and 5. Received: {selected_answer}")

    # Attempt to read the file content
    try:
        with open(file_name, "r") as file:
            model_content = file.read()
    except IOError as e:
        print(f"Error reading file {file_name}: {e}")
        return False

    # Find the Fish index
    fish_line = None
    for line in model_content.split('\n'):
        if "function(Fish, [" in line:
            fish_line = line.strip()
            break

    if not fish_line:
        print("Could not find Fish's line in the model.")
        return False

    # Extract the index for Fish 
    try:
        fish_index = int(fish_line.split('[ ')[-1].split(' ]')[0])
    except (IndexError, ValueError) as e:
        print(f"Error parsing Fish index: {e}")
        return False

    # Find the nationality with the same index by direct search in the model
    fish_nationality = None
    for line in model_content.split('\n'):
        if f"function(" in line and f"[ {fish_index} ])" in line:
            fish_nationality = line.split("function(")[1].split(",")[0].strip()
            break

    if not fish_nationality:
        print(f"Could not find a nationality with index {fish_index}")
        return False

    # Compare the found nationality with the selected answer
    selected_nationality = nationality_mapping[selected_answer]
    result = fish_nationality == selected_nationality

    return result