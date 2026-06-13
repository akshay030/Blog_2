from typing import TypedDict, List, Any
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import json
from tavily import TavilyClient
from src.utils.settings import settings
from src.llm.schemas import BlogOutput,EvaluationOutput,PlannerOutput
from langgraph.graph import StateGraph,END
from src.utils.settings import settings

MIN_SCORE = 8.0

MAX_RETRIES = 2


class BlogState(TypedDict):
    # User Input
    topic: str

    audience: str

    tone: str

    category: str

    word_count: int

    seo_optimized: bool

    include_examples: bool

    include_faq: bool

    include_references: bool

    include_code_samples: bool

    # Research
    queries: List[str]

    sources: List[dict[str, Any]]
    
    research_context: str

    # Generated Blog
    title: str

    introduction: str

    content: str

    conclusion: str
    
    slug: str

    meta_description: str

    keywords: List[str]
    
    references: List[str]

    # Evaluation
    score: float

    feedback: str

    retries: int


def should_retry(state):
    print("=" * 50)
    print("RETRY CHECK")

    print(f"Score: {state['score']}")
    print(f"Retries: {state['retries']}")
    if state["score"] >= MIN_SCORE:
        return "accepted"

    if state["retries"] >= MAX_RETRIES:
        return "accepted"

    return "retry"


tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

planner_llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.2,api_key=settings.GROQ_API_KEY)

writer_llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.2,api_key=settings.GROQ_API_KEY)

evaluator_llm = ChatGroq(model="qwen/qwen3-32b", temperature=0,api_key=settings.GROQ_API_KEY)


def planner_node(state):
    
    
    structured_llm = planner_llm.with_structured_output(
        PlannerOutput
    )
    print("=" * 50)
    print("PLANNER NODE STARTED")
    


    prompt = f"""
    Generate 5 search queries.

    Topic:
    {state['topic']}

    Audience:
    {state['audience']}

    Category:
    {state['category']}

    Return JSON:

    {{
      "queries": [
        "query1",
        "query2",
        "query3",
        "query4",
        "query5"
      ]
    }}
    """

    result = structured_llm.invoke(prompt)
    print(f"Topic: {state['topic']}")

    

    print("Generated Queries:")
    print(result.queries)

    print("PLANNER NODE COMPLETED")
    print("=" * 50)

    # result = json.loads(response.content)
    
    return {
        "queries": result.queries
    }


def research_node(state):
    print("=" * 50)
    print("RESEARCH NODE STARTED")

    

    

    sources = []
    
    seen_urls = set()

    for query in state["queries"]:

        response = tavily_client.search(query=query, max_results=3)

        for result in response["results"]:

            if result["url"] not in seen_urls:

                seen_urls.add(result["url"])

                sources.append(
                    {
                        "title": result["title"],
                        "url": result["url"],
                        "content": result["content"][:300]
                    }
                )
    sources = sources[:5]

    research_context = "\n\n".join(
        [
            f"Title: {source['title']}\n"
            f"Content: {source['content']}"
            for source in sources
        ]
    )

    print(f"Sources Found: {len(sources)}")
    print(f"Research Context Length: {len(research_context)}")

    print("RESEARCH NODE COMPLETED")
    print("=" * 50)

    return {
        "sources": sources,
        "research_context": research_context
    }


def writer_node(state):
    print("=" * 50)
    print("WRITER NODE STARTED")

    

    


    structured_llm = writer_llm.with_structured_output(BlogOutput)
    

    prompt = f"""
    Write a high quality blog.

    Topic:
    {state["topic"]}

    Audience:
    {state["audience"]}

    Tone:
    {state["tone"]}

    Category:
    {state["category"]}

    Word Count:
    {state["word_count"]}

    SEO Optimized:
    {state["seo_optimized"]}

    Include Examples:
    {state["include_examples"]}

    Include FAQ:
    {state["include_faq"]}

    Include References:
    {state["include_references"]}

    Include Code Samples:
    {state["include_code_samples"]}

    Research Sources:
    {state["research_context"]}

    Generate:

    1. title
    2. introduction
    3. content
    4. conclusion
    5. slug
    6. meta_description
    7. keywords

    SEO Requirements:

    - Title should be SEO friendly
    - Title should be under 60 characters
    - Meta description should be under 160 characters
    - Generate 5-10 relevant keywords
    - Slug should be lowercase
    - Slug should use hyphens
    - Slug should be URL friendly

    Example:

    Slug:
    google-turboquant-ai-optimization

    Meta Description:
    Learn how Google's TurboQuant improves AI model efficiency through advanced quantization and memory optimization.

    Keywords:
    [
    "TurboQuant",
    "Google AI",
    "LLM Optimization",
    "Quantization",
    "AI Inference"
    ]

    Use the research sources to support claims.
"""

    result = structured_llm.invoke(prompt)
    print("Generated Title:")
    print(result.title)
    print("Generated SEO")
    print("Slug:", result.slug)
    print("Meta:", result.meta_description)
    print("Keywords:", result.keywords)

    print("WRITER NODE COMPLETED")
    print("=" * 50)
    
    references = [
    source["url"]
    for source in state["sources"]
]

    return {
        "title": result.title,
        "introduction": result.introduction,
        "content": result.content,
        "conclusion": result.conclusion,
        
        "slug": result.slug,
        "meta_description": result.meta_description,
        "keywords": result.keywords,
        "references":references,
        }


def evaluator_node(state):
    print("=" * 50)
    print("EVALUATOR NODE STARTED")

    

    

    structured_llm = evaluator_llm.with_structured_output(EvaluationOutput)

    prompt = f"""
    Evaluate the following blog.

    Topic:
    {state["topic"]}

    Audience:
    {state["audience"]}

    Tone:
    {state["tone"]}

    Blog Title:
    {state["title"]}

    Introduction:
    {state["introduction"]}

    Content:
    {state["content"]}

    Conclusion:
    {state["conclusion"]}

    Score from 0 to 10.

    Evaluate:
    - Accuracy
    - Completeness
    - Readability
    - Audience Alignment
    - Tone Consistency
    - SEO Quality
    - Grammar

    Return:
    {{
        "score": float,
        "feedback": "detailed feedback"
    }}
    """

    result = structured_llm.invoke(prompt)
    print(f"Score: {result.score}")
    print(f"Feedback: {result.feedback}")

    print("EVALUATOR NODE COMPLETED")
    print("=" * 50)

    return {"score": result.score, "feedback": result.feedback}


def rewrite_node(state):
    print("=" * 50)
    print("REWRITE NODE STARTED")

    print("Previous Score:")
    print(state["score"])

    print("Feedback:")
    print(state["feedback"])

    

    

    structured_llm = writer_llm.with_structured_output(BlogOutput)

    prompt = f"""
    Improve the blog using the evaluator feedback.

    Topic:
    {state["topic"]}

    Audience:
    {state["audience"]}

    Tone:
    {state["tone"]}

    Existing Blog:

    Title:
    {state["title"]}

    Introduction:
    {state["introduction"]}

    Content:
    {state["content"][:8000]}

    Conclusion:
    {state["conclusion"]}

    Feedback:
    {state["feedback"]}

    Rewrite and improve the blog.

    Keep:
    - same topic
    - same audience
    - same tone

    Improve according to feedback.

    Return:
    title
    introduction
    content
    conclusion
    """

    result = structured_llm.invoke(prompt)
    print("REWRITE NODE COMPLETED")
    print("=" * 50)
    
    references = [
    source["url"]
    for source in state["sources"]
]

    return {
        "title": result.title,
        "introduction": result.introduction,
        "content": result.content,
        "conclusion": result.conclusion,
        "slug": result.slug,
        "meta_description": result.meta_description,
        "keywords": result.keywords,
        "references":references,
        "retries": state["retries"] + 1,
    }


builder = StateGraph(BlogState)

builder.add_node("planner", planner_node)

builder.add_node("research", research_node)

builder.add_node("writer", writer_node)

builder.add_node("evaluator", evaluator_node)

builder.add_node("rewrite", rewrite_node)


builder.set_entry_point("planner")


builder.add_edge("planner", "research")

builder.add_edge("research", "writer")

builder.add_edge("writer", "evaluator")

builder.add_conditional_edges(
    "evaluator", should_retry, {"accepted": END, "retry": "rewrite"}
)

builder.add_edge("rewrite", "evaluator")

graph = builder.compile( name="blog_generation_graph")


