"""The README's header: the front page of The Hooks Daily, into .github/readme-header.png."""
import os, subprocess
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from x_assets import HERE, RED, INK, PAPER, anton, franklin, text_path, mark

MUTED, LINE = "#675f55", "#cbc2b2"
ROOT = os.path.abspath(f"{HERE}/../..")
news = TTFont(f"{HERE}/fonts/NewsreaderItalic.ttf")
if "fvar" in news:
    axes = {a.axisTag: a for a in news["fvar"].axes}
    news = instantiateVariableFont(news, {t: (400 if t == "wght" else axes[t].defaultValue) for t in axes})

W, H, M = 1600, 760, 72
parts = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']


def centered(font, text, size, y, fill, tracking=0.0):
    d, w = text_path(font, text, size, tracking)
    parts.append(f'<path transform="translate({(W - w) / 2:.1f},{y})" d="{d}" fill="{fill}"/>')
    return w


def fit(font, text, size, tracking=0.0):
    """The largest size up to `size` at which `text` fits between the margins."""
    _, w = text_path(font, text, size, tracking)
    return min(size, size * (W - 2 * M) / w)


# Motto above the flag.
centered(franklin, "THE DEGENS' FAVORITE PAPER · ALL THE SOVEREIGN DEBT THAT FITS IN A MEME", 18, 58, INK, 0.1)

# The flag: red band between two ink rules, as on the app's front page.
top, bot, rule = 84, 316, 10
parts.append(f'<rect x="0" y="{top}" width="{W}" height="{bot - top}" fill="{RED}"/>')
parts.append(f'<rect x="0" y="{top}" width="{W}" height="{rule}" fill="{INK}"/>')
parts.append(f'<rect x="0" y="{bot - rule}" width="{W}" height="{rule}" fill="{INK}"/>')

size = 150
d1, w1 = text_path(anton, "THE HOOKS", size, 0.01)
d2, w2 = text_path(anton, "DAILY", size, 0.01)
box_w, box_h, gap = 140, 106, 28
x0 = (W - (w1 + gap + box_w + gap + w2)) / 2
base = (top + bot) / 2 + 0.735 * size / 2  # Anton's cap height


def word(d, x):
    sk = f"translate({x:.1f},{base:.1f}) skewX(-10)"
    return (f'<path transform="translate(7,7) {sk}" d="{d}" fill="{INK}"/>'
            f'<path transform="{sk}" d="{d}" fill="{PAPER}" stroke="{INK}" stroke-width="4" paint-order="stroke" stroke-linejoin="round"/>')


parts.append(word(d1, x0))
bx, by = x0 + w1 + gap, (top + bot) / 2 - box_h / 2
parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{box_w}" height="{box_h}" fill="{INK}"/>')
parts.append(f'<rect x="{bx + 10:.1f}" y="{by + 10:.1f}" width="{box_w - 20}" height="{box_h - 20}" fill="none" stroke="{PAPER}" stroke-width="4"/>')
parts.append(mark(bx + box_w / 2, by + box_h / 2, box_w * 0.62, PAPER))
parts.append(word(d2, bx + box_w + gap))

# Edition line, justified between the margins and closed by a rule.
items = ["STELLAR EDITION", "MEMECOINS BACKED BY BONDS", "CETES · TESOURO", "WEATHER: BONDS UP", "FREE"]
paths = [text_path(franklin, s, 18, 0.08) for s in items]
slash_d, slash_w = text_path(franklin, "/", 18)
step = (W - 2 * M - sum(w for _, w in paths)) / (len(items) - 1)
x, y = M, 356
for i, (d, w) in enumerate(paths):
    parts.append(f'<path transform="translate({x:.1f},{y})" d="{d}" fill="{INK}"/>')
    if i < len(items) - 1:
        parts.append(f'<path transform="translate({x + w + (step - slash_w) / 2:.1f},{y})" d="{slash_d}" fill="{MUTED}"/>')
    x += w + step
parts.append(f'<rect x="{M}" y="376" width="{W - 2 * M}" height="2" fill="{INK}"/>')

# The lead story: kicker, headline, deck.
centered(franklin, "LAST MINUTE", 20, 428, RED, 0.12)
head = "EVERY MEME BUYS SOVEREIGN DEBT"
hs = fit(anton, head, 128, 0.005)
hy = 428 + 34 + 0.735 * hs
centered(anton, head, hs, hy, INK, 0.005)
deck = ["Memecoins on Stellar whose reserve sits in Mexican and Brazilian bonds, not idle XLM.",
        "The reserve earns the bond's yield, and holders are paid in it on every trade."]
ds = min(fit(news, s, 36) for s in deck)
for i, s in enumerate(deck):
    centered(news, s, ds, hy + 58 + i * ds * 1.3, "#3b3630")

# Foot: a double rule and the address.
fy = H - 78
parts.append(f'<rect x="{M}" y="{fy}" width="{W - 2 * M}" height="4" fill="{INK}"/>')
parts.append(f'<rect x="{M}" y="{fy + 8}" width="{W - 2 * M}" height="1" fill="{INK}"/>')
centered(franklin, "READ IT LIVE ON TESTNET  ·  HOOKS.UP.RAILWAY.APP", 18, H - 34, INK, 0.1)

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{"".join(parts)}</svg>'
os.makedirs(f"{ROOT}/.github", exist_ok=True)
open(f"{HERE}/build/readme-header.svg", "w").write(svg)
subprocess.run(["rsvg-convert", "-w", str(W * 2), "-h", str(H * 2), f"{HERE}/build/readme-header.svg",
                "-o", f"{ROOT}/.github/readme-header.png"], check=True)
print("headline", round(hs, 1), "deck", round(ds, 1))
