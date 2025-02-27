import argparse
import json
from datetime import datetime

from lcb_runner.utils.path_utils import get_eval_all_output_path
from lcb_runner.utils.scenarios import Scenario


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo-0301",
        help="Name of the model to use matching `lm_styles.py`",
    )
    parser.add_argument(
        "--scenario",
        type=Scenario,
        default=Scenario.codegeneration,
        help="Type of scenario to run",
    )
    parser.add_argument(
        "--n", type=int, default=10, help="Number of samples to generate"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.2, help="Temperature for sampling"
    )

    parser.add_argument(
        "--eval_all_file",
        type=str,
        default=None,
        help="Alternative way to provide the evaluation file",
    )

    parser.add_argument(
        "--start_date",
        type=str,
        default=None,
        help="Start date for the contest to filter the evaluation file (format - YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        default=None,
        help="End date for the contest to filter the evaluation file (format - YYYY-MM-DD)",
    )

    args = parser.parse_args()

    if args.eval_all_file is None:
        args.eval_all_file = get_eval_all_output_path(args.model, args)

    return args


def compute_scores(args):
    with open(args.eval_all_file, "r") as f:
        results = json.load(f)

    for res in results:
        res["contest_date"] = datetime.fromisoformat(res["contest_date"])

    if args.start_date is not None:
        args.start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        results = [
            result for result in results if args.start_date <= result["contest_date"]
        ]

    if args.end_date is not None:
        args.end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        results = [
            result for result in results if result["contest_date"] <= args.end_date
        ]

    pass_1_list = [result["pass@1"] for result in results]
    print(f"Pass@1: {sum(pass_1_list) / len(pass_1_list)}")

    easy_pass_1_list = [
        result["pass@1"]
        for result in results
        if "difficulty" in result and result["difficulty"] == "easy"
    ]
    if len(easy_pass_1_list) > 0:
        print(f"Easy Pass@1: {sum(easy_pass_1_list) / len(easy_pass_1_list)}")

    medium_pass_1_list = [
        result["pass@1"]
        for result in results
        if "difficulty" in result and result["difficulty"] == "medium"
    ]
    if len(medium_pass_1_list) > 0:
        print(f"Medium Pass@1: {sum(medium_pass_1_list) / len(medium_pass_1_list)}")

    hard_pass_1_list = [
        result["pass@1"]
        for result in results
        if "difficulty" in result and result["difficulty"] == "hard"
    ]
    if len(hard_pass_1_list) > 0:
        print(f"Hard Pass@1: {sum(hard_pass_1_list) / len(hard_pass_1_list)}")


if __name__ == "__main__":
    compute_scores(get_parser())
