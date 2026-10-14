"""The output contract: the JSON schema handed to the model."""
import pytest

from appota_kb.services.answering.output import answer_schema


def test_answer_schema_enum_and_order():
    schema = answer_schema(("LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"))
    point = schema["$defs"]["Point"]
    assert list(point["properties"]) == ["chunks", "quote", "text"]
    chunks = point["properties"]["chunks"]
    assert chunks["type"] == "array"
    assert chunks["items"]["type"] == "string"
    assert chunks["items"]["enum"] == ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"]
    assert point["required"] == ["chunks", "quote", "text"]
    assert schema["properties"]["points"]["minItems"] == 1


def test_answer_schema_single_id_is_still_an_enum():
    schema = answer_schema(("LEAVE-GAMECO-v2#2",))
    assert schema["$defs"]["Point"]["properties"]["chunks"]["items"]["enum"] == ["LEAVE-GAMECO-v2#2"]


def test_answer_schema_empty_ids_raises():
    with pytest.raises(ValueError):
        answer_schema(())
