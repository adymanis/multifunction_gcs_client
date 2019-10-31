# multifunction_gcs_client
Simplified Google Cloud Storage client written in python. 

Requires:
pip install google-cloud-storage 

Usage:
  Initialize Instance:
    gcs = GCSInterface("BUCKET_NAME_HERE")

  List Objects in bucket (Returns a list of file with full path name):
    list = gcs.list_files()
    print(list)

  Upload Objects in bucket (Uploads a list of files or folders into GCS bucket, optionally specify folder in bucket)
    upload = gcs.upload_files("DestinationFolderName", "/path/to/local/file1","/path/to/local/file2", "/path/to/local/folder")
    print(upload)

  Deletes objects in bucket(Can take multiple files)
    delete = gcs.delete_files("path/to/gcs/file1","path/to/gcs/file2")
    print(delete)

  Moves objects around in bucket(Takes desitnation folder and can take multiple files)
    move = gcs.move_files("DestinationFolderName","path/to/gcs/file")
    print(move)



