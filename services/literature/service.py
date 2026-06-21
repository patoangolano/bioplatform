"""Serviço de busca em literatura biomédica via PubMed."""

from mcp_servers.adapters.pubmed import PubMedAdapter


class LiteratureService:
    """Serviço para busca e integração com literatura biomédica."""

    def __init__(self) -> None:
        self._adapter = PubMedAdapter()

    async def search_pubmed(self, query: str, max_results: int = 10) -> list[dict]:
        """Busca artigos no PubMed.

        Args:
            query: Termo de busca.
            max_results: Número máximo de resultados.

        Returns:
            Lista de artigos encontrados.
        """
        return await self._adapter.search(query, max_results=max_results)
