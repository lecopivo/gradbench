import argparse
import json
import os.path
from pathlib import Path
from typing import Any

import manual.ht as golden
from gradbench.comparison import compare_json_objects
from gradbench.eval import Analysis, SingleModuleValidatedEval, approve, mismatch
from gradbench.evals.ht import io


def check(function: str, input: Any, output: Any) -> None:
    func = getattr(golden, function)
    proc = func(input | {"min_runs": 1, "min_seconds": 0})
    if proc.returncode == 0:
        ls = proc.stdout.splitlines()
        expected = json.loads(ls[0])
        return compare_json_objects(expected, output)
    else:
        return Analysis(
            valid=False,
            error=f"golden implementation failed with stderr:\n{proc.stderr}",
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=int, default=1)
    parser.add_argument("--max", type=int, default=2)
    parser.add_argument("--min-runs", type=int, default=1)
    parser.add_argument("--min-seconds", type=float, default=1)
    parser.add_argument("--no-validation", action="store_true", default=False)
    args = parser.parse_args()

    e = SingleModuleValidatedEval(
        module="ht", validator=approve if args.no_validation else mismatch(check)
    )
    e.start()
    if e.define().success:
        data_root = Path("evals/ht/data")  # assumes cwd is set correctly
        # NOTE: data files are taken directly from ADBench.
        simple_small = data_root / "simple_small"
        simple_big = data_root / "simple_big"
        complicated_small = data_root / "complicated_small"
        complicated_big = data_root / "complicated_big"

        def evals(data_dir, complicated):
            c = os.path.basename(os.path.normpath(data_dir)) + "/"
            for i in range(args.min, args.max + 1):
                fn = next(data_dir.glob(f"hand{i}_*.txt"), None)
                model_dir = data_dir / "model"
                input = io.read_hand_instance(model_dir, fn, complicated).to_dict()
                e.evaluate(
                    function="objective",
                    input=input
                    | {"min_runs": args.min_runs, "min_seconds": args.min_seconds},
                    description=c + fn.stem,
                )
                e.evaluate(
                    function="jacobian",
                    input=input
                    | {"min_runs": args.min_runs, "min_seconds": args.min_seconds},
                    description=c + fn.stem,
                )

        evals(simple_small, False)
        evals(simple_big, False)
        evals(complicated_small, True)
        evals(complicated_big, True)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, BrokenPipeError):
        pass
