from rag.prompt_templates import (
    system_prompt_en, document_prompt_en, footer_prompt_en,
    system_prompt_ar, document_prompt_ar, footer_prompt_ar
)
from rag.llm_factory import LLMProviderFactory


def is_arabic(text: str):
    return any('\u0600' <= c <= '\u06FF' for c in text)


def build_prompt(query, retrieved_docs):
    # Detect language
    arabic = is_arabic(query)

    if arabic:
        system = system_prompt_ar.substitute()
        doc_template = document_prompt_ar
        footer = footer_prompt_ar.substitute()
    else:
        system = system_prompt_en.substitute()
        doc_template = document_prompt_en
        footer = footer_prompt_en.substitute()

    # Build documents section
    docs_text = ""
    for i, doc in enumerate(retrieved_docs, start=1):
        docs_text += doc_template.substitute(
            doc_num=i,
            chunk_text=doc["chunks"]
        ) + "\n"

    # Final prompt
    prompt = f"{system}\n\n{docs_text}\n{footer}\n{query}"

    return prompt


def generate_answer(query, retrieved_docs, config):
    # 1. Build prompt
    prompt = build_prompt(query, retrieved_docs)

    # 2. Create LLM
    factory = LLMProviderFactory(config)
    llm = factory.create(config.get("PROVIDER", "DEEPSEEK"))

    # 3. Generate answer
    answer = llm.generate_text(prompt)

    return answer