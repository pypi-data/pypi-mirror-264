import pytest

from iotadb.iotadb import (OPSET_LOOKUP, Collection, Document, EmbedModel,
                           IotaDB)


@pytest.mark.parametrize(
    "metric, embed_model, persist, persist_dir",
    [
        ("cosine", "all-mpnet-base-v2", False, None),
        ("cosine", "all-mpnet-base-v2", True, "data/"),
        ("dot", "all-mpnet-base-v2", False, None),
        ("dot", "all-mpnet-base-v2", True, "data/"),
        ("euclidean", "all-mpnet-base-v2", False, None),
        ("euclidean", "all-mpnet-base-v2", True, "data/"),
    ],
)
def test_database_init(metric, embed_model, persist, persist_dir):
    db = IotaDB(
        metric=metric, embed_model=embed_model, persist=persist, persist_dir=persist_dir
    )

    assert db.sim_func == OPSET_LOOKUP[metric]
    assert isinstance(db.embed_model, EmbedModel)
    assert db.persist == persist
    assert isinstance(db.persist, bool)
    assert db.persist_dir == persist_dir
    assert isinstance(db.persist_dir, str) or db.persist_dir is None


def test_create_collection(default_database, sample_documents):
    default_database.create_collection(
        name="test_collection", documents=sample_documents
    )

    assert isinstance(default_database.get_collection(), Collection)


def test_load_collection():
    pass


def test_get_documents():
    pass


def test_add_documents():
    pass


def test_update_document():
    pass


def test_remove_document():
    pass


def test_search():
    pass
