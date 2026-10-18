# How we tested it

The public ladder was useless as a test bench. A new bot needs 100+ games to settle, ratings drift 100 to 150 points a day as the field
improves, and the final ranking used a separate Bradley-Terry fit on wins and losses only. So every candidate was judged locally, by
rules written down before its first game.

## Rules first, numbers second

- Each candidate's bars, opponent pools and seed blocks were written to a file before any game was played. A rule change was logged
  as a numbered amendment, before the numbers it would affect.
- A seed block is used once. Used blocks go on a burned list that every later run checks.
- The pick rule between passing candidates was also fixed in advance, so the final choice is mechanical.

## Three kinds of evidence

| kind | what it is | strength | weakness |
|---|---|---|---|
| **Recorded frames** | A live ladder game rebuilt step by step with the engine's own functions: the candidate plays our seat, the rival replays its recorded actions. With no change, the rebuild reproduces both players' money after every step. | Real opponents, real worlds, cheap. | The rival cannot react, so every flip is an upper bound. |
| **Closed-loop pools** | Full engine games, both seats, paired seeds, against a population of public forks and our own earlier bots. | Rivals react. | The population is a proxy for the ladder. |
| **Forward holdout** | Live games that ended after the candidate's code was frozen. | Data the candidate could not have been fit to. | Small. Used as a veto only. |

Timing is a gate of its own: the slowest turn in a quiet run, times a 3.8 safety factor for Kaggle's slower CPU, must stay under
Kaggle's 1 s limit.

## Final gates

Every number below is against FXC, the previous bot, on identical jobs. F2FRSC3 is the submitted bot; F1FRSC3 is its one-line twin.

| gate | bar | F2FRSC3 | F1FRSC3 | FXC |
|---|---|---|---|---|
| Screen: 459 recorded ladder frames | net flips ≥ +3, margin ≥ 0 | +5 (+5 / −0), +169.8K | +5 (+5 / −0), +164.4K | 401-0-58 |
| Top-bot guard: 90 frames vs 2,700+ bots | net ≥ 0 | 0, +253 | 0, +502 | 25-0-65 |
| Training pool: 240 games | ≥ FXC − 1 pp | 238-2 | 238-2 | 238-2 |
| Head to head vs FXC: 100 paired games | win rate ≥ 0.55 | **91-9** | **100-0** | |
| Holdout pool: 480 games | ≥ FXC − 2 pp, every opponent ≥ 0.35 | 476-4, worst opponent 0.95 | 476-4, worst 0.95 | 476-4 |
| Holdout pool: 80 games | losses ≤ FXC + 2 | 79-1 | 79-1 | 79-1 |
| Timing: quiet max turn × 3.8 | < 1.0 s | 0.622 s | 0.614 s | 0.610 s |
| Forward holdout: 38 live games (veto) | net ≥ 0 | **+7 (+7 / −0), +79.6K** | +6 (+6 / −0), +77.8K | 20-0-18 |

Read plainly: both candidates flip losses on recorded frames and on the forward holdout without losing a single win, and match FXC's
record everywhere the rivals react. The 7 forward-holdout flips of F2FRSC3 against 0 reversals give a one-sided sign test p of 0.008.
The frozen pick rule chose F1FRSC3 (better head to head); F2FRSC3 went into the second submission slot 15 hours later. In the final
tournament the two finished 7 points apart (4,457.8 and 4,450.8).

## What the tests could not see

- **Rivals that adapt.** Recorded frames replay rivals that cannot react. A rival that changes its wash after seeing our replays would
  blunt the front-run.
- **Load.** In one lab game run alongside 8 to 12 others, a single turn took 3.06 s. Kaggle allows 1 s per turn plus 60 s of total
  overage, so this is a margin, not a failure, but it was never measured on Kaggle's hardware under load.
- **The top of the ladder.** Against 2,700+ bots both candidates kept FXC's 25-65 record exactly. The layers do not touch that gap.

## Final day

On 30 September a last round ran on Kaggle's free CPU: a census of 200 of our lost games (200 of 200 money ledgers reproduced exactly),
a screen of five fresh public references (each lost 0-40 to the submitted bot), and two repair diagnostics. No new candidate qualified,
so the pair above was kept rather than spending the last upload on an unproven change.
