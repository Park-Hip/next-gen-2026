"""Print the top chunks of step 5 with their RRF, BM25 and dense numbers.

Run by hand (needs GEMINI_API_KEY):
  uv run python scripts/search.py <persona> <as_of> <question>
  uv run python scripts/search.py          # every row and wording of data/test_cases.yaml
"""
from datetime import date
import logging
import os
import sys

from appota_kb.core.config import load_config
from appota_kb.evaluation.data_edit import with_edit
from appota_kb.integrations.data_files import load_documents, load_org, load_personas, load_test_cases
from appota_kb.integrations.gemini import gemini_embeddings
from appota_kb.models.retrieval import Hit
from appota_kb.services.retrieval.index import build_index
from appota_kb.services.retrieval.search import retrieve
from appota_kb.services.scope import scope as build_scope


def _print_hits(hits: list[Hit]) -> None:
    for hit in hits:
        print(
            f"  {hit.chunk.id}  rrf={hit.score:.4f}  bm25={hit.bm25:.4f}#{hit.bm25_rank}"
            f"  dense={hit.dense:.4f}#{hit.dense_rank}"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set; set it to a Gemini API key to run the manual check")
    config = load_config()
    documents = load_documents()
    personas = load_personas(load_org())
    if len(sys.argv) == 1:
        index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
        for row in load_test_cases():
            docs = with_edit(documents, row["data_edit"]) if "data_edit" in row else documents
            persona = personas[row["persona"]]
            as_of = row["as_of"]
            for question in row["questions"]:
                scoped = build_scope(persona, as_of, docs)
                print(f"row {row['id']} {row['kind']} | {persona.id} {as_of} | {question}")
                _print_hits(retrieve(index, scoped, question, config.retrieval))
    elif len(sys.argv) == 4:
        persona_id, as_of_text, question = sys.argv[1], sys.argv[2], sys.argv[3]
        if persona_id not in personas:
            sys.exit(f"unknown persona {persona_id}")
        index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
        scoped = build_scope(personas[persona_id], date.fromisoformat(as_of_text), documents)
        print(f"{persona_id} {as_of_text} | {question}")
        _print_hits(retrieve(index, scoped, question, config.retrieval))
    else:
        sys.exit("usage: python scripts/search.py [<persona> <as_of> <question>]")
