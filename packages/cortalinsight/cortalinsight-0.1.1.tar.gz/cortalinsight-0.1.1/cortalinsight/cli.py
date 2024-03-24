"""
Main Module 
"""
import argparse
from cortalinsight.api import CortalInsightClient
from cortalinsight.exceptions import CIException, CIInvalidRequest


__version__ = '0.1.1'

def setup_arg_parser():
    """
    Set up and return the argument parser
    """
    parser = argparse.ArgumentParser(description="Cortal Insight CLI Tool")
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--setup', action='store_true', help='Setup your api key')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for each command
    subparsers.add_parser('setup', help='Setup your API key')
    subparsers.add_parser('list_datasets', help='Get all datasets')

    get_parser = subparsers.add_parser('get_dataset', help='Get a dataset by ID')
    get_parser.add_argument('id', type=str, help='Dataset ID')

    create_parser = subparsers.add_parser('create_dataset', help='Create a dataset')
    create_parser.add_argument('name', type=str, help='Name of the new dataset')

    delete_parser = subparsers.add_parser('delete_dataset', help='Delete a dataset')
    delete_parser.add_argument('id', type=str, help='Dataset ID to delete')

    delete_metadata_parser = subparsers.add_parser('delete_metadata', help='Delete metdata of a dataset')
    delete_metadata_parser.add_argument('id', type=str, help='Dataset ID to delete')

    upload_parser = subparsers.add_parser('upload_images_from_dir', help='Upload images from directory')
    upload_parser.add_argument('id', type=str, help='Dataset ID to ingest data')
    upload_parser.add_argument('directory_path', type=str, help='Directory to upload images from')

    upload_metadata_parser = subparsers.add_parser('upload_metadata', help='Upload metadata file')
    upload_metadata_parser.add_argument('id', type=str, help='Dataset ID to ingest metadata')
    upload_metadata_parser.add_argument('file_path', type=str, help='File to upload metadata from')

    update_metadata_parser = subparsers.add_parser('update_metadata', help='Update metadata file')
    update_metadata_parser.add_argument('id', type=str, help='Dataset ID to update metadata')
    update_metadata_parser.add_argument('file_path', type=str, help='File to upload metadata from')

    upload_zip_parser = subparsers.add_parser('upload_zip', help='Upload zip from directory')
    upload_zip_parser.add_argument('id', type=str, help='Dataset ID to ingest data')
    upload_zip_parser.add_argument('zip_path', type=str, help='Directory to upload images from')

    validate_parser = subparsers.add_parser('validate_metadata', help='Validate metadata format')
    validate_parser.add_argument('file_path', type=str, help='File to validate metadata from')
    return parser

def process_commands(args, ci_api):
    """
    Process the given command
    """
    if args.command == 'setup':
        response = setup_api_key(ci_api)
    elif args.command == 'get_dataset':
        response = ci_api.get_dataset_by_id(args.id)
    elif args.command == 'list_datasets':
        response = ci_api.list_datasets()
    elif args.command == 'create_dataset':
        response = ci_api.create_dataset(args.name)
    elif args.command == 'delete_dataset':
        response = ci_api.delete_dataset(args.id)
    elif args.command == 'delete_metadata':
        response = ci_api.delete_metadata(args.id)
    elif args.command == 'upload_images_from_dir':
        response = ci_api.upload_images_from_dir(args.id, args.directory_path)
    elif args.command == 'upload_metadata':
        response = ci_api.upload_metadata_file(args.id, args.file_path)
    elif args.command == 'update_metadata':
        response = ci_api.update_metadata_file(args.id, args.file_path)
    elif args.command == 'upload_zip':
        response = ci_api.upload_zip_file(args.id, args.zip_path)
    elif args.command == 'validate_metadata':
        response = ci_api.validate_coco_format(args.file_path)
    else:
        raise CIInvalidRequest(f"Unknown command: {args.command}", 400)
    return response

def setup_api_key(api_client):
    api_key = input("Please enter your API key: ")
    api_client.set_api_key(api_key)
    print("API key has been set up successfully.")

def main():
    parser = setup_arg_parser()
    args = parser.parse_args()

    if args.setup:
        api_client = CortalInsightClient()
        setup_api_key(api_client)

    else:
        try:
            ci_api = CortalInsightClient()
            response = process_commands(args, ci_api)
        except CIException as e:
            print(f"API error occurred: {e}")
        except CIInvalidRequest as e:
            print(f"Invalid request: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
