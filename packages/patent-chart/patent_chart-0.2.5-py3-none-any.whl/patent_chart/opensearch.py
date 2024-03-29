import typing

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

from . import parser

host = 'vpc-patents-fbqas7tj6njmlbjopex7thfxzm.us-east-2.es.amazonaws.com'
region = 'us-east-2'

session = boto3.Session()
credentials = session.get_credentials()

awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    'es',
    session_token=credentials.token
)

client = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


class IndexedPatent(parser.GoogleParsedPatent):
    summary: typing.Optional[str] = None
    short_summary: typing.Optional[str] = None
    topics: typing.Optional[typing.List[str]] = None
    text: typing.Optional[str] = None
    text_format: typing.Optional[str] = None

XML_USPTO_POST_2001 = 'xml_uspto_post_2001'

CLAIM_EMBEDDING_MAPPINGS = {
    "properties": {
        "patent_doc_id": {
            "type": "keyword"
        },
        "claim_id": {
            "type": "keyword"
        },
        "embedding": {
            "type": "knn_vector",
            "dimension": 1024,
            "method": {
                "name": "hnsw",
                "space_type": "cosinesimil",
                "engine": "nmslib",
                "parameters": {
                    "ef_construction": 128,
                    "m": 64
                }
            }
        }
    }
}

SPECIFICATION_EMBEDDING_MAPPINGS = {
    "properties": {
        "patent_doc_id": {
            "type": "keyword"
        },
        "paragraph_id": {
            "type": "keyword"
        },
        "embedding": {
            "type": "knn_vector",
            "dimension": 1024,
            "method": {
                "name": "hnsw",
                "space_type": "cosinesimil",
                "engine": "nmslib",
                "parameters": {
                    "ef_construction": 128,
                    "m": 64
                }
            }
        }
    }
}

PATENTS_MAPPINGS = {
    "properties": {
        "unique_id": {
            "properties": {
                "patent_number": {
                    "type": "keyword"
                },
                "country_code": {
                    "type": "keyword"
                },
                "kind_code": {
                    "type": "keyword"
                },
            }
        },
        "claims": {
            "type": "text"
        },
        'claims_format': {
            'properties': {
                'data_format': {
                    'type': 'keyword'
                },
                'tree_structure': {
                    'type': 'keyword'
                }
            }
        },
        'specification': {
            "type": "text"
        },
        'specification_format': {
            'properties': {
                'data_format': {
                    'type': 'keyword'
                },
                'tree_structure': {
                    'type': 'keyword'
                }
            }
        },
        'title': {
            'type': 'text'
        },
        'summary': {
            'type': 'text'
        },
        'summary_model_version': {
            'type': 'keyword'
        },
        'short_summary': {
            'type': 'text'
        },
        'short_summary_model_version': {
            'type': 'keyword'
        },
        'topics': {
            'type': 'keyword'
        },
        'topics_model_version': {
            'type': 'keyword'
        },
        'text': {
            'type': 'text'
        },
        'text_format': {
            'type': 'keyword'
        },
    }
}

def create_specification_embedding_index():
    body = {
        "settings": {
            "index": {
                "knn": True,
                "knn.algo_param.ef_search": 100
            }
        },
    }
    try:
        client.indices.create(index='patents_specification_embedding', body=body)
    except Exception as e:
        pass
    client.indices.put_mapping(index='patents_specification_embedding', body=SPECIFICATION_EMBEDDING_MAPPINGS)


def create_claim_embedding_index():
    body = {
        "settings": {
            "index": {
                "knn": True,
                "knn.algo_param.ef_search": 100
            }
        },
    }
    try:
        client.indices.create(index='patents_claim_embedding', body=body)
    except Exception as e:
        pass
    client.indices.put_mapping(index='patents_claim_embedding', body=CLAIM_EMBEDDING_MAPPINGS)


def create_patents_index():
    try:
        client.indices.create(index='patents')
    except Exception as e:
        pass
    client.indices.put_mapping(index='patents', body=PATENTS_MAPPINGS)

def index_patent(unique_id, text, title, text_format=None):
    body = {
        "unique_id": {
            "patent_number": unique_id.patent_number,
            "kind_code": unique_id.kind_code,
            "country_code": unique_id.country_code
        },
        "text": text,
        "title": title
    }

    if text_format:
        body['text_format'] = text_format
    else:
        body['text_format'] = XML_USPTO_POST_2001
        
    client.index(index='patents', id=str(unique_id), body=body)
    return str(unique_id)


def index_claim_embedding(patent_doc_id, embedding, claim_id=None):
    body = {
        "patent_doc_id": patent_doc_id,
        "embedding": embedding
    }
    if claim_id:
        body['claim_id'] = claim_id

    client.index(index='patents_claim_embedding', body=body)

def index_specification_embedding(patent_doc_id, embedding, paragraph_id=None):
    body = {
        "patent_doc_id": patent_doc_id,
        "embedding": embedding
    }
    if paragraph_id:
        body['paragraph_id'] = paragraph_id
    client.index(index='patents_specification_embedding', body=body)

def get_patent_summary(patent: parser.GoogleParsedPatent) -> str:
    response = client.get(index='patents', id=str(patent.unique_id))
    return response['_source'].get('summary')

def update_patent_by_id(patent: parser.GoogleParsedPatent, **kwargs):
    client.update(index='patents', id=str(patent.unique_id), body={'doc': kwargs})

def patent_specification_knn_search(query_vector: list[float]):
    body = {
        'query': {
            'knn': {
                'embedding': {
                    'vector': query_vector,
                    'k': 10
                }
            }
        }
    }
    response = client.search(index='patents_specification_embedding', body=body)
    return [hit['_source'] for hit in response['hits']['hits']]