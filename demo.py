"""
evaluate.py  —  Runs all 3 strategies, computes metrics, saves charts.
Usage: python evaluate.py
"""

import os, time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, ConfusionMatrixDisplay,
)
from phishing_detector import classify_email, STRATEGIES, MODEL

DATA_PATH   = "data/sample_emails.csv"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_emails(path):
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} emails  "
          f"({(df.label=='phishing').sum()} phishing, "
          f"{(df.label=='legitimate').sum()} legitimate)")
    return df


def run_evaluation(df, strategy):
    print(f"\n{'='*56}\n  Strategy: {strategy.upper()}\n{'='*56}")
    records = []
    for _, row in df.iterrows():
        text   = f"Subject: {row['subject']}\n\n{row['body']}"
        result = classify_email(text, strategy)
        correct = (row["label"] == result["classification"])
        records.append({
            "id": row["id"], "true_label": row["label"],
            "predicted": result["classification"],
            "confidence": result["confidence"],
            "reasoning": result.get("reasoning", ""),
            "correct": correct,
        })
        print(f"  {'✓' if correct else '✗'} [{row['id']:>2}] "
              f"{row['label']:<12} → {result['classification']:<12} "
              f"conf={result['confidence']:.2f}")
        time.sleep(0.2)
    return pd.DataFrame(records)


def compute_metrics(results, strategy):
    valid  = results[results["predicted"] != "error"]
    y_true = valid["true_label"].map({"phishing": 1, "legitimate": 0})
    y_pred = valid["predicted"].map({"phishing": 1, "legitimate": 0})
    m = {
        "strategy":  strategy,
        "accuracy":  accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall":    recall_score(y_true, y_pred, zero_division=0),
        "f1":        f1_score(y_true, y_pred, zero_division=0),
        "n": len(valid), "errors": (results["predicted"] == "error").sum(),
    }
    print(f"\n  Accuracy={m['accuracy']:.3f}  Precision={m['precision']:.3f}"
          f"  Recall={m['recall']:.3f}  F1={m['f1']:.3f}")
    return m


def plot_results(all_metrics, all_results):
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle(
        f"LLM Phishing Detection — Prompting Strategy Comparison\n"
        f"Model: {MODEL} (Ollama)  |  Dataset: 30 emails",
        fontsize=13, fontweight="bold", y=1.01)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.48, wspace=0.35)
    strategies  = [m["strategy"] for m in all_metrics]
    colors      = ["#2196F3", "#4CAF50", "#FF9800"]
    metric_keys = ["accuracy", "precision", "recall", "f1"]

    ax0 = fig.add_subplot(gs[0, :2])
    x, width = np.arange(len(metric_keys)), 0.25
    for i, (m, col) in enumerate(zip(all_metrics, colors)):
        vals = [m[k] for k in metric_keys]
        bars = ax0.bar(x + i*width, vals, width,
                       label=m["strategy"].replace("_","-"),
                       color=col, alpha=0.85, edgecolor="white")
        for bar, val in zip(bars, vals):
            ax0.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.012,
                     f"{val:.2f}", ha="center", va="bottom", fontsize=7.5)
    ax0.set_ylim(0, 1.15); ax0.set_xticks(x+width)
    ax0.set_xticklabels(metric_keys, fontsize=10)
    ax0.set_title("Performance Metrics by Prompting Strategy", fontsize=11)
    ax0.set_ylabel("Score"); ax0.legend(loc="lower right")
    ax0.yaxis.grid(True, alpha=0.3); ax0.set_axisbelow(True)

    ax1 = fig.add_subplot(gs[0, 2])
    avg  = [all_results[s]["confidence"].mean() for s in strategies]
    bars = ax1.bar(range(len(strategies)), avg, color=colors, alpha=0.85, edgecolor="white")
    for bar, val in zip(bars, avg):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.008,
                 f"{val:.2f}", ha="center", va="bottom", fontsize=9)
    ax1.set_ylim(0, 1.1); ax1.set_xticks(range(len(strategies)))
    ax1.set_xticklabels([s.replace("_","\n") for s in strategies], fontsize=8)
    ax1.set_title("Avg Confidence Score"); ax1.set_ylabel("Confidence")
    ax1.yaxis.grid(True, alpha=0.3); ax1.set_axisbelow(True)

    for i, strategy in enumerate(strategies):
        ax    = fig.add_subplot(gs[1, i])
        res   = all_results[strategy]
        valid = res[res["predicted"] != "error"]
        y_t   = valid["true_label"].map({"phishing":1,"legitimate":0})
        y_p   = valid["predicted"].map({"phishing":1,"legitimate":0})
        disp  = ConfusionMatrixDisplay(confusion_matrix(y_t, y_p),
                                       display_labels=["Legitimate","Phishing"])
        disp.plot(ax=ax, colorbar=False, cmap="Blues")
        ax.set_title(strategy.replace("_","-"), fontsize=9)

    plt.savefig(f"{RESULTS_DIR}/evaluation_results.png", dpi=150, bbox_inches="tight")
    print(f"\nChart saved → {RESULTS_DIR}/evaluation_results.png")
    plt.close()


def main():
    df = load_emails(DATA_PATH)
    all_metrics, all_results = [], {}

    for strategy in STRATEGIES:
        results_df = run_evaluation(df, strategy)
        results_df.to_csv(f"{RESULTS_DIR}/{strategy}_results.csv", index=False)
        all_metrics.append(compute_metrics(results_df, strategy))
        all_results[strategy] = results_df

    summary = pd.DataFrame(all_metrics).round(4)
    summary.to_csv(f"{RESULTS_DIR}/summary_metrics.csv", index=False)
    print("\n" + "="*56 + "\nFINAL SUMMARY\n" + "="*56)
    print(summary[["strategy","accuracy","precision","recall","f1"]].to_string(index=False))
    plot_results(all_metrics, all_results)
    print("\nAll done! Check the results/ folder.")

if __name__ == "__main__":
    main()