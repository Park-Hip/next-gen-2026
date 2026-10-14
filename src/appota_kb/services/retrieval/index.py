"""The search index: every chunk of every loaded document, embedded once at start-up."""
from dataclasses import dataclass

from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from appota_kb.models.document import Chunk, Document
from appota_kb.services.chunking import chunks as document_chunks
from appota_kb.services.retrieval.bm25 import tokens


def index_text(document: Document, chunk: Chunk) -> str:
    """The text indexed for both BM25 and embeddings: the document title in front of the chunk."""
    return f"{document.title}. {chunk.text}"


@dataclass(frozen=True)
class Index:
    store: InMemoryVectorStore
    texts: dict[str, str]
    tokens: dict[str, tuple[str, ...]]


def build_index(documents: list[Document], embeddings: Embeddings) -> Index:
    """Embed every chunk of every loaded document once; the scope is applied at search time."""
    pairs = [(document, chunk) for document in documents for chunk in document_chunks(document)]
    texts: dict[str, str] = {}
    indexed_tokens: dict[str, tuple[str, ...]] = {}
    lc_docs = []
    ids = []
    for document, chunk in pairs:
        text = index_text(document, chunk)
        texts[chunk.id] = text
        indexed_tokens[chunk.id] = tuple(tokens(text))
        lc_docs.append(LCDocument(id=chunk.id, page_content=text))
        ids.append(chunk.id)
    store = InMemoryVectorStore(embeddings)
    store.add_documents(lc_docs, ids=ids)
    return Index(store=store, texts=texts, tokens=indexed_tokens)
