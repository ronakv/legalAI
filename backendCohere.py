import boto3
import pprint
from botocore.client import Config
from dotenv import load_dotenv
import os
import helpers
import json
import cohere

co = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

load_dotenv()

pp = pprint.PrettyPrinter(indent=2)

session = boto3.session.Session()

region = session.region_name

bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})

bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name='us-west-2', config=bedrock_config,
                                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

bedrock_agent_runtime = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name='us-west-2',
    config=bedrock_config,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
)


def retrieve(query, kbId, numberOfResults=20):
    return bedrock_agent_runtime.retrieve(
        retrievalQuery={
            'text': query
        },
        knowledgeBaseId=kbId,
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': numberOfResults,
                'overRideSearchType': 'SEMANTIC'

            }
        }
    )


def get_answer(query):
    query = "You are a Legal Assistant Helping lawyers do their research. Provide comprehensive answers citing cases " \
            "from the documents as far as possible." + query

    response3 = retrieve(query, "IOJINR6IWU")["retrievalResults"]

    documents = helpers.extract_documents(response3)

    response = co.chat(
        model="command-r-plus",
        message=query,
        documents=documents)

    sources = "Sources: \n"
    prev_title = ""
    for document in response.documents:

        if helpers.format_s3_url(document["title"]) != prev_title:

            sources += "\n" + helpers.format_s3_url(document["title"])

            prev_title = helpers.format_s3_url(document["title"])

    answer = response.text + sources

    return answer


