
from src.llm.schemas import GenerateBlogSchema

from src.llm.graph import graph
import time

def generate_blog(body: GenerateBlogSchema):
    start = time.time()

    


    result = graph.invoke(
        {
            "topic": body.topic,
            "audience": body.audience,
            "tone": body.tone,
            "category": body.category,
            "word_count": body.word_count,
            "seo_optimized": body.seo_optimized,
            "include_examples": body.include_examples,
            "include_faq": body.include_faq,
            "include_references": body.include_references,
            "include_code_samples": body.include_code_samples,
            "retries": 0
        }
    )
    end = time.time()

    print("=" * 50)
    print(f"TOTAL EXECUTION TIME: {end-start:.2f} sec")
    print("=" * 50)
    return {
    "title": result["title"],
    "introduction": result["introduction"],
    "content": result["content"],
    "conclusion": result["conclusion"],

    "slug": result["slug"],
    "meta_description": result["meta_description"],
    "keywords": result["keywords"],

    "references": result["references"],

    "score": result["score"],
    "feedback": result["feedback"]
}