# evalution/benchmarks.py
import sys
import os
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from services.retrieval.integration_pip_ret import vector_store_from_pipline
from rag.context_builder import get_context_from_query, set_vector_store
from rag.generator import generate_answer
from core.config import get_llm_config

# ─────────────────────────────────────────
# TEST CASES — based on your actual documents
# ─────────────────────────────────────────
TEST_CASES = [
    {
        "id": 1,
        "query": "What is the salary for the cybersecurity analyst position?",
        "expected_source": "jd_05_cybersecurity_analyst",
        "expected_keywords": ["18,000", "26,000", "AED"],
        "difficulty": "Easy",
        "should_fail": False
    },
    {
        "id": 2,
        "query": "What are the required certifications for the cybersecurity analyst role?",
        "expected_source": "jd_05_cybersecurity_analyst",
        "expected_keywords": ["CEH", "GCIH", "CISSP"],
        "difficulty": "Easy",
        "should_fail": False
    },
    {
        "id": 3,
        "query": "What is James Holloway's current job title and company?",
        "expected_source": "english_cv_01_software_engineer",
        "expected_keywords": ["TechBridge", "Senior Software Engineer"],
        "difficulty": "Easy",
        "should_fail": False
    },
    {
        "id": 4,
        "query": "How many years of product management experience does Sarah Nguyen have?",
        "expected_source": "english_cv_04_product_manager",
        "expected_keywords": ["7"],
        "difficulty": "Easy",
        "should_fail": False
    },
    {
        "id": 5,
        "query": "What SIEM platforms does SecureNet Global require?",
        "expected_source": "jd_05_cybersecurity_analyst",
        "expected_keywords": ["Splunk", "Sentinel", "QRadar"],
        "difficulty": "Medium",
        "should_fail": False
    },
    {
        "id": 6,
        "query": "Which candidates have experience with Splunk?",
        "expected_source": "english_cv_05_cybersecurity_analyst",
        "expected_keywords": ["Marcus", "Okafor"],
        "difficulty": "Hard",
        "should_fail": False
    },
    {
        "id": 7,
        "query": "List all candidates who know Python",
        "expected_source": None,  # requires ALL cvs
        "expected_keywords": ["Holloway", "Sharma", "Mendes", "Okafor"],
        "difficulty": "Hard",
        "should_fail": False
    },
    {
        "id": 8,
        "query": "What is the experience?",
        "expected_source": None,
        "expected_keywords": [],
        "difficulty": "Designed to fail",
        "should_fail": True  # vague query
    },
    {
        "id": 9,
        "query": "What salary does CloudStack offer the Senior Product Manager?",
        "expected_source": "jd_04_product_manager",
        "expected_keywords": ["145,000", "175,000"],
        "difficulty": "Medium",
        "should_fail": False
    },
    {
        "id": 10,
        "query": "ما هي المهارات المطلوبة للمحلل الأمني؟",
        "expected_source": "jd_05_cybersecurity_analyst",
        "expected_keywords": ["Splunk", "MITRE", "Python", "CrowdStrike"],
        "difficulty": "Designed to fail",
        "should_fail": True  # Arabic query on English docs
    },
]


# ─────────────────────────────────────────
# EVALUATION FUNCTIONS
# ─────────────────────────────────────────

def check_source_retrieved(sources, expected_source):
    """Check if the expected source document appears in retrieved chunks."""
    if expected_source is None:
        return None  # N/A for multi-document queries
    for s in sources:
        src = s.get("source", "") or s.get("metadata", {}).get("source", "")
        if expected_source.lower() in src.lower():
            return True
    return False


def check_keywords_in_answer(answer, keywords):
    """Check how many expected keywords appear in the answer."""
    if not keywords:
        return 0, 0
    answer_lower = answer.lower()
    found = sum(1 for kw in keywords if kw.lower() in answer_lower)
    return found, len(keywords)


def detect_hallucination(answer, sources, keywords):
    """
    Simple hallucination heuristic:
    If answer contains expected keywords but NO source retrieved them,
    the LLM likely answered from training data, not context.
    """
    if not sources or not keywords:
        return False
    
    # Check if any keyword appears in the retrieved chunks
    all_chunk_text = " ".join([
        s.get("chunk", "") for s in sources
    ]).lower()
    
    answer_lower = answer.lower()
    
    for kw in keywords:
        kw_lower = kw.lower()
        # keyword in answer but NOT in any retrieved chunk = hallucination
        if kw_lower in answer_lower and kw_lower not in all_chunk_text:
            return True
    return False


def run_evaluation(folder_path, top_k=5):
    print("=" * 60)
    print("   RAG SYSTEM EVALUATION")
    print("=" * 60)
    print(f"Loading vector store from: {folder_path}")
    print(f"Top-K: {top_k}\n")

    # load vector store once
    vec_store = vector_store_from_pipline(folder_path)
    set_vector_store(vec_store)
    config = get_llm_config()

    results = []

    for tc in TEST_CASES:
        print(f"Running Query {tc['id']}: {tc['query'][:60]}...")
        start = time.time()

        try:
            result = get_context_from_query(tc["query"], top_k=top_k)
            sources = result.get("sources", [])

            # format sources for evaluation
            formatted_sources = []
            for s in sources:
                formatted_sources.append({
                    "source": s.get("metadata", {}).get("source", "unknown"),
                    "chunk": s.get("chunks", "")
                })

            answer = generate_answer(tc["query"], sources, config)
            elapsed = round(time.time() - start, 2)

            # evaluate
            source_ok = check_source_retrieved(formatted_sources, tc["expected_source"])
            found_kw, total_kw = check_keywords_in_answer(answer, tc["expected_keywords"])
            answer_correct = (found_kw == total_kw) if total_kw > 0 else None
            hallucinated = detect_hallucination(answer, formatted_sources, tc["expected_keywords"])

            # pass/fail logic
            if tc["should_fail"]:
                # for designed-to-fail queries, we EXPECT failure
                passed = not answer_correct  # it should get wrong answer
            else:
                passed = (source_ok is not False) and answer_correct

            results.append({
                "id": tc["id"],
                "query": tc["query"],
                "difficulty": tc["difficulty"],
                "expected_source": tc["expected_source"],
                "source_retrieved": source_ok,
                "keywords_found": f"{found_kw}/{total_kw}",
                "answer_correct": answer_correct,
                "hallucination": hallucinated,
                "passed": passed,
                "response_time_s": elapsed,
                "answer_snippet": answer[:200]
            })

            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] Source: {source_ok} | Keywords: {found_kw}/{total_kw} "
                  f"| Hallucination: {hallucinated} | Time: {elapsed}s")

        except Exception as e:
            print(f"  [ERROR] {str(e)}")
            results.append({
                "id": tc["id"],
                "query": tc["query"],
                "difficulty": tc["difficulty"],
                "error": str(e),
                "passed": False
            })

    return results


def print_report(results):
    print("\n" + "=" * 60)
    print("   EVALUATION REPORT")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    source_correct = [r for r in results if r.get("source_retrieved") is True]
    hallucinations = [r for r in results if r.get("hallucination")]
    answer_correct = [r for r in results
                      if r.get("answer_correct") is True and not results[results.index(r)].get("error")]

    retrieval_accuracy = len(source_correct) / total * 100
    answer_accuracy = len(answer_correct) / total * 100
    hallucination_rate = len(hallucinations) / total * 100
    pass_rate = passed / total * 100

    print(f"\n  Total Queries:       {total}")
    print(f"  Passed:              {passed}/{total} ({pass_rate:.0f}%)")
    print(f"  Retrieval Accuracy:  {len(source_correct)}/{total} ({retrieval_accuracy:.0f}%)")
    print(f"  Answer Accuracy:     {len(answer_correct)}/{total} ({answer_accuracy:.0f}%)")
    print(f"  Hallucination Rate:  {len(hallucinations)}/{total} ({hallucination_rate:.0f}%)")

    avg_time = sum(r.get("response_time_s", 0) for r in results) / total
    print(f"  Avg Response Time:   {avg_time:.2f}s")

    print("\n  Detailed Results:")
    print(f"  {'ID':<4} {'Difficulty':<20} {'Source':<8} {'Keywords':<12} {'Hallu':<8} {'Result'}")
    print("  " + "-" * 58)
    for r in results:
        if "error" in r:
            print(f"  {r['id']:<4} {r['difficulty']:<20} {'ERROR':<8} {'---':<12} {'---':<8} FAIL")
        else:
            src = str(r['source_retrieved'])
            print(f"  {r['id']:<4} {r['difficulty']:<20} {src:<8} "
                  f"{r['keywords_found']:<12} {str(r['hallucination']):<8} "
                  f"{'PASS' if r['passed'] else 'FAIL'}")

    # save to JSON for report
    output_path = os.path.join(os.path.dirname(__file__), "evaluation_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "total_queries": total,
                "pass_rate": f"{pass_rate:.0f}%",
                "retrieval_accuracy": f"{retrieval_accuracy:.0f}%",
                "answer_accuracy": f"{answer_accuracy:.0f}%",
                "hallucination_rate": f"{hallucination_rate:.0f}%",
                "avg_response_time_s": round(avg_time, 2)
            },
            "results": results
        }, f, indent=2, ensure_ascii=False)

    print(f"\n  Full results saved to: {output_path}")
    print("=" * 60)


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    # change this to your actual data folder
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")
    
    results = run_evaluation(DATA_FOLDER, top_k=5)
    print_report(results)