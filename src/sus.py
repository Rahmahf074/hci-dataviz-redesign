"""Hitung skor SUS (System Usability Scale) + metrik tugas usability test.

responses.csv : participant,q1..q10   (skala 1-5)
tasks.csv     : participant,task,time_sec,success   (success: 1/0)  [opsional]
"""
import argparse

import pandas as pd


def sus_scores(df: pd.DataFrame) -> pd.Series:
    q = df[[f"q{i}" for i in range(1, 11)]]
    if not q.apply(lambda c: c.between(1, 5)).all().all():
        raise ValueError("Semua jawaban SUS harus 1-5")
    odd = q[[f"q{i}" for i in (1, 3, 5, 7, 9)]] - 1       # item positif
    even = 5 - q[[f"q{i}" for i in (2, 4, 6, 8, 10)]]     # item negatif
    return (odd.sum(axis=1) + even.sum(axis=1)) * 2.5


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--responses", default=None, help="CSV jawaban SUS (opsional, untuk antarmuka interaktif)")
    ap.add_argument("--tasks", default=None, help="CSV tugas: participant,version,task,time_sec,success")
    a = ap.parse_args()
    if not a.responses and not a.tasks:
        ap.error("isi --tasks dan/atau --responses")
    if a.responses:
        r = pd.read_csv(a.responses)
        s = sus_scores(r)
        print(pd.DataFrame({"participant": r["participant"], "SUS": s}).to_string(index=False))
        print(f"\nn={len(s)}  mean SUS={s.mean():.1f}  sd={s.std(ddof=1):.1f}")
        print("Pembanding yang umum dikutip: rata-rata SUS sekitar 68. Dengan n kecil, jangan klaim signifikan.")
    if a.tasks:
        t = pd.read_csv(a.tasks)
        print("\nPer tugas:")
        keys = ["version", "task"] if "version" in t.columns else ["task"]
        print(t.groupby(keys).agg(success_rate=("success", "mean"), mean_time_sec=("time_sec", "mean"), n=("participant", "nunique")).round(2).to_string())