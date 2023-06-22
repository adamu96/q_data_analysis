from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gapi_authorization import get_creds

import google.auth
from googleapiclient.http import MediaFileUpload

def get_files():

    try:
        service = build('drive', 'v3', credentials=get_creds())

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def create_folder():
    """
    Create a folder and prints the folder ID
    """
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=get_creds())
        file_metadata = {
            'name': 'Invoices',
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        print(F'Folder ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def upload_to_folder(folder_id):
    """
    Args: Id of the folder
    Returns: ID of the file uploaded
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': 'photo.jpg',
            'parents': [folder_id]
        }
        media = MediaFileUpload('download.jpeg',
                                mimetype='image/jpeg', resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


if __name__ == '__main__':
    # create_folder()
    # upload_to_folder(folder_id='1s0oKEZZXjImNngxHGnY0xed6Mw-tvspu')
    get_files()