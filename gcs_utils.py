from google.cloud import storage
import json

def upload_json_to_gcs(bucket_name, data_dict, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    json_data = json.dumps(data_dict)
    blob.upload_from_string(json_data, content_type='application/json')

def list_files_in_gcs(bucket_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    return [blob.name for blob in blobs]

def get_weather_data_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_contents = blob.download_as_text()
    weather_data = json.loads(file_contents)
    return weather_data
