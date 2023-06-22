from __future__ import print_function
import os
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
import mimetypes
from gapi_authorization import get_creds


def get_folders():
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=get_creds())
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        print(f'An error occurred: {error}')


def send_gmail(to=None, subject=None, msg=None, attachments=None, action='draft'):
    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=get_creds())
        message = EmailMessage()

        # Email Headers
        message['To'] = to
        message['From'] = 'adam.urquhart96@gmail.com'
        message['Subject'] = subject

        # Email Body
        message.set_content(msg)

        # Attachments
        for i in range(len(attachments)):
            attachment_filename = attachments[i]
            # guessing the MIME type
            type_subtype, _ = mimetypes.guess_type(attachment_filename)
            maintype, subtype = type_subtype.split('/')

            with open(attachment_filename, 'rb') as fp:
                attachment_data = fp.read()
            message.add_attachment(attachment_data, maintype, subtype, filename=attachment_filename.split('/')[-1])

        # encode message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
                'raw': encoded_message
        }
        # pylint: disable=E1101

        # Save as draft
        if action == 'draft':
            draft = service.users().drafts().create(userId="me",
                                                    body=create_message).execute()
            print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
            return draft

        # Send message
        elif action == 'send':
            send_message = (service.users().messages().send
                            (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
            return send_message
        else:
            print('ERROR: Action keyword not recognised')

    except HttpError as error:
        print(F'An error occurred: {error}')


if __name__ == '__main__':
    path = '/Users/adamurquhart/data/qardio_graphs/'
    files = [path + file for file in os.listdir(path) if file != '.DS_Store']

    send_gmail(to='margretbarclay10@gmail.com',
               subject='Qardio Data',
               msg='This is automated mail.\n\nPlease find Qardio data figures attached.',
               attachments=files,
               action='draft')
