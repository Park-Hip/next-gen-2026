"""The output contract: the JSON schema handed to the model and the parsing of its reply."""
import pytest

from appota_kb.services.answering.output import answer_schema, parse_disagreement, parse_reply


def test_answer_schema_enum_and_order():
    schema = answer_schema(("LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"))
    assert list(schema["properties"]) == ["answer", "points", "disagreement"]
    assert schema["required"] == ["answer", "points", "disagreement"]
    point = schema["$defs"]["Point"]
    assert list(point["properties"]) == ["quote", "chunks"]
    chunks = point["properties"]["chunks"]
    assert chunks["type"] == "array"
    assert chunks["items"]["type"] == "string"
    assert chunks["items"]["enum"] == ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"]
    assert point["required"] == ["quote", "chunks"]
    assert point["properties"]["chunks"]["minItems"] == 1
    assert "minItems" not in schema["properties"]["points"]


def test_answer_schema_has_a_required_disagreement_of_at_most_two_ids():
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1", "LEAVE-PAYCO-v1#2")
    schema = answer_schema(ids)
    flag = schema["properties"]["disagreement"]
    assert flag["type"] == "array"
    assert flag["maxItems"] == 2
    assert "minItems" not in flag
    assert flag["items"]["enum"] == list(ids)


def test_answer_schema_single_id_keeps_the_disagreement_an_enum():
    flag = answer_schema(("LEAVE-GAMECO-v2#2",))["properties"]["disagreement"]
    assert flag["items"]["enum"] == ["LEAVE-GAMECO-v2#2"]
    assert "const" not in flag["items"]


def test_parse_reply_returns_the_answer_and_its_points():
    answer, points = parse_reply(
        {
            "answer": "  Bạn tạo đơn trên hệ thống HR nội bộ, trưởng nhóm duyệt.  ",
            "points": [{"quote": "14 ngày.", "chunks": ["X#1"]}],
        }
    )
    assert answer == "Bạn tạo đơn trên hệ thống HR nội bộ, trưởng nhóm duyệt."
    assert points is not None and len(points) == 1
    assert points[0].quote == "14 ngày." and points[0].chunks == ("X#1",)
    assert not hasattr(points[0], "claim")


def test_parse_reply_refuses_a_missing_answer():
    for parsed in (None, "text", [], {"points": []}, {"answer": None, "points": []}):
        assert parse_reply(parsed) == ("", None), parsed


def test_parse_reply_refuses_an_empty_answer_while_points_are_not_empty():
    for answer in ("", "   "):
        parsed = {"answer": answer, "points": [{"quote": "14 ngày.", "chunks": ["X#1"]}]}
        assert parse_reply(parsed) == ("", None), answer


def test_parse_reply_keeps_an_empty_answer_with_no_points():
    # The "không tìm thấy" reply stays valid; step 7 turns it into the refusal, not a malformed one.
    assert parse_reply({"answer": "", "points": []}) == ("", ())
    assert parse_reply({"answer": "   ", "points": []}) == ("", ())


def test_parse_reply_keeps_an_answer_with_no_points():
    answer, points = parse_reply({"answer": "Không có quy định.", "points": []})
    assert answer == "Không có quy định."
    assert points == ()


def test_parse_reply_refuses_a_malformed_point():
    for point in ({"quote": "14 ngày."}, {"chunks": ["X#1"]}, {"quote": 14, "chunks": ["X#1"]}):
        assert parse_reply({"answer": "14 ngày.", "points": [point]}) == ("", None), point


def test_parse_disagreement():
    assert parse_disagreement({"answer": "", "points": [], "disagreement": ["a#1", "b#1"]}) == ("a#1", "b#1")
    assert parse_disagreement({"answer": "", "points": [], "disagreement": []}) == ()
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
