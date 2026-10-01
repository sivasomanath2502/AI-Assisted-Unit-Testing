from dataset_loader import load_dataset
from pipeline import run_pipeline
from utils.results_writer import save_problem_result


dataset = load_dataset()

problem_data = next(
    problem
    for problem in dataset
    if problem["task_id"] == 11
)

print("=" * 60)
print("RUNNING SINGLE PROBLEM: 11")
print("=" * 60)

problem_result = run_pipeline(problem_data)

print("\n" + "=" * 60)
print("SAVING PROBLEM RESULT")
print("=" * 60)

result_file = save_problem_result(problem_result)

print(f"Result saved to: {result_file}")