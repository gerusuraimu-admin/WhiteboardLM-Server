from vertexai import rag
from utils.Session import Session
from utils.handler.Auth import handle_auth, InvalidAuthError
from utils.handler.Embed import CorpusNotFound
from utils.Payload import QueryPayload, AuthPayload, Response

"""
QueryPayload:
    uid: str
    session_id: str
    message: str

Response:
    status_code: int
    content: Dict[str, Any]

content = {
    'uid': uid,
    'session_id': session_id,
    'message': message
}

message:
    -
"""


def handle_query(payload: QueryPayload, session: Session) -> Response:
    try:
        auth_payload = AuthPayload(uid=payload.uid, session_id=payload.session_id)
        response: Response = handle_auth(auth_payload, session)
        if response.status_code != 200:
            raise InvalidAuthError()

        result = prompt(payload)
        response.content['message'] = result
        return response

    except Exception as e:
        return Response(status_code=500, content={'message': str(e)})


def prompt(payload: QueryPayload) -> str:
    corpus_list = [corpus for corpus in rag.list_corpora() if payload.uid == corpus.display_name]
    if not corpus_list:
        raise CorpusNotFound()

    corpus_name = corpus_list[0].name

    rag_config = rag.RagRetrievalConfig(
        top_k=10,
        filter=rag.Filter(
            vector_distance_threshold=0.5
        )
    )

    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=corpus_name
            )
        ],
        text=payload.message,
        rag_retrieval_config=rag_config
    )

    return str(response)
