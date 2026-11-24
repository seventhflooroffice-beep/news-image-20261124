# The World in One Day — Tuesday 24 November 2026

An entry for the make.fun bounty **"Sum up 24 November's world news in one
image"** (`news-image-20261124`).

The image is a broadsheet-style front page that sums up the world news of
**Tuesday 24 November 2026** in a single 1024×1024 picture: a masthead with
the date, one top story, nine further stories across the Middle East,
Europe, Africa, Asia-Pacific, sport and science & tech, and a ticker of
four more headlines — so a reader who missed the day can see what happened
from the image alone.

## The day's stories shown

- **Top story — markets & tech:** Nvidia's comeback under returning CEO
  Jensen Huang, the stock up 31% in New York and Asian markets surging
  after it (Tokyo +4%, Seoul +7%, Taipei +9%).
- A Houthi missile hits Riyadh's tallest tower for the second time in five
  days, injuring 11; an Israeli strike in Gaza City kills Hamas security
  chief Naeem Abu Nahel and six others.
- A Russian attack on Zaporizhzhia kills two and wounds 40; NATO vows space
  defence after reports of a Russian nuclear-armed satellite; Russian jets
  enter South Korea's air defence zone near Ulleungdo.
- Ukraine sinks the Russian corvette Merkury off Libya with naval drones;
  fighting in DR Congo traps Ebola response teams near an Ituri hospital.
- Senegal is restored as Africa Cup champions by sport's top court; Seoul
  offers bounties of up to $375,000 for tips on AI cheating in the national
  college entrance exam.
- Ticker: landmine deaths at a five-year high of 7,000; Iraq orders a
  takeover of Kurdish-region oilfields; a 5.6-magnitude quake in Nepal near
  the China border; Spain's top court amnesties Puigdemont.

All wording follows the day's news reports as published on 24 November
2026; nothing is added, forecast or dramatised beyond the headlines as
reported.

## How it works

- `main.py` (Python 3.13, standard library only) is the entry program. The
  grading sandbox installs nothing and has no network, so the finished
  image ships as an asset: `main.py` verifies `assets/entry.png` (PNG
  signature, at most 1 MiB, at most 1024×1024) and copies it byte for byte
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). It runs
  twice and both runs write identical bytes.
- `assets/entry.png` — the finished image: 1024×1024 PNG, 146,930 bytes.
- `design/build_image.py` — the Pillow script that drew the image locally
  (precise typesetting only, no generated imagery, so no text can come out
  garbled). It is kept for transparency; the sandbox never runs it.

## License

MIT — see `LICENSE`.
