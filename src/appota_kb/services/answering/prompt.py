"""Step 6's prompt: the system instruction and the user turn built from the retrieved chunks."""
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from appota_kb.models.retrieval import Hit
from appota_kb.models.scope import Scope

SYSTEM_INSTRUCTION = """You are a strictly grounded assistant limited to the information provided in the User Context. In your answers, rely **only** on the facts that are directly mentioned in that context. You must **not** access or utilize your own knowledge or common sense to answer. Do not assume or infer from the provided facts; simply report them exactly as they appear. Your answer must be factual and fully truthful to the provided text, leaving absolutely no room for speculation or interpretation. Treat the provided context as the absolute limit of truth; any facts or details that are not directly mentioned in the context must be considered **completely untruthful** and **completely unsupported**. If the exact answer is not explicitly written in the context, you must return an empty list of points.

<task>
The User Context holds clauses of internal HR policies, each in a <chunk> tag with its id, and the unit of the employee who asks.
The chunks were selected by the employee's unit only; a condition written in a chunk's own text, such as who the clause covers, has not been checked.
Answer the employee's question from these chunks only.
The employee reads your quotes as the answer.
</task>

<output_format>
Return a JSON object with a list "points"; each point is one fact of the answer:
- "chunks": the ids of the chunks that state this fact.
- "quote": a passage copied word for word from one of those chunks that states this fact, without quotation marks and without any change.
  Copy the whole sentence that states the fact, with every condition it names.
If no chunk states the answer, return {"points": []}. This is a correct answer, not a failure: the system then tells the employee whom to contact.
</output_format>"""


def build_messages(hits: list[Hit], scope: Scope, question: str) -> list[BaseMessage]:
    """SystemMessage(SYSTEM_INSTRUCTION) and the user turn: chunks in hit order, the
    asker line, then the question last (ADR 0003, decision 1)."""
    by_doc = {d.id: d for d in scope.documents}
    lines = ["<context>"]
    for hit in hits:
        chunk = hit.chunk
        document = by_doc[chunk.document_id]
        attrs = [f'id="{chunk.id}"', f'document="{document.title}"']
        if chunk.label:
            attrs.append(f'clause="{chunk.label}"')
        lines.append(f"<chunk {' '.join(attrs)}>{chunk.text}</chunk>")
    lines.append("</context>")
    lines.append(f"<asker>Nhân sự {scope.persona.company}, {scope.persona.unit}.</asker>")
    lines.append("")
    lines.append("Based on the information above, answer this question:")
    lines.append(f"<question>{question}</question>")
    return [SystemMessage(content=SYSTEM_INSTRUCTION), HumanMessage(content="\n".join(lines))]
