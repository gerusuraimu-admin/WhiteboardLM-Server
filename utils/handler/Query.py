from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
from utils.handler.Embed import CorpusNotFound
from utils.Payload import QueryPayload, Response

"""
QueryPayload:
    uid: str
    message: str

Response:
    status_code: int
    content: Dict[str, Any]

content = {
    'message': message
}

message:
    -
"""


def handle_query(payload: QueryPayload) -> Response:
    try:
        result = prompt(payload)
        return Response(status_code=200, content={'message': result})

    except CorpusNotFound:
        return Response(status_code=404, content={'message': 'Corpus not found'})

    except Exception as e:
        return Response(status_code=500, content={'message': str(e)})


def prompt(payload: QueryPayload) -> str:
    corpus_list = [corpus for corpus in rag.list_corpora() if payload.uid == corpus.display_name]
    if not corpus_list:
        raise CorpusNotFound()

    corpus_name = corpus_list[0].name

    tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[
                    rag.RagResource(
                        rag_corpus=corpus_name
                    )
                ]
            )
        )
    )

    model = GenerativeModel(model_name='gemini-2.0-flash-lite-001', tools=[tool])
    response = model.generate_content(payload.message)

    return str(response)
