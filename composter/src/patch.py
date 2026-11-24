from pathlib import Path
from shutil import copyfile
import streamlit as st
import re


ICON_VERSION = 2


def patch_index(title: str, desc: str) -> None:
    static_dir = Path(st.__file__).parent / "static"
    index_path = static_dir / "index.html"
    html = index_path.read_text(encoding="utf-8")
    html = html.replace("<title>Streamlit</title>", f'<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="https://composter.bigman7305.dev/">')
    html = re.sub(r"favicon\.png(\?v=\d+)?", f"favicon.png?v={ICON_VERSION}", html)
    index_path.write_text(html, encoding="utf-8")
    copyfile(Path(__file__).parent.parent / "assets" / "favicon.png", static_dir / "favicon.png")


def main() -> None:
    patch_index("Composter Tools | bigman7305.dev", "A compost calculator tool for Hypixel Skyblock with Optimal Upgrades, Compost Rates, and more!")


if __name__ == "__main__":
    main()