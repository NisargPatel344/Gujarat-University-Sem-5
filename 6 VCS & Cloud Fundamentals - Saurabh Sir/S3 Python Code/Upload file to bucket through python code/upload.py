import boto3

def upload_to_s3(bucket_name, file_name, s3_key):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(file_name, bucket_name, s3_key)
        print("File uploaded successfully to S3")
    except FileNotFoundError:
        print("The file was not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

bucket_name = '4demo0608'
file_name = 'data.xlsx'
s3_key = 'UploadedData.xlsx'

upload_to_s3(bucket_name, file_name, s3_key)