# How it works

The final bot is one Python file, [`submission/main.py`](../submission/main.py) (11,025 lines). Lines 1 to ~10,230 are a public
Apache-2.0 bot (X2, see [Credits](../README.md#credits)) with four small patches of ours. The last ~790 lines are three layers we wrote.
Each layer wraps the one below it, and the top three change **market orders only**: no planting, animal, land or hiring decision of the
base bot is touched. [`our-changes.patch`](our-changes.patch) is every line we changed, as a diff against the public file.

## Engine facts the layers rely on

All of these were read from the `kaggle-environments` 1.32.7 source and checked against recorded games: a replay of the market with
these rules reproduces both players' money after every step of every recorded game we tested.

- **Lockstep queues.** Each player sends up to 10 market orders per step. Both players' orders at the same queue index are processed
  together, one unit each per round, at the same quote. Index *i* finishes before index *i* + 1 starts. So for any item, the lower
  index trades first and equal indices tie.
- **Round trips are free.** A BUY is quoted at inventory − 1 and a SELL at inventory. Buying and selling the same units against an
  unchanged market nets exactly 0.
- **The town eats on a clock.** After the market phase of every step *t* with *t* % 4 = 0, the town consumes one unit of each product
  per shop that buys it, plus one more per product at *t* % 24 = 0. For WHEAT that is about 2.6 units per 4-step tick and 3.6 on the
  daily tick (measured on 163 live games).
- **Price.** Below the cap, WHEAT costs 25 + √(10000 − inventory) coins, so one unit moves the price by about 0.04 to 0.06 coins.
- Only WHEAT and FERTILIZER can be bought back from the market. Every other product can only be sold.

## Layer 1: the tick wash

At every step *t* with *t* % 4 = 0 between steps 48 and 712, buy *n* WHEAT and sell the same *n* at *t* + 1. The town's consumption
falls between the two, so the price we sell at is slightly higher than the price we paid: about 0.1 coins per unit, roughly 110 times a
game.

- **Size.** *n* is the free room in the shed, computed so that even if every worker drops everything it carries at *t* + 1, the shed
  still fits. A money guard keeps enough cash for the base bot's own orders at *t* and *t* + 1, plus 300.
- **Hidden from the base bot.** While the wash is held, the base bot is called with a copy of the observation in which the wheat does
  not exist: shed count minus the held units, money plus their cost, market inventory plus the held units. Every inner layer therefore
  decides exactly as it would without the wash.
- **Placement matters more than size.** Many public forks of the same bot wash on the same clock. Whichever side sits at the lower queue
  index captures the other's price impact. Merging our wash into our own same-side WHEAT order, or else placing it right after our last
  sale, beat both "append last" and "index 0" in a market-only replay of 19 lost games: +38.9K coins in total, 9 of 19 losses flipped.
- **Stake sort.** Our own SELL orders are re-sorted into their existing slots by stake: lot size times the price drop the lot itself
  causes, so the lot with the most to lose sells first. Every other order keeps its index. It was the only one of five reorder rules
  that came out positive on 29 lost games (+859 coins); "wool first" lost 6.1K.

## Layer 2: order safety

A replay of the head-to-head games the tick-wash bot lost against its own predecessor found two defects, both in routes whose scripted
plan already washes wheat:

1. **Merge exposure.** The wash was merged into a scripted BUY that the same step also closes. The rival's same-step close then sold into
   our extra units. Fix: never merge the wash into a buy that closes in the same step; place it after the closing sale. Worth +225 to
   +348 coins per game in the affected worlds, 2 flips.
2. **Stake sort jumping a buy.** The stake sort could move a large WHEAT sale ahead of a same-step WHEAT buy, so the sale ran first, sold
   2 of 59 units and held the rest across the tick. Fix: a sale never moves ahead of a same-step buy of the same item.

The layer also closes our whole wash inside the same step while the rival is seen tick-washing (2 of its last 3 tick pairs). Against a
rival that holds across the tick at a lower queue index, holding loses; closing in-step takes its price impact instead.

## Layer 3: front-running the rival's wash

The rival's trades are not in the observation, but its flows can be inferred exactly: its net units bought of a product = our net sale
of it − the town's consumption − the change in market inventory. Its money is public.

- **Front-run.** If the rival tick-washed at 2 of the ticks *t* − 4, *t* − 8 and *t* − 12, buy *m* WHEAT at *t* − 1 and sell it at
  *t* at queue index 9 (the queue is padded with empty `SELL WHEAT 0` orders), after the rival's wash BUY at index 0 or 1. The rival
  then buys at prices our units raised, and we sell into its buying. Measured gain per hit: +66 coins (live games) to +79 (recorded
  frames). If the rival does not wash, the round trip nets 0 by the rules above; observed misses cost 0.4 to 3 coins.
- **Front-run guard.** No own wash at *t* if the rival already net-bought at least 20 WHEAT at *t* − 1 (it is front-running us).
- **Same-step closers.** Some rivals buy at index 0 and sell the same units at index 9 in one step, selling at the top our buy creates.
  Their net flow is 0, so inventory cannot see them. Their money can: net flow 0 in every product while money rose by 10 or more. On
  101 live games this signature fired only on the two known closers, with no false positives. After 3 such events, the layer
  front-runs at *t* − 1 and forces its own same-step close at *t*, selling first.

The submitted bot uses the "2 of the last 3 ticks" trigger. Its twin submission (F1FRSC3) triggers on the last tick alone; that is the
only line that differs (`_X469_CFG`).

## Patches inside the public base

| tag | change | why |
|---|---|---|
| **PF** | Re-issue a pasture or coop build that a day-1 weed blocked | The hand dug the weed instead of building, nothing re-issued the build, and a bought cow waited in the shed about 650 of 720 steps. 1 to 1.6% of games, all of them losses. |
| **W2** | A sheep worker carrying wool skips the optional fertilizer pickup, once the rival has shown a sheep | The pickup delayed every wool lot by 3 steps, so a rival selling the same lot sold first, into the steep part of the price curve. |
| **S1** | Close the scripted wheat washes (BUY at *t*, SELL at *t* + 1) in the same step | Rivals that close in-step captured our held units. |
| **C1** | Premium-lot reservation from step 240 instead of 192; the lead seller works all 24 hours | The two best knobs of a 16-knob search against a population of public forks. |

W2 and S1 together, on 166 recorded live frames: 25 losses flipped, 0 wins lost, +119.6K coins. Recorded frames cannot react, so these
are upper bounds; the closed-loop pools in [evaluation.md](evaluation.md) are the real check.

## What the layers do not fix

Against the top-ladder bots (2,700+ rating) the median loss was 11.7K coins. That gap is their economy: what they grow, when they
expand, how many hands they hire. Market timing is worth hundreds of coins per game, not thousands, and no market-only edge we found
moved those games.
