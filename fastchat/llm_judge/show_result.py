"""
Usage:
python3 show_result.py --mode [single|pairwise-baseline|pairwise-all]
"""

import argparse
import pandas as pd
from pathlib import Path


def display_result_single(args):
    wk_dir = Path(args.work_dir) or Path(__file__).parent / "data"
    input_file = (
        args.input_file
        or wk_dir / f"{args.bench_name}/model_judgment/{args.judge_model}_single.jsonl"
    )
    output_file = Path(input_file).with_suffix(".tsv")
    print(f"Input file: {input_file}")
    df_all = pd.read_json(input_file, lines=True)
    df = df_all[["model", "score", "turn", "question_id"]]
    df = df[df["score"] != -1]

    if args.model_list is not None:
        df = df[df["model"].isin(args.model_list)]

    df = df.drop_duplicates(subset=["model", "question_id", "turn"], keep="last")
    if args.exclude is not None:
        df = df[~df["question_id"].isin(args.exclude)]

    gdf = (
        df.groupby(["model", "turn"])
        .agg(score=("score", "mean"), count=("score", "count"))
        .reset_index()
    )
    agf = gdf.groupby("model").mean().reset_index()
    agf["turn"] = "avg"
    gdf = pd.concat([gdf, agf], ignore_index=True)
    gdf = gdf.sort_values(by=["turn", "score"], ascending=(True, False))
    print(gdf.to_csv(index=False, sep="\t", float_format="%.1f"))
    gdf.to_csv(output_file, index=False, sep="\t", float_format="%.2f")
    print(f"Result file: {output_file}")


def display_result_pairwise(args):
    wk_dir = Path(args.work_dir) or Path(__file__).parent / "data"
    input_file = (
        args.input_file
        or wk_dir / f"{args.bench_name}/model_judgment/{args.judge_model}_single.jsonl"
    )
    print(f"Input file: {input_file}")
    df_all = pd.read_json(input_file, lines=True)
    df_all = df_all[(df_all["g1_winner"] != "error") & (df_all["g2_winner"] != "error")]

    model_list = df_all["model_1"].unique().tolist() + df_all["model_2"].unique().tolist()
    model_list = list(set(model_list))

    list_res = []
    # traverse df row by row
    for index, row in df_all.iterrows():
        if args.model_list is not None and row["model_1"] not in args.model_list:
            continue
        if args.baseline_model is not None:
            if args.baseline_model not in [row["model_1"], row["model_2"]]:
                continue
        if row["g1_winner"] == "tie" or row["g1_winner"] != row["g2_winner"]:
            list_res.append({"model": row["model_1"], "win": 0, "loss": 0, "tie": 1})
            list_res.append({"model": row["model_2"], "win": 0, "loss": 0, "tie": 1})
        else:
            if row["g1_winner"] == "model_1":
                winner = row["model_1"]
                loser = row["model_2"]
            else:
                winner = row["model_2"]
                loser = row["model_1"]
            list_res.append({"model": winner, "win": 1, "loss": 0, "tie": 0})
            list_res.append({"model": loser, "win": 0, "loss": 1, "tie": 0})

    df = pd.DataFrame(list_res)
    df = df.groupby(["model"]).sum()

    # remove baseline model
    if args.baseline_model is not None:
        df = df[df.index != args.baseline_model]
    # add win rate
    df["win_rate"] = df["win"] / (df["win"] + df["loss"] + df["tie"])
    df["loss_rate"] = df["loss"] / (df["win"] + df["loss"] + df["tie"])
    # each tie counts as 0.5 win + 0.5 loss
    df["win_rate_adjusted"] = (df["win"] + 0.5 * df["tie"]) / (df["win"] + df["loss"] + df["tie"])
    # print(df.sort_values(by="win_rate", ascending=False))
    # print(df.sort_values(by="loss_rate", ascending=True))
    print(df.sort_values(by="win_rate_adjusted", ascending=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench-name", type=str, default="mt_bench")
    parser.add_argument("--input-file", type=str)
    parser.add_argument("--judge-model", type=str, default="gpt-4")
    parser.add_argument("--baseline-model", type=str, default="gpt-3.5-turbo")
    parser.add_argument(
        "--model-list",
        type=str,
        nargs="+",
        default=None,
        help="A list of models to be evaluated",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="single",
        choices=["pairwise-baseline", "pairwise-all", "single"],
        help=(
            "Evaluation mode. "
            "`pairwise-baseline` runs pairwise comparision against a baseline. "
            "`pairwise-all` runs pairwise comparision between all pairs. "
            "`single` runs single answer grading."
        ),
    )
    parser.add_argument("--work-dir", type=str, default=None, help="The working directory.")
    parser.add_argument(
        "--exclude", type=int, nargs="+", default=None, help="Exclude question ids."
    )
    args = parser.parse_args()

    if args.mode == "single":
        display_result_func = display_result_single
    else:
        if args.mode == "pairwise-all":
            args.baseline_model = None
        display_result_func = display_result_pairwise

    print(f"Mode: {args.mode}")
    display_result_func(args)
