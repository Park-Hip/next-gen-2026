"""Shared fixtures: loaded data, the boundary dates, network guard and the trap mutations."""
from dataclasses import replace
from datetime import date, timedelta
import socket

import pytest

from appota_kb.integrations.data_files import load_documents, load_org, load_personas, load_test_cases
from appota_kb.models.document import Document

MISSION1_IDS = [
    "LEAVE-GROUP-v1", "LEAVE-GAMECO-v1", "LEAVE-GAMECO-v2", "LEAVE-GAMECO-v3",
    "LEAVE-GAMECO-v4-DRAFT", "LEAVE-PROC-GAMECO-v1", "LEAVE-PAYCO-v1",
    "SAL-BAND-GAMECO", "OT-GAMECO-v1", "TRAVEL-GAMECO-v1",
]


LOOPBACK = {"127.0.0.1", "::1", "localhost"}


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Blocks every connection off this machine. Loopback stays open because asyncio's
    event loop on Windows (used by FastAPI's TestClient) connects a local socket pair."""
    connect = socket.socket.connect

    def guarded(sock, address):
        if isinstance(address, tuple) and address[0] in LOOPBACK:
            return connect(sock, address)
        raise RuntimeError("network is disabled during tests")

    def blocked(*args, **kwargs):
        raise RuntimeError("network is disabled during tests")

    monkeypatch.setattr(socket.socket, "connect", guarded)
    monkeypatch.setattr(socket, "create_connection", blocked)


@pytest.fixture(scope="session")
def documents():
    return load_documents()


@pytest.fixture(scope="session")
def org():
    return load_org()


@pytest.fixture(scope="session")
def personas(org):
    return load_personas(org)


@pytest.fixture(scope="session")
def cases():
    return load_test_cases()


@pytest.fixture(scope="session")
def dates(documents):
    days = {date(2026, 10, 7)}
    for d in documents:
        for value in (d.effective_from, d.effective_to):
            if value is not None:
                days.add(value)
                days.add(value - timedelta(days=1))
                days.add(value + timedelta(days=1))
    return sorted(days)


@pytest.fixture(scope="session")
def mission1_documents(documents):
    return [d for d in documents if d.id in MISSION1_IDS]


@pytest.fixture
def mutations(documents):
    """The seven trap changes from the #9 plan, each as a (name, documents) pair."""
    group = next(d for d in documents if d.id == "LEAVE-GROUP-v1")
    out = []

    def changed(doc_id, **kwargs):
        return [replace(d, **kwargs) if d.id == doc_id else d for d in documents]

    out.append(("remove_override_v2", changed("LEAVE-GAMECO-v2", overrides=None)))
    out.append(("publish_v4", changed("LEAVE-GAMECO-v4-DRAFT", status="published", effective_from=date(2026, 10, 1))))
    out.append(("publish_v4_no_date", changed("LEAVE-GAMECO-v4-DRAFT", status="published", effective_from=None)))
    out.append(("v3_delayed", changed("LEAVE-GAMECO-v3", status="draft")))
    gv2 = Document(
        id="LEAVE-GROUP-v2", title=group.title, owner=group.owner, series="LEAVE-GROUP",
        topic=group.topic, access=group.access, applies_to=group.applies_to, status="published",
        effective_from=date(2026, 7, 1), effective_to=None, overrides=None,
        complements=group.complements, body=group.body,
    )
    out.append(("group_v2", documents + [gv2]))
    with_end = changed("LEAVE-GAMECO-v2", effective_to=date(2026, 6, 30))
    with_end = [replace(d, status="draft") if d.id == "LEAVE-GAMECO-v3" else d for d in with_end]
    out.append(("v2_repealed", with_end))
    out.append(("remove_complement_proc", changed("LEAVE-PROC-GAMECO-v1", complements=())))
    return out