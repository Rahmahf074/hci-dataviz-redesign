"""Redesign visualisasi: pie 'berantakan' -> bar terurut berfokus (prinsip Gestalt, preattentive, WCAG).

Data contoh (data/sample_tickets.csv) adalah DATA SINTETIS untuk demonstrasi, bukan data nyata.
"""
import argparse
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE, HIGHLIGHT, TEXT, BG = "#6B7280", "#B91C1C", "#111827", "#FFFFFF"


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def before(df, out):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(df["value"], labels=None, colors=plt.cm.tab20.colors[: len(df)])
    ax.legend(df["category"], loc="center left", bbox_to_anchor=(1.0, 0.5))  # legend jauh dari data
    ax.set_title("Tickets")  # judul tidak informatif
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)


def after(df, out, top_k=2):
    d = df.sort_values("value")
    total = d["value"].sum()
    share = d["value"].tail(top_k).sum() / total * 100
    names = " and ".join(d["category"].tail(top_k)[::-1])
    colors = [BASE] * (len(d) - top_k) + [HIGHLIGHT] * top_k   # satu atribut preattentive: warna
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(d["category"], d["value"], color=colors)
    for y, v in enumerate(d["value"]):                          # label langsung, tanpa legend
        ax.text(v + total * 0.005, y, f"{v:,}", va="center", color=TEXT, fontsize=10)
    title = textwrap.fill(f"{names} account for {share:.0f}% of support tickets", 48)
    fig.suptitle(title, x=0.02, ha="left", color=TEXT, fontsize=13, fontweight="bold")
    ax.set_xlabel("Tickets"); ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, d["value"].max() * 1.12)
    fig.tight_layout(rect=[0, 0, 1, 0.9]); fig.savefig(out, dpi=140); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/sample_tickets.csv", help="kolom: category,value")
    a = ap.parse_args()
    df = pd.read_csv(a.csv)
    Path("results").mkdir(exist_ok=True)
    before(df, "results/before_pie.png"); after(df, "results/after_bar.png")
    print(f"Contrast bar abu-abu vs background : {contrast_ratio(BASE, BG):.2f}:1 (target >= 3:1, WCAG 1.4.11)")
    print(f"Contrast bar highlight vs background: {contrast_ratio(HIGHLIGHT, BG):.2f}:1 (target >= 3:1)")
    print(f"Contrast teks vs background         : {contrast_ratio(TEXT, BG):.2f}:1 (target >= 4.5:1, WCAG 1.4.3)")
    print("Catatan: warna merah-vs-abu saja tidak cukup untuk buta warna; nilai tetap ditulis di label.")
