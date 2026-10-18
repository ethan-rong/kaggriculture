"""Play the final submission locally.

    python play.py                     # one game vs Kaggle's starter bot
    python play.py --opponent self --seed 7
    python play.py --games 10 --opponent random

Prints both seats' final coins, the winner and the bot's slowest turn.
"""
import argparse
import importlib.util
import time
from pathlib import Path

from kaggle_environments import make

BOT = Path(__file__).parent / "submission" / "main.py"


def load_bot():
    spec = importlib.util.spec_from_file_location("final_bot", BOT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def play(seed, opponent):
    bot, times = load_bot(), []

    def timed(obs, cfg=None):
        t0 = time.perf_counter()
        out = bot(obs, cfg)
        times.append(time.perf_counter() - t0)
        return out

    rival = load_bot() if opponent == "self" else opponent
    env = make("kaggriculture", configuration={"seed": seed})
    env.run([timed, rival])
    statuses = [s.status for s in env.state]
    ours, theirs = (s.reward or 0 for s in env.state)
    return ours, theirs, statuses, max(times)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--opponent", default="starter", help="starter | random | pass | self")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--games", type=int, default=1)
    args = ap.parse_args()

    wins = 0
    for seed in range(args.seed, args.seed + args.games):
        ours, theirs, statuses, slowest = play(seed, args.opponent)
        wins += ours > theirs
        print(f"seed {seed}: bot {ours:,.0f} vs {args.opponent} {theirs:,.0f} | "
              f"status {statuses} | slowest turn {slowest:.2f}s")
    print(f"won {wins}/{args.games}")


if __name__ == "__main__":
    main()
