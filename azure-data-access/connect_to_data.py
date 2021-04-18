"""

Need to pip install azure-storage-blob
Working to get an example loader from azure

"""

from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, ContainerClient, BlobClient
import pandas as pd
from collections import defaultdict


if __name__ == "__main__":
    # blob_service_client = BlobServiceClient(account_url="https://datavillagesa.blob.core.windows.net")
    url_postfix = 'sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl'
    url = 'https://datavillagesa.blob.core.windows.net/northernlights?'
    nl_container = ContainerClient.from_container_url(container_url=url+url_postfix)
    blob_list = nl_container.list_blobs()
    output = defaultdict(list)
    for blob in blob_list:
        output['SourceName'].append(blob.name)
        blob_client = BlobClient.from_blob_url(blob_url=f"https://datavillagesa.blob.core.windows.net/northernlights/{blob.name}?{url_postfix}")
        with open("./BlockDestination.txt", "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
            print('here')
    pd.DataFrame(output).to_csv('name_list.csv')
    print('here')
