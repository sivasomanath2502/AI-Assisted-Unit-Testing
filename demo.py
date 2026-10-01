from dataset_loader import load_dataset
from pipeline import run_pipeline
from utils.dataset_contract import infer_contract


def display_problems(dataset):

    print("\n" + "=" * 70)
    print(
        "        AI-ASSISTED UNIT TEST GENERATION SYSTEM"
    )
    print("=" * 70)

    print("\nAvailable Problems")
    print("=" * 70)

    for problem in dataset:

        task_id = problem["task_id"]

        contract = infer_contract(problem)

        function_name = contract[
            "function_name"
        ]

        description = problem.get(
            "text",
            "No problem description available.",
        ).strip()

        print(
            f"\nID: {task_id}"
        )

        print(
            f"Function: {function_name}"
        )

        print(
            "Problem:"
        )

        print(description)

        print("-" * 70)


def main():

    dataset = load_dataset()

    if not dataset:

        print(
            "No problems found in the dataset."
        )

        return

    display_problems(dataset)

    while True:

        user_input = input(
            "\nEnter Problem ID "
            "(or 'q' to quit): "
        ).strip()

        if user_input.lower() == "q":

            print(
                "\nExiting demo."
            )

            return

        try:

            task_id = int(user_input)

        except ValueError:

            print(
                "Invalid input. "
                "Please enter a valid Problem ID."
            )

            continue

        selected_problem = None

        for problem in dataset:

            if problem["task_id"] == task_id:

                selected_problem = problem

                break

        if selected_problem is None:

            print(
                f"Problem {task_id} "
                "was not found in the dataset."
            )

            continue

        contract = infer_contract(
            selected_problem
        )

        print(
            "\n"
            + "=" * 70
        )

        print(
            f"Selected Problem: "
            f"{selected_problem['task_id']}"
        )

        print(
            f"Function: "
            f"{contract['function_name']}"
        )

        print(
            "\nProblem:"
        )

        print(
            selected_problem["text"]
        )

        print(
            "=" * 70
        )

        print(
            "\nStarting agentic pipeline..."
        )

        result = run_pipeline(
            selected_problem
        )

        print(
            "\n"
            + "=" * 70
        )

        print(
            "DEMO COMPLETED"
        )

        print("=" * 70)

        final_result = (
            result.get("result")
            or {}
        )

        reference = (
            result.get("reference")
            or {}
        )

        print(
            "Code Correctness : "
            + (
                "PASS"
                if reference.get("passed")
                else "FAIL"
            )
        )

        print(
            "Review Status    : "
            + str(
                result.get(
                    "review_status",
                    "N/A",
                )
            )
        )

        print(
            "Test Execution   : "
            + str(
                final_result.get(
                    "test_execution",
                    "N/A",
                )
            )
        )

        branch_coverage = (
            final_result.get(
                "branch_coverage"
            )
        )

        if branch_coverage is None:

            branch_text = "N/A"

        else:

            branch_text = (
                f"{branch_coverage}%"
            )

        print(
            "Branch Coverage  : "
            + branch_text
        )

        print(
            "Tests Passed     : "
            + str(
                final_result.get(
                    "tests_passed",
                    0,
                )
            )
        )

        print(
            "Tests Failed     : "
            + str(
                final_result.get(
                    "tests_failed",
                    0,
                )
            )
        )

        print("=" * 70)

        again = input(
            "\nRun another problem? "
            "(y/n): "
        ).strip().lower()

        if again != "y":

            print(
                "\nExiting demo."
            )

            break


if __name__ == "__main__":

    main()