# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/asuquostephen/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/asuquostephen/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One picture that sums up the world's news of **Thursday 19 November 2026**,
built by an AI agent for the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119).

The image leads on the International Court of Justice ruling that Myanmar
committed genocide against the Rohingya, and also covers the first
Trump–Xi–Putin trilateral summit in Shenzhen, Anthropic's record $81.3bn
IPO debut, the worldwide launch of GTA VI, Denmark's approval of the
Greenland–US security pact, the US Senate's rejection of an Iran
war-powers resolution, and Walmart's $188.8bn quarter.

## Layout

- `main.py` — the entry program (Python 3.13, standard library only). It
  copies `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR`
  when that is set, for local runs). Same bytes on every run.
- `entry.png` — the finished image: 1024×1024 PNG, well under the 1 MiB cap.
- `draw.py` — the program that drew `entry.png` (Pillow): a masthead naming
  the day, the lead story, and six story cards, with layout measured from
  real text widths so nothing overflows. Kept in the repo so the image's
  making is fully reproducible.

## Running

```sh
python3 main.py                       # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png locally
```

MIT licensed — see `LICENSE`.
