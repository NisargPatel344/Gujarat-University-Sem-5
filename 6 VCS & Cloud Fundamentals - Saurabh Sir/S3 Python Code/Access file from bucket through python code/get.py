import boto3

def download_from_s3(bucket_name, s3_key, file_name):
    s3 = boto3.client('s3')
    
    try:
        s3.download_file(bucket_name, s3_key, file_name)
        print("File download successfully to S3")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

bucket_name = '5demo0608'
s3_key = 'data.xlsx'
file_name = 'DownloadedData.xlsx'

download_from_s3(bucket_name, s3_key, file_name)
