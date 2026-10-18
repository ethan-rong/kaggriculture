<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Kaggriculture: a market-microstructure bot. Bronze medal, 702nd of 10,148 teams.">
</p>

<p align="center">
  <a href="https://www.kaggle.com/competitions/kaggriculture">Competition</a> ·
  <a href="docs/how-it-works.md">How it works</a> ·
  <a href="docs/evaluation.md">How we tested it</a> ·
  <a href="docs/our-changes.patch">Our diff</a> ·
  <a href="#credits">Credits</a>
</p>

A market-microstructure bot for Kaggle's [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture), a two-player farming game
decided in a shared market. It finished **702nd of 10,148 teams** and won a **bronze medal**.

The edge is three market layers that read the rival's trades from public data and act one step ahead of them. They run on top of
tetsutani's public Apache-2.0 bot, X2; all 893 of our lines are in [`docs/our-changes.patch`](docs/our-changes.patch).

## Result

| Final standing | **702nd of 10,148 teams** · bronze medal · top 7% |
|---|---|
| Final tournament score | 4,457.8 |
| Head to head vs our previous best bot | **91-9** over 100 paired games |
| Forward holdout, live games after the freeze | **7 losses turned into wins, 0 wins lost** |
| Final check, 30 Sep, vs five fresh public bots | **200-0** |

## The game in 30 seconds

Two farms share one town and one market for 720 steps (30 days of 24 hours). Each player plants crops, raises animals, hires hands and
sells. Selling pushes a product's price down; the town buys products back on a fixed clock, which pushes it up again. The richer farm
after day 30 wins.

## The idea

Every 4 steps the town eats about 3 units of WHEAT, right after both players' market orders run. Wheat held across that moment sells
back higher than it was bought: a tenth of a coin per unit, about 110 times a game.

Late in the competition, much of the field ran the same trade on the same clock. That makes the clock predictable, and a predictable
trade can be front-run. The edge moves to **order and timing**: which queue slot trades first, who holds and who closes, and who sees
the other coming. Our layers work at that level.

<p align="center">
  <img src="assets/layers.svg" width="88%" alt="Layer diagram: three market layers of ours on top of the public X2 bot and its upstream lineage.">
</p>

| layer | what it does | evidence |
|---|---|---|
| **Front-run** | Infers the rival's trades from market inventory and money; buys one step before its wash and sells into it from queue slot 9 | +66 to +79 coins per hit |
| **Order safety** | Keeps the wash out of orders a same-step closer could exploit | +225 to +348 coins per game where it fires |
| **Tick wash** | Holds wheat across the town's consumption tick and sells the largest-stake lots first, invisible to the bot below | 9 of 19 lost games turned into wins in replay |
| **Patches in the base** | Stuck-pasture rebuild, earlier wool lots, same-step close of scripted washes, later premium reservation | 25 losses turned into wins, 0 wins lost, on 166 recorded games |

The engine rules behind each step, and every number, are in [**How it works**](docs/how-it-works.md).

## How we tested it

Every candidate had to pass bars written down before its first game: recorded ladder games replayed with the candidate in our seat,
closed-loop pools where the rivals react, a head-to-head against the previous bot, a timing gate, and a forward holdout of live games
played after the code was frozen.

| gate (vs the previous bot) | result |
|---|---|
| 459 recorded ladder games | 5 losses turned into wins, 0 wins lost |
| 100 paired games head to head | 91-9 |
| 480-game holdout pool | 476-4 |
| 38 live games after the freeze | 7 losses turned into wins, 0 wins lost |
| slowest quiet turn × 3.8 | 0.62 s, inside the 1 s limit |

Full tables: [**How we tested it**](docs/evaluation.md).

## The climb

<p align="center">
  <img src="assets/campaign.svg" width="100%" alt="All 88 submissions by date and ladder rating, from 525 in August to the top 5% line in late September.">
</p>

From a first rating of 525 to the top-5% line in 44 days, over 88 submissions:

1. **Own engine.** A day planner that values every task by net present value, and one greedy dispatcher over every (worker, task)
   pair. Written from scratch in four days.
2. **The strongest public bases** as the platform, with every change of ours gated on our own bench.
3. **Market layers.** Three layers, each built from a loss autopsy, gated and shipped in two days.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python play.py                          # one game vs Kaggle's starter bot
python play.py --opponent self --seed 7
python play.py --games 10 --opponent random
```

On a MacBook, seed 1 ends 138,369 to 3,824 against the starter bot, with a slowest turn of 0.90 s.

## Layout

```
submission/main.py      the file that was scored (sha256 b00d2fbf…)
submission/LICENSE.txt  Apache-2.0, as shipped
submission/NOTICE.txt   upstream attribution, as shipped
play.py                 play it locally with kaggle-environments 1.32.7
docs/how-it-works.md    engine facts and every layer
docs/evaluation.md      test design and every gate number
docs/our-changes.patch  our 893 lines as a diff against the public X2 file
docs/submissions.csv    all 88 submissions: date, ladder rating, phase
assets/                 banner and diagrams
```

Applying the patch to the public X2 `main.py` rebuilds `submission/main.py` byte for byte.

<details>
<summary>Checksums</summary>

| file | sha256 |
|---|---|
| `submission/main.py` | `b00d2fbfd08456c55f490542dc8c36df81b1f24b6395f1481fc01a8a28ce70ff` |
| `submission/LICENSE.txt` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| `submission/NOTICE.txt` | `82f3cbdc5ee3b4dbbad054b2ba703a8370b6431af573adf10ad92964421e6ea7` |
| submitted archive | `f54bf576b001024b2beec2726ca7bb6b056e561c48f6df37f48ecfeff5333270` |
| public X2 `main.py` (base of the patch) | `55be5d5f124c8daaaa63c1a29ba4aab096004909666f04748007603c67b7d2a8` |

</details>

## Credits

The base bot comes from public Kaggle notebooks, all Apache-2.0:

- **tetsutani**: [Demand-Preserving Turn Sale Timing](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing), the direct base
- **shiiin9**: [Your Market List Is an Order Book](https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book)
- **Ahmed Berat Ozer**: the V55 controller and [V56 Smarter Seeds and Fertilizer](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer)
- **Thomas Tschinkel**: [the public state router](https://www.kaggle.com/code/thomastschinkel/kaggriculture-93-8-win-rate-public-state-router) and Metav4
- **Yusuke Hayashi (yhay81)**: the [Shop Router](https://www.kaggle.com/code/yhay81/shop-router-0913) line
- **nathanjacob**: [Pipe-16 idle workers](https://www.kaggle.com/code/nathanjacob/kaggriculture-pipe16-idle-workers)
- **Dmitrii Gluzdov**: the seven-turn rescue and its integration
- **aurax7**: the Reactive Router's sale timing and shed projection
- **prvsiyan** (production and timing) and **destbreso**
- **Kaggle and the kaggle-environments contributors**: the game engine

The full chain of notices is in [`submission/NOTICE.txt`](submission/NOTICE.txt) and at the top of
[`submission/main.py`](submission/main.py).

## License

[Apache-2.0](LICENSE), inherited from the upstream bots. Our documents, `play.py` and the diagrams are released under the same license.
