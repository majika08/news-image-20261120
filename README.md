# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/majika08/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/majika08/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world news of **Friday, November 20, 2026**, drawn entirely
by a program: every letter, flag and pictogram in `entry.png` is rendered in code
(Python/PIL), so the text is crisp and nothing is left to an image model.

The day's main stories, in one 1024×1024 panel grid:

1. **Russia unleashes a huge barrage on Ukraine** — more than 400 drones and over
   110 missiles strike Kyiv and nine regions overnight, hours after Putin vowed
   revenge for Ukraine's attacks on the Crimea bridge. Eight people are killed and
   28 injured; three bridges over the Dnipro are hit, embassies and St Volodymyr's
   Cathedral are damaged, and two missiles and a drone fall inside Poland.
2. **AI sell-off rocks global markets** — Japan's Nikkei plunges 4.8% to a
   seven-month low as AI and chip shares are dumped (SoftBank −14.6%, Kospi −5.2%,
   Taiwan −6%); US stocks fall for a fifth straight day after Anthropic's record debut.
3. **After Shenzhen, Europe pushes back** — Trump tells European leaders and
   Zelenskyy that "Putin wants to end the war"; Europe and Ukraine reject a
   "new Yalta" and insist Kyiv must be part of any peace deal.
4. **Houthi missile damages Riyadh's tallest tower** — windows are blown out across
   eight floors of the PIF Tower, the Saudi wealth fund's HQ; no injuries. On Friday,
   Saudi air defences down another missile and two drones.
5. **COP31 draft drops the fossil-fuel phase-out** — a revised climate draft keeps a
   35% electrification target but deletes the call to phase out fossil fuels.
6. **Kenya declares its Ebola outbreak over** — the last patient is discharged,
   37 days after the first case.
7. **The White House ousts its cyber chief** — Sean Cairncross is fired after a week
   of tech failures at Microsoft, the FAA and banks; officials say there is no sign
   of a coordinated attack.

Footer: Estonia to close its Russian border for at least six months · the EU sends
Ukraine €7.9 billion, its largest single payment yet.

The image was rendered by the Python scripts in `tools/` (`newsart.py` is the
drawing library; `gen_candidates.py` drives it to produce candidate panels — this
entry is its panel-grid candidate). At run time, `main.ts` verifies `entry.png` —
PNG signature, IHDR dimensions, the 1024×1024 and 1 MiB limits, and a full chunk
walk that re-checks every chunk's CRC and ends exactly at IEND — then publishes
the validated bytes, unchanged, to the output directory and prints a one-line
JSON manifest with the image's SHA-256.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, 343,581 bytes), identical to the
`entry.png` in this repository.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
