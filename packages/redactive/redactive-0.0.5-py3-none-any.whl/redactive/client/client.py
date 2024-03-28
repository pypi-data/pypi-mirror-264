from typing import List

from grpclib.client import Channel

from redactive.grpc.v1 import Query, QueryRequest, RelevantChunk, SearchStub

# from pprint import pprint


class Client:
    host: str
    port: int

    def __init__(self, credential: str, host: str = "grpc.redactive.ai", port: int = 443) -> None:
        self.credential = credential
        self.host = host
        self.port = port

    async def query_chunks(self, semantic_query: str, count=1) -> List[RelevantChunk]:
        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=(dict(authorization=f"Bearer {self.credential}")))
            request = QueryRequest(count=count, query=Query(semantic_query=semantic_query))
            response = await stub.query_chunks(request)
            return response.relevant_chunks
