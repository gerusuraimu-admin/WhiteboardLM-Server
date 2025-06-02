import os
from vertexai import rag
from utils.Session import Session
from utils.Session import InvalidAuthError
from utils.Payload import AuthPayload, EmbedPayload, Response
from utils.handler.Auth import handle_auth
from utils.handler.Register import create_corpus

"""
AuthPayload:
    uid: str
    session_id: str

Response:
    status_code: int
    content: Dict[str, Any]

content = {
    'uid': uid,
    'session_id': session_id,
    'message': message
}

message:
    - Update corpus successfully ... RAGコーパスのデータソース更新が正常に終了
    - Invalid Auth ... 正規ユーザーによるリクエストとして扱えなかった
    - Corpus not found ... データソースを更新すべきRAGコーパスが存在しなかった
    - その他例外
"""


class FailedCreateCorpus(Exception):
    pass


class CorpusNotFound(Exception):
    pass


def handle_embed(payload: EmbedPayload, session: Session) -> Response:
    try:
        auth_payload = AuthPayload(uid=payload.uid, session_id=payload.session_id)
        response: Response = handle_auth(auth_payload, session)
        if response.status_code != 200:
            raise InvalidAuthError()

        names, display_names = update_corpus(payload)
        response.content['message'] = 'Update corpus successfully'
        response.content['content']['names'] = names
        response.content['content']['display_names'] = display_names

        return response

    except InvalidAuthError:
        return Response(status_code=401, content={'message': 'Invalid Auth'})

    except CorpusNotFound:
        return Response(status_code=404, content={'message': 'Corpus not found'})

    except Exception as e:
        return Response(status_code=500, content={'message': str(e)})


def update_corpus(payload: EmbedPayload):
    try:
        corpus_list = [corpus for corpus in rag.list_corpora() if payload.uid == corpus.display_name]
        if not corpus_list:
            raise CorpusNotFound()

        corpus_name = corpus_list[0].name

        files = rag.list_files(corpus_name=corpus_name)
        if not files:
            raise CorpusNotFound()

        names = [name.name for name in files]
        display_names = [name.display_name for name in files]

        path = [f'gs://{os.environ["BUCKET"]}/documents/{payload.uid}']
        # TODO: チャンクサイズとオーバーラップはデプロイのタイミングではもう少し大きくすること！
        transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=128,
                chunk_overlap=32
            )
        )

        rag.import_files(
            corpus_name,
            path,
            transformation_config=transformation_config
        )

        return names, display_names
    except CorpusNotFound:
        raise CorpusNotFound()

    except Exception:
        raise FailedCreateCorpus()
