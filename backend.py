import boto3
from botocore.client import Config
from dotenv import load_dotenv
import os

load_dotenv()

# comments

bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})

bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name='us-west-2', config=bedrock_config,
                                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

boto3_session = boto3.session.Session(
    region_name='us-west-2'
)
region_name = boto3_session.region_name

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # For testing with Claude Instant and Claude V2
region_id = region_name

bedrock_agent_runtime = boto3.client(
    service_name="bedrock-agent-runtime"
)


def retrieve(query, kbId, numberOfResults=5):
    return bedrock_agent_runtime.retrieve(
        retrievalQuery={
            'text': query
        },
        knowledgeBaseId=kbId,
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': numberOfResults
            }
        }
    )


response3 = retrieve("Are two kartas legal", "AES9P3MT9T")["retrievalResults"]

print(response3)


def retrieveAndGenerate(input, kbId, sessionId=None, model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                        region_id="us-west-2"):
    model_arn = f'arn:aws:bedrock:{region_id}::foundation-model/{model_id}'
    if sessionId:
        return bedrock_agent_client.retrieve_and_generate(
            input={
                'text': input
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': os.getenv('KBID'),
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": 10
                        }
                    },
                    'modelArn': model_arn,
                    "inferenceConfig": {
                        "textInferenceConfig": {
                            "maxTokens": 10000
                        }
                    }
                }
            },
            sessionId=sessionId
        )
    else:
        return bedrock_agent_client.retrieve_and_generate(
            input={
                'text': input
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kbId,
                    'modelArn': model_arn
                }
            }
        )


def get_answer(query):
    url_list = ''
    query = query + " Provide case names and dates in text if the question is a legal one. Otherwise use the regular model without retrived context"
    print('Querying:')
    print(query)
    response = retrieveAndGenerate(query, os.getenv('KBID'), model_id=model_id, region_id=region_id)

    aws_region = "us-west-2"

    # S3 bucket name
    bucket_name = "legaldocuments-test"

    # Initialize an empty list to hold all the S3 URLs
    s3_urls = []

    # Loop through each citation to extract S3 object URIs and create complete URLs
    for citation in response['citations']:
        for reference in citation['retrievedReferences']:
            s3_uri = reference['location']['s3Location']['uri']
            # Extract the object key from the S3 URI
            object_key = s3_uri.split("/")[-1]
            # Create the S3 URL using the specified format
            s3_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{object_key}"
            s3_urls.append(s3_url)

    # Print all the generated S3 URLs
    for url in s3_urls:
        url_list = url + "\n"

    return response['output']['text'], url_list
