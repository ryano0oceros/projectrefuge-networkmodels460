from pulp import LpMinimize, LpProblem, LpVariable
import pandas as pd
import math
import matplotlib.pyplot as plt

# Load the data from the Excel file
data = pd.read_excel('rf-project-plan.xlsx')  # Replace with your file path if necessary

# Define task duration dictionaries for each scenario using columns 4 (best case), 5 (expected), and 6 (worst case)
best_case_durations = data.set_index('taskID').iloc[:, 2].fillna(0).to_dict()  # Column 4 for best case
expected_case_durations = data.set_index('taskID').iloc[:, 3].fillna(0).to_dict()
worst_case_durations = data.set_index('taskID').iloc[:, 4].fillna(0).to_dict()

# Define a function to solve the LP model for each scenario and save results to a file
def solve_and_save_scenario(duration_scenario, filename):
    # Initialize the LP problem with a minimization objective
    scenario_problem = LpProblem("Project_Minimum_Time_Scenario", LpMinimize)
    
    # Define start time variables for each task
    start_times = {task: LpVariable(f"start_{task}", lowBound=0) for task in duration_scenario.keys()}
    
    # Objective function: Minimize the end time of the last task (H)
    scenario_problem += start_times['H'] + duration_scenario['H'], "Total_Project_Time_Scenario"
    
    # Constraints for task duration, handling NaN or inf values
    for task, duration in duration_scenario.items():
        if math.isfinite(duration):  # Check that duration is a valid number
            scenario_problem += start_times[task] + duration >= start_times[task], f"Duration_{task}_Scenario"
    
    # Precedence constraints: each task must start after its predecessors finish
    predecessors = data.set_index('taskID')['predecessorTaskIDs'].dropna().apply(lambda x: x.split(',')).to_dict()
    for task, preds in predecessors.items():
        for pred in preds:
            pred = pred.strip()  # Remove any extra whitespace
            if pred in duration_scenario and math.isfinite(duration_scenario[pred]):
                scenario_problem += start_times[task] >= start_times[pred] + duration_scenario[pred], f"Precedence_{pred}_to_{task}_Scenario"
    
    # Solve the model
    scenario_problem.solve()
    
    # Collect start times and total project duration
    task_start_times = {task: start_times[task].varValue for task in duration_scenario.keys()}
    total_time = start_times['H'].varValue + duration_scenario['H']
    
    # Write results to a text file
    with open(filename, 'w') as file:
        file.write(f"Total Project Time: {total_time}\n")
        file.write("Task Start Times:\n")
        for task, start_time in task_start_times.items():
            file.write(f"{task}: Start Time = {start_time}\n")
    
    return task_start_times, total_time  # Return start times for Gantt chart creation

# Function to generate a Gantt chart from task start times and durations
def create_gantt_chart(task_start_times, duration_scenario, title, filename):
    fig, ax = plt.subplots(figsize=(12, 8))
    for i, (task, start_time) in enumerate(task_start_times.items()):
        if start_time is not None:
            duration = duration_scenario[task]
            ax.barh(task, duration, left=start_time, height=0.5, align='center')
    ax.set_xlabel("Time (Hours)")
    ax.set_ylabel("Tasks")
    ax.set_title(title)
    plt.savefig(filename)  # Save the Gantt chart to file
    plt.close()

# Solve each scenario, save results, and generate Gantt charts
best_case_start_times, _ = solve_and_save_scenario(best_case_durations, "best.txt")
create_gantt_chart(best_case_start_times, best_case_durations, "Best Case Scenario Gantt Chart", "best_case_gantt.png")

expected_case_start_times, _ = solve_and_save_scenario(expected_case_durations, "expected.txt")
create_gantt_chart(expected_case_start_times, expected_case_durations, "Expected Case Scenario Gantt Chart", "expected_case_gantt.png")

worst_case_start_times, _ = solve_and_save_scenario(worst_case_durations, "worst.txt")
create_gantt_chart(worst_case_start_times, worst_case_durations, "Worst Case Scenario Gantt Chart", "worst_case_gantt.png")