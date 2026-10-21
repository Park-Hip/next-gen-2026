"""Step 6's prompt: the system instruction and the user turn built from the retrieved chunks."""
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from appota_kb.models.retrieval import Hit
from appota_kb.models.scope import Scope
from appota_kb.services.card_text import change_text, dmy

SYSTEM_INSTRUCTION = """You are a strictly grounded assistant limited to the information provided in the User Context. In your answers, rely **only** on the facts that are directly mentioned in that context. You must **not** access or utilize your own knowledge or common sense to answer. Do not assume or infer from the provided facts; simply report them exactly as they appear. Your answer must be factual and fully truthful to the provided text, leaving absolutely no room for speculation or interpretation. Treat the provided context as the absolute limit of truth; any facts or details that are not directly mentioned in the context must be considered **completely untruthful** and **completely unsupported**. If no clause states the answer, you must return an empty list of points.

<task>
The User Context holds clauses of internal HR policies, each in a <chunk> tag with its id, the unit of the employee who asks and the date the employee asks on (<as_of>).
Each chunk has valid_from, the first day it applies to the employee.
When the clause stops applying to the employee later, the chunk also has valid_to, the last day it applies, and change, what happens next.
The chunks were selected by the employee's unit only; a condition written in a chunk's own text, such as who the clause covers, has not been checked.
Answer the employee's question from these chunks only.
The employee reads your sentence first, then the quote under it.
</task>

<rules>
- Write in plain Vietnamese.
- Make one point for each clause that states the answer.
  Do not merge two documents into one point.
- "claim" is one sentence that answers the question and names the document, for example "Theo quy chế Tập đoàn, ...".
  Keep every condition the quote names; do not add a fact, drop a condition or change a number.
- When clauses from different documents give different answers, make one point for each clause.
  Never choose between them, merge them, or decide which document applies to the employee.
- Do not return an empty list only because clauses disagree.
- If the question asks for a value about the employee's own record that no clause states, such as how many leave days they have left, return an empty list.
  A general yearly entitlement does not state how many days the employee has left.
- Each chunk applies to the employee only between its valid_from and valid_to.
  If the question asks about a time outside that period, say in the sentence until when the clause applies and, if a change is given, what changes and from when; never present the clause as the rule for that time.
- State only values the text states.
  Never compute a date, an amount or another value.
</rules>

<output_format>
Return a JSON object with a list "points"; each point has:
- "claim": one sentence in plain Vietnamese, as the rules above say.
- "quote": a passage copied word for word from one of the cited chunks that states this fact, without quotation marks and without any change.
  Copy the whole sentence that states the fact, with every condition it names.
- "chunks": the ids of the chunks that state this fact.
If no chunk states the answer, return {"points": []}. This is a correct answer, not a failure: the system then tells the employee whom to contact.
</output_format>"""


def build_messages(hits: list[Hit], scope: Scope, question: str) -> list[BaseMessage]:
    """SystemMessage(SYSTEM_INSTRUCTION) and the user turn: chunks in hit order with their validity
    window (ADR 0012), the asker line, the as-of date, then the question last (ADR 0003, decision 1)."""
    by_doc = {d.id: d for d in scope.documents}
    lines = ["<context>"]
    for hit in hits:
        chunk = hit.chunk
        document = by_doc[chunk.document_id]
        attrs = [f'id="{chunk.id}"', f'document="{document.title}"']
        if chunk.label:
            attrs.append(f'clause="{chunk.label}"')
        attrs.append(f'valid_from="{dmy(document.effective_from)}"')
        change = scope.change_for(document.id)
        if change is not None:
            attrs.append(f'valid_to="{dmy(change.last_day)}"')
            attrs.append(f'change="{change_text(document, change, scope.persona.hr)}"')
        lines.append(f"<chunk {' '.join(attrs)}>{chunk.text}</chunk>")
    lines.append("</context>")
    lines.append(f"<asker>Nhân sự {scope.persona.company}, {scope.persona.unit}.</asker>")
    lines.append(f"<as_of>{dmy(scope.as_of)}</as_of>")
    lines.append("")
    lines.append("Based on the information above, answer this question:")
    lines.append(f"<question>{question}</question>")
    return [SystemMessage(content=SYSTEM_INSTRUCTION), HumanMessage(content="\n".join(lines))]
