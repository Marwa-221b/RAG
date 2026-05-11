# evalution/metrics.py
import json
import os
from datetime import datetime


def load_results(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "evaluation_results.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_metrics(data):
    results = data["results"]
    total = len(results)

    # ── Core Metrics ──
    passed          = sum(1 for r in results if r.get("passed"))
    source_correct  = sum(1 for r in results if r.get("source_retrieved") is True)
    hallucinations  = sum(1 for r in results if r.get("hallucination") is True)
    answer_correct  = sum(1 for r in results if r.get("answer_correct") is True)
    errors          = sum(1 for r in results if "error" in r)
    avg_time        = sum(r.get("response_time_s", 0) for r in results) / total

    # ── Per-Difficulty Breakdown ──
    difficulty_groups = {}
    for r in results:
        d = r.get("difficulty", "Unknown")
        difficulty_groups.setdefault(d, {"total": 0, "passed": 0})
        difficulty_groups[d]["total"] += 1
        if r.get("passed"):
            difficulty_groups[d]["passed"] += 1

    # ── Keyword Coverage ──
    keyword_scores = []
    for r in results:
        kw = r.get("keywords_found", "0/0")
        found, total_kw = map(int, kw.split("/"))
        if total_kw > 0:
            keyword_scores.append(found / total_kw)
    avg_keyword_coverage = (sum(keyword_scores) / len(keyword_scores) * 100) if keyword_scores else 0

    # ── Slowest queries ──
    sorted_by_time = sorted(results, key=lambda x: x.get("response_time_s", 0), reverse=True)

    metrics = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_queries": total,
        "pass_rate":             f"{passed}/{total} ({passed/total*100:.0f}%)",
        "retrieval_accuracy":    f"{source_correct}/{total} ({source_correct/total*100:.0f}%)",
        "answer_accuracy":       f"{answer_correct}/{total} ({answer_correct/total*100:.0f}%)",
        "hallucination_rate":    f"{hallucinations}/{total} ({hallucinations/total*100:.0f}%)",
        "keyword_coverage":      f"{avg_keyword_coverage:.0f}%",
        "avg_response_time_s":   round(avg_time, 2),
        "slowest_query_s":       sorted_by_time[0].get("response_time_s"),
        "fastest_query_s":       sorted_by_time[-1].get("response_time_s"),
        "errors":                errors,
        "difficulty_breakdown":  difficulty_groups,
    }
    return metrics


def print_metrics(metrics):
    print("\n" + "=" * 55)
    print("   RAG SYSTEM — METRICS REPORT")
    print(f"   Generated: {metrics['generated_at']}")
    print("=" * 55)

    print("\n  CORE METRICS")
    print(f"  {'Pass Rate':<30} {metrics['pass_rate']}")
    print(f"  {'Retrieval Accuracy':<30} {metrics['retrieval_accuracy']}")
    print(f"  {'Answer Accuracy':<30} {metrics['answer_accuracy']}")
    print(f"  {'Hallucination Rate':<30} {metrics['hallucination_rate']}")
    print(f"  {'Keyword Coverage':<30} {metrics['keyword_coverage']}")

    print("\n  PERFORMANCE")
    print(f"  {'Avg Response Time':<30} {metrics['avg_response_time_s']}s")
    print(f"  {'Slowest Query':<30} {metrics['slowest_query_s']}s")
    print(f"  {'Fastest Query':<30} {metrics['fastest_query_s']}s")

    print("\n  BREAKDOWN BY DIFFICULTY")
    for diff, counts in metrics["difficulty_breakdown"].items():
        pct = counts["passed"] / counts["total"] * 100
        bar = "█" * counts["passed"] + "░" * (counts["total"] - counts["passed"])
        print(f"  {diff:<22} {bar}  {counts['passed']}/{counts['total']} ({pct:.0f}%)")

    print("=" * 55)


def save_metrics_md(metrics, results):
    lines = []
    lines.append("# RAG System — Metrics Report")
    lines.append(f"\nGenerated: {metrics['generated_at']}\n")

    lines.append("## Core Metrics\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Pass Rate | {metrics['pass_rate']} |")
    lines.append(f"| Retrieval Accuracy | {metrics['retrieval_accuracy']} |")
    lines.append(f"| Answer Accuracy | {metrics['answer_accuracy']} |")
    lines.append(f"| Hallucination Rate | {metrics['hallucination_rate']} |")
    lines.append(f"| Keyword Coverage | {metrics['keyword_coverage']} |")
    lines.append(f"| Avg Response Time | {metrics['avg_response_time_s']}s |")
    lines.append(f"| Slowest Query | {metrics['slowest_query_s']}s |")
    lines.append(f"| Fastest Query | {metrics['fastest_query_s']}s |")

    lines.append("\n## Breakdown by Difficulty\n")
    lines.append("| Difficulty | Passed | Total | Pass Rate |")
    lines.append("|------------|--------|-------|-----------|")
    for diff, counts in metrics["difficulty_breakdown"].items():
        pct = counts["passed"] / counts["total"] * 100
        lines.append(f"| {diff} | {counts['passed']} | {counts['total']} | {pct:.0f}% |")

    lines.append("\n## Detailed Query Results\n")
    lines.append("| ID | Query | Source OK | Keywords | Hallucination | Time(s) | Result |")
    lines.append("|----|-------|-----------|----------|---------------|---------|--------|")
    for r in results:
        query_short = r["query"][:45] + "..." if len(r["query"]) > 45 else r["query"]
        src    = "Yes" if r.get("source_retrieved") is True else ("N/A" if r.get("source_retrieved") is None else "No")
        kw     = r.get("keywords_found", "---")
        hallu  = "Yes" if r.get("hallucination") else "No"
        time_s = r.get("response_time_s", "---")
        result = "PASS" if r.get("passed") else "FAIL"
        lines.append(f"| {r['id']} | {query_short} | {src} | {kw} | {hallu} | {time_s} | {result} |")

    lines.append("\n## Analysis\n")
    lines.append("**Strengths:**")
    lines.append("- Easy queries (salary, certifications, named person lookup) achieved 100% pass rate")
    lines.append("- DOCX and HTML parsing both worked correctly (Queries 2, 9)")
    lines.append("- Cross-document retrieval succeeded for Splunk candidate lookup (Query 6)\n")
    lines.append("**Weaknesses:**")
    lines.append("- Arabic query (Query 10) failed retrieval due to monolingual embedding model")
    lines.append("- Aggregation queries (Query 7) missed candidates — fundamental top_k limitation")
    lines.append("- Average response time of 26.94s is high for production use")
    lines.append("- Query 5 missed QRadar keyword — chunk boundary split the SIEM list\n")
    lines.append("**Key Finding:**")
    lines.append("Retrieval accuracy (70%) exceeds answer accuracy (60%), meaning the bottleneck")
    lines.append("is the LLM not fully utilizing retrieved context rather than retrieval itself.")

    out_path = os.path.join(os.path.dirname(__file__), "metrics_report.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n  Markdown report saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    data    = load_results()
    metrics = compute_metrics(data)
    print_metrics(metrics)
    save_metrics_md(metrics, data["results"])