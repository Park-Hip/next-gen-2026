"""The output contract: the JSON schema handed to the model."""
import pytest

from appota_kb.services.answering.output import answer_schema, parse_disagreement


def test_answer_schema_enum_and_order():
    schema = answer_schema(("LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"))
    point = schema["$defs"]["Point"]
    assert list(point["properties"]) == ["claim", "quote", "chunks"]
    chunks = point["properties"]["chunks"]
    assert chunks["type"] == "array"
    assert chunks["items"]["type"] == "string"
    assert chunks["items"]["enum"] == ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"]
    assert point["required"] == ["claim", "quote", "chunks"]
    assert point["properties"]["chunks"]["minItems"] == 1
    assert "minItems" not in schema["properties"]["points"]


def test_answer_schema_has_a_required_disagreement_of_at_most_two_ids():
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1", "LEAVE-PAYCO-v1#2")
    schema = answer_schema(ids)
    assert list(schema["properties"]) == ["points", "disagreement"]
    assert schema["required"] == ["points", "disagreement"]
    flag = schema["properties"]["disagreement"]
    assert flag["type"] == "array"
    assert flag["maxItems"] == 2
    assert "minItems" not in flag
    assert flag["items"]["enum"] == list(ids)


def test_answer_schema_single_id_keeps_the_disagreement_an_enum():
    flag = answer_schema(("LEAVE-GAMECO-v2#2",))["properties"]["disagreement"]
    assert flag["items"]["enum"] == ["LEAVE-GAMECO-v2#2"]
    assert "const" not in flag["items"]


def test_parse_disagreement():
    assert parse_disagreement({"points": [], "disagreement": ["a#1", "b#1"]}) == ("a#1", "b#1")
    assert parse_disagreement({"points": [], "disagreement": []}) == ()
    # A longer list is kept whole; step 7 decides it is not a valid flag.
    assert parse_disagreement({"disagreement": ["a#1", "b#1", "c#1"]}) == ("a#1", "b#1", "c#1")


def test_parse_disagreement_treats_a_missing_or_malformed_field_as_empty():
    for parsed in (None, "text", [], {"points": []}, {"disagreement": None}, {"disagreement": "a#1"},
                   {"disagreement": [1, 2]}, {"disagreement": ["a#1", None]}, {"disagreement": {"a#1": 1}}):
        assert parse_disagreement(parsed) == (), parsed


def test_answer_schema_allows_empty_points():
    points = answer_schema(("LEAVE-GAMECO-v2#2",))["properties"]["points"]
    assert points["type"] == "array"
    assert "minItems" not in points


def test_answer_schema_single_id_is_still_an_enum():
    schema = answer_schema(("LEAVE-GAMECO-v2#2",))
    assert schema["$defs"]["Point"]["properties"]["chunks"]["items"]["enum"] == ["LEAVE-GAMECO-v2#2"]


def test_answer_schema_empty_ids_raises():
    with pytest.raises(ValueError):
        answer_schema(())
