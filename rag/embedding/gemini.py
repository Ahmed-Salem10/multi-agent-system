import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .base import BaseEmbedding


load_dotenv()


class GeminiEmbedding(BaseEmbedding):

    def __init__(
        self,
        model_name: str = "gemini-embedding-001",
        output_dimensionality: int = 768,
    ):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in the environment."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = model_name
        self.output_dimensionality = output_dimensionality

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:

        result = self.client.models.embed_content(
            model=self.model_name,
            contents=documents,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=self.output_dimensionality,
            ),
        )

        return [
            embedding.values
            for embedding in result.embeddings
        ]

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        result = self.client.models.embed_content(
            model=self.model_name,
            contents=query,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=self.output_dimensionality,
            ),
        )

        return result.embeddings[0].values