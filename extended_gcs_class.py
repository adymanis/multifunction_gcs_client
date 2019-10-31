from google.cloud import storage
import os 

class GCSInterface:
    def __init__(self, bucket_name):
            self.bucket_name = bucket_name
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.get_bucket(bucket_name)

    def list_files(self):
            files = []
            
            """Lists files in the bucket."""
            getblobs = self.storage_client.list_blobs(self.bucket_name)

            for blob in getblobs:
                files.append(blob.name)

            return(files)

    #Uploads multiple files or folders from args ie. gcs.upload_files("Destination_FOLDER","/tmp/testfolder/2.txt","/tmp/testfolder/1.txt")
    def upload_files(self, dest_folder, *source_filenames):
            files = []
            #Format for folder uploads
            if dest_folder:
                if dest_folder == "/":
                    dest_folder = ""
                else:
                    dest_folder = dest_folder+"/"

            """Uploads files to the bucket. And perform check if file or dir was passed"""
            for source_filename in source_filenames:
                if os.path.isfile(source_filename):
                    destination_blob_name = os.path.basename(source_filename)
                        
                    blob = self.bucket.blob(dest_folder+destination_blob_name)
                    blob.upload_from_filename(source_filename)

                    files.append(destination_blob_name)
                #If folder was given we will walk the dir and upload content
                elif os.path.isdir(source_filename):
                    for root, dirs, walkfiles in os.walk(source_filename):
                            for name in walkfiles:
                                filepath = os.path.join(root, name)
                                
                                destination_blob_name = os.path.relpath(filepath, source_filename) 
                                blob = self.bucket.blob(dest_folder+destination_blob_name)
                                blob.upload_from_filename(source_filename+"/"+destination_blob_name)

                                files.append(dest_folder+destination_blob_name)
                            
            return('{} uploaded to folder: {} in bucket: {}.'.format(files, dest_folder, self.bucket_name))

    def delete_files(self, *filenames):
            files = []

            """Deletes files to the bucket."""
            for filename in filenames:
                blob = self.bucket.blob(filename)
                blob.delete()
                files.append(filename)

            return('{} deleted from {}.'.format(files, self.bucket_name))

    def move_files(self, dest_folder, *filenames):
            files = []
            #Format for folder moves
            if dest_folder:
                if dest_folder == "/":
                    dest_folder = ""
                else:
                    dest_folder = dest_folder+"/"
            print(dest_folder)
            
            """Move file in bucket."""
            for filename in filenames:
                #split old 
                pathless_filename = filename.split('/')[-1]
                print(pathless_filename)
                blob = self.bucket.blob(filename)
                self.bucket.rename_blob(blob, dest_folder+pathless_filename)

                files.append(filename)

            return('Files {} has been moved to {}'.format(files, dest_folder))


#Initialize GCS interface with bucket name
gcs = GCSInterface("BUCKET_NAME_HERE")

#list = gcs.list_files()
#print(list)

#upload = gcs.upload_files("", "/path/to/local/file1","/path/to/local/file2", "/path/to/local/folder")
#print(upload)

#delete = gcs.delete_files("path/to/gcs/fil")
#print(delete)

#move = gcs.move_files("DestinationFolderName","path/to/gcs/file")
#print(move)
