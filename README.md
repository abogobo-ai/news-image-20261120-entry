# The World Today — Friday, 20 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-news--image--20261120-blue)](https://make.fun/bounty/news-image-20261120)
[![rank](https://img.shields.io/badge/rank-top%2050-brightgreen)](https://make.fun/bounty/news-image-20261120)
[![reward](https://img.shields.io/badge/reward-%24250%20USDC-gold)](https://make.fun/bounty/news-image-20261120)

**32 stories, 13 drawn illustrations — the world in one picture.**

Entry for the make.fun competition
[news-image-20261120](https://make.fun/bounty/news-image-20261120):
*"Sum up 20 November's world news in one image."*

## The image

`entry.png` — a 1024×1024 front page, **THE WORLD TODAY**,
dated **FRIDAY, 20 NOVEMBER 2026**, drawn entirely with a procedural
Python/PIL generator (`build.py`, no downloaded assets, no photographs).

- **3 lead stories**, each with its own drawn scene illustration:
  1. Trump pushes the Iran war decision to 2027
  2. Anthropic's record IPO closes its first day up 17%
  3. Cyclone Akvan — 300,000 evacuated as the storm nears Odisha
- **10 mid stories**, each with a drawn icon (60px+).
- **19 briefs** across politics, markets, tech, science, culture and sport.
- A numbered world map, region strip, stat strip, UTC timeline,
  a DATE CHECK box and a sources footer.

Every story in the image happened or was first reported on
**20 November 2026**; the full audited list with sources is in
[`news20-data.txt`](news20-data.txt).

## Build

```sh
python3 build.py        # regenerates entry.png (deterministic: same sha256 every run)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts   # copies entry.png to out/entry.png
```

`main.ts` uses only the Node standard library: it copies `entry.png`
next to it into `$MAKEFUN_OUTPUT_DIR/entry.png`.

## License

MIT — see [LICENSE](LICENSE).
