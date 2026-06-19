# src/ai/schemas.py

from pydantic import BaseModel, Field


class GenerateBlogSchema(BaseModel):
    topic: str = Field(..., min_length=3)

    audience: str
    tone: str
    category: str

    word_count: int = 1000

    seo_optimized: bool = True

    include_examples: bool = True
    include_faq: bool = True
    include_references: bool = True
    include_code_samples: bool = False


# class GeneratedBlogResponseSchema(BaseModel):
#     title: str

#     introduction: str

#     content: str

#     conclusion: str

#     score: float


class GenerateBlogResponse(BaseModel):

    title: str

    introduction: str

    content: str

    conclusion: str

    slug: str

    meta_description: str

    keywords: list[str]

    references: list[str]

    score: float

    feedback: str


# src/ai/writer_schema.py


class PlannerOutput(BaseModel):
    queries: list[str]


class BlogOutput(BaseModel):
    title: str

    introduction: str

    content: str

    conclusion: str

    slug: str
    meta_description: str
    keywords: list[str]
    references: list[str]


class EvaluationOutput(BaseModel):
    score: float

    feedback: str
