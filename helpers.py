def extract_documents(json_response):
    documents = []
    for entry in json_response:
        title = entry['location']['s3Location']['uri']
        text = entry['content']['text']
        documents.append({"title": title, "snippet": text})
    return documents