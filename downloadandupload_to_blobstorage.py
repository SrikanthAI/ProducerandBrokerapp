from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
import zipfile
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageforphotoapp;AccountKey=fj2JswQZLNyqY3e6DWMIONqHaYcXyq5u4p7+h0l6EnnNWMdWGEhHm8PPLNCcfC9HCS+T7kP4V8Hi+AStyjqbQg==;EndpointSuffix=core.windows.net"
container_name = "pcai"
blob_name = "output.zip"
try:
    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    # Create a BlobClient for the zip file you want to download
    blob_client = container_client.get_blob_client(blob_name)
    local_zip_file_path = "C:/Users/konne/Downloads/blobimages1.zip"
    # Download the blob to a local file
    with open(local_zip_file_path, "wb") as my_blob:
        download_stream = blob_client.download_blob()
        my_blob.write(download_stream.readall())

    with zipfile.ZipFile(local_zip_file_path, "r") as zip_ref:
        # Provide the path where you want to extract the images
        extraction_path = "C:/Users/konne/Downloads/blobimages1"
        zip_ref.extractall(extraction_path)
        print(f"Blob '{blob_name}' downloaded to 'local_zip_file.zip'")
except Exception as e:
    print(f"An error occurred: {e}")


