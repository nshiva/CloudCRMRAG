from __future__ import annotations

import unittest

from src.config import get_settings
from src.llm import check_provider_connectivity, resolve_llm_config
from src.retrieve import (
    embed_query,
    query_chunks,
)
from src.runtime import (
    connect_neo4j,
    get_vector_index_dimension,
    load_embedding_model,
)


class TestRuntimeChecks(unittest.TestCase):
    """Runtime smoke tests that validate external dependencies end-to-end."""

    @classmethod
    def setUpClass(cls):
        # Load validated settings once to avoid repeated env parsing per test.
        cls.settings = get_settings()

    def test_01_required_configs_loaded(self):
        """Ensure all core runtime config values are present and sane."""

        settings = self.settings
        self.assertTrue(settings.neo4j_uri)
        self.assertTrue(settings.neo4j_username)
        self.assertTrue(settings.neo4j_password)
        self.assertTrue(settings.neo4j_database)
        self.assertTrue(settings.vector_index_name)
        self.assertTrue(settings.embedding_model)
        self.assertGreater(settings.embedding_dimension, 0)
        self.assertTrue(settings.docs_path.exists())
        self.assertTrue(settings.docs_path.is_dir())

    def test_02_can_connect_to_neo4j(self):
        """Ensure Neo4j is reachable and can execute a simple query."""

        settings = self.settings
        driver, _connected_uri = connect_neo4j(
            uri=settings.neo4j_uri,
            username=settings.neo4j_username,
            password=settings.neo4j_password,
        )
        with driver:
            with driver.session(database=settings.neo4j_database) as session:
                record = session.run("RETURN 1 AS ok").single()
                self.assertIsNotNone(record)
                self.assertEqual(record["ok"], 1)

    def test_03_can_retrieve_data(self):
        """Ensure vector retrieval returns at least one meaningful result."""

        settings = self.settings
        # Use the same embedding model used for indexing/retrieval.
        embedding_model = load_embedding_model(settings.embedding_model)
        query_embedding = embed_query(
            embedding_model,
            "SSO login failure after identity provider certificate rotation",
        )

        driver, _connected_uri = connect_neo4j(
            uri=settings.neo4j_uri,
            username=settings.neo4j_username,
            password=settings.neo4j_password,
        )
        with driver:
            with driver.session(database=settings.neo4j_database) as session:
                index_dimension = get_vector_index_dimension(
                    session,
                    settings.vector_index_name,
                )
                self.assertIsNotNone(
                    index_dimension,
                    "Vector index not found. Run indexing first.",
                )
                self.assertEqual(
                    int(index_dimension),
                    int(settings.embedding_dimension),
                    "Vector index dimension and embedding dimension mismatch.",
                )

                results = query_chunks(
                    session=session,
                    index_name=settings.vector_index_name,
                    top_k=3,
                    query_embedding=query_embedding,
                    doc_type=None,
                    module=None,
                )
                self.assertGreater(len(results), 0)
                self.assertTrue(results[0].doc_id)
                self.assertTrue(results[0].text.strip())

    def test_04_can_connect_to_llm(self):
        """Ensure configured LLM provider endpoint is reachable and model exists."""

        llm_config = resolve_llm_config(timeout=20)
        info = check_provider_connectivity(llm_config)
        self.assertTrue(info["reachable"])
        self.assertTrue(
            info["model_available"],
            f"Configured model '{llm_config.model}' was not found at provider endpoint.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
