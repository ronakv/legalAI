def extract_documents(json_response):
    documents = []
    for entry in json_response:
        title = entry['location']['s3Location']['uri']
        text = entry['content']['text']
        documents.append({"title": title, "snippet": text})
    return documents


def format_s3_url(s3_string, region='us-west-2'):
    """
    Format an S3 URI to a specific URL format.

    Parameters:
    s3_string (str): The S3 URI (e.g., 's3://bucket-name/path/to/file')
    region (str): The AWS region (default is 'us-west-2')

    Returns:
    str: The formatted URL
    """
    # Remove the 's3://' prefix
    s3_path = s3_string[5:]

    # Split the remaining string into bucket name and file path
    bucket_name, file_path = s3_path.split('/', 1)

    # Replace spaces with '+' in the file path
    formatted_file_path = file_path.replace(' ', '+')

    # Construct the formatted URL
    formatted_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{formatted_file_path}"

    return formatted_url
