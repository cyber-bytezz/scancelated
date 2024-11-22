from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobServiceClient, __version__, generate_blob_sas, BlobSasPermissions
import os
from datetime import datetime, timedelta, timezone


account_name = os.getenv('ACCOUNT_NAME')
account_key = os.getenv('ACCOUNT_KEY')
output_container_name = os.getenv('OUTPUT_CONTAINER_NAME')
blob_name = os.getenv('BLOB_NAME')
connection_str =  f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"


def get_download_link(blob_name):
    expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    permissions = BlobSasPermissions(read=True)
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=output_container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=permissions,
        expiry=expiry
    )
    download_link = f"https://{account_name}.blob.core.windows.net/{output_container_name}/{blob_name}" #?{sas_token}"
    print("Download link:", download_link)
    return download_link


def upload_file_to_blob(file_content, blob_name):
    try:
        blob_name = f'{blob_name}.zip'
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        output_blob_client = blob_service_client.get_blob_client(container=output_container_name, blob=blob_name)
        modified_date = datetime.now()
        output_blob_client.upload_blob(file_content, overwrite=True)
        print(f'Uploaded content to blob storage as {blob_name}')
        output_path = get_download_link(blob_name)
        return output_path, modified_date.isoformat()
    except Exception as e:
        print(f"Error uploading content to blob storage: {str(e)}")
        return None, None

def upload_pdf_to_blob(file_content, blob_name):
    try:
        blob_name = f'{blob_name}.pdf'
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        output_blob_client = blob_service_client.get_blob_client(container=output_container_name, blob=blob_name)
        modified_date = datetime.now()
        output_blob_client.upload_blob(file_content, overwrite=True)
        print(f'Uploaded content to blob storage as {blob_name}')
        output_path = get_download_link(blob_name)
        return output_path, modified_date.isoformat()
    except Exception as e:
        print(f"Error uploading content to blob storage: {str(e)}")
        return None, None
