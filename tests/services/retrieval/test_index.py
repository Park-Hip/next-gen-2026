"""The search index: every chunk embedded once, with its document title in front."""
from fakes import CountingEmbeddings

from appota_kb.services.chunking import chunks as document_chunks
from appota_kb.services.retrieval.index import build_index, index_text


def test_build_index_one_embed_call_title_in_front(documents):
    embeddings = CountingEmbeddings()
    index = build_index(documents, embeddings)
    chunks = [c for d in documents for c in document_chunks(d)]
    assert embeddings.document_calls == 1
    assert len(index.texts) == len(chunks)
    assert len(index.store.store) == len(chunks)
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    chunk = next(c for c in document_chunks(v2) if c.id == "LEAVE-GAMECO-v2#2")
    assert index.texts[chunk.id] == index_text(v2, chunk)
    assert index.texts[chunk.id].startswith(v2.title + ". ")
