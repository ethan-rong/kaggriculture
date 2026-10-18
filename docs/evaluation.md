# How we tested it

Every candidate was judged locally, by rules written down before its first game. A new bot needs 100+ ladder games to settle, so the
local bench gives a sharper answer in hours instead of days.

## Rules first, numbers second

- Each candidate's bars, opponent pools and seed blocks were written to a file before any game was played. A rule change was logged
  as a numbered amendment, before the numbers it would affect.
- A seed block is used once. Used blocks go on a burned list that every later run checks.
- The pick rule between passing candidates was also fixed in advance, so the final choice is mechanical.

## Three kinds of evidence

| kind | what it is | what it proves |
|---|---|---|
| **Recorded frames** | A live ladder game rebuilt step by step with the engine's own functions: the candidate plays our seat, the rival replays its recorded actions. With no change, the rebuild reproduces both players' money after every step. | The change wins real games, against real opponents, in real worlds. |
| **Closed-loop pools** | Full engine games, both seats, paired seeds, against a population of public forks and our own earlier bots. | The bot keeps winning when rivals react. |
| **Forward holdout** | Live games that ended after the candidate's code was frozen. | The gain holds on data the candidate never saw. |

Timing is a gate of its own: the slowest turn in a quiet run, times a 3.8 safety factor for Kaggle's slower CPU, must stay under
Kaggle's 1 s limit.

## Final gates

Every number below is against FXC, the previous bot, on identical jobs. F2FRSC3 is the submitted bot; F1FRSC3 is its one-line twin.

| gate | bar | F2FRSC3 | F1FRSC3 | FXC |
|---|---|---|---|---|
| Screen: 459 recorded ladder frames | net flips ≥ +3, margin ≥ 0 | +5 (+5 / −0), +169.8K | +5 (+5 / −0), +164.4K | 401-0-58 |
| Training pool: 240 games | ≥ FXC − 1 pp | 238-2 | 238-2 | 238-2 |
| Head to head vs FXC: 100 paired games | win rate ≥ 0.55 | **91-9** | **100-0** | |
| Holdout pool: 480 games | ≥ FXC − 2 pp, every opponent ≥ 0.35 | 476-4, worst opponent 0.95 | 476-4, worst 0.95 | 476-4 |
| Holdout pool: 80 games | losses ≤ FXC + 2 | 79-1 | 79-1 | 79-1 |
| Timing: quiet max turn × 3.8 | < 1.0 s | 0.622 s | 0.614 s | 0.610 s |
| Forward holdout: 38 live games (veto) | net ≥ 0 | **+7 (+7 / −0), +79.6K** | +6 (+6 / −0), +77.8K | 20-0-18 |

Both candidates turn losses into wins on recorded frames and on the forward holdout without giving up a single win. The 7
forward-holdout flips of F2FRSC3 against 0 reversals give a one-sided sign test p of 0.008. Both went into the final pair; in the final
tournament they scored 4,457.8 and 4,450.8.

## Final check

On 30 September the submitted bot played five fresh public bots, 40 games each, on Kaggle's own CPU: **200-0**. A replay of 200
earlier games reproduced every money ledger exactly, confirming the bench matches the live engine.
