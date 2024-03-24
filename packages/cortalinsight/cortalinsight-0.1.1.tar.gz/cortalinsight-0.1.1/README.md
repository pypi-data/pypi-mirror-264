# Cortal Insight CLI Tool

The Cortal Insight CLI Tool is a command-line interface for interacting with the Cortal Insight API, allowing you to manage datasets conveniently through your terminal.


## Setup

## Documentation
Dashboard documentation
Docs / API 

## Installation 
```
pip install cortalinsight
```

or 

```
git clone https://github.com/cortal-insight/cortal-insight-python-client

cd path/to/cortal-insight-python-client

pip install .
```
## Get started

1. Create your account
Sign up in the Cortal Insight dashboard

2. Request your API key for the service

3. Set your API key 
```
cortalinsight setup "YOUR_API_KEY_HERE"
```

## Usage

1. Creating a dataset

```
cortalinsight create_dataset <dataset_name>
```

2. List all datasets
```
cortalinsight list_datasets
```

3. Get dataset by id
```
cortalinsight get_dataset <dataset_id>
```

4. Delete dataset by id
```
cortalinsight delete_dataset <dataset_id>
```

5. Upload images from directory to dataset
```
cortalinsight upload_images_from_dir <dataset_id>  <directory_containing_images>
```

6. Upload zip of images  to dataset
```
cortalinsight upload_zip <dataset_id>  <zip_containing_images>
```
   
7. Upload metadata to dataset
```
cortalinsight upload_metadata <dataset_id>  <file_containing_metadata>
```
   
8. Update metadata to dataset
```
cortalinsight update_metadata <dataset_id>  <file_containing_metadata>
```
   
9. Validate metadata to dataset
```
cortalinsight validate_metadata  <dfile_containing_metadata>
```



This project is licensed under the MIT License - see the LICENSE file for details.
