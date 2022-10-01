import json
import os
import asyncio
import requests
import base64
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from channels.generic.websocket import AsyncJsonWebsocketConsumer

os.environ["CDS_NAME"] = "gmailSender"
REQUEST_PREFIX = os.path.expandvars(os.environ["CREDENTIAL_MANAGER_REQUEST_PREFIX"])

class HttpRequestWrapper(HttpRequest):
    def __init__(self, *args, **kwargs):
        if "uri" in kwargs:
            kwargs["uri"] = REQUEST_PREFIX + re.sub(r"^https://", "", kwargs["uri"])
        elif len(args) >= 3:
            args = list(args)
            args[2] = REQUEST_PREFIX + re.sub(r"^https://", "", args[2])
        super().__init__(*args, **kwargs)

class SocketAdapter(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_tasks = set()
        self.connected = False

    async def connect(self):
        self.connected = True
        await self.accept()

    async def disconnect(self, close_code):
        self.connected = False
        print('-----socket disconnected-----')

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        request = json.loads(text_data)
        method = request.get("method", None)
        params = request.get("params", None)
        id = request.get("id", None)
        if method == 'ping':
            response = {
                'jsonrpc': '2.0',
                'result': {},
                'id': id
            }
            await self.send_json(response)
            return
        key = params['key']
        session_id = params['sessionId']
        fields = params['fields']

        token = params['authentication']


        to = ''
        cc = ''
        bcc = ''
        subject = ''
        content = ''
        if 'to' in fields:
            to = fields['to']
        if 'cc' in fields:
            cc = fields['cc']
        if 'bcc' in fields:
            bcc = fields['bcc']
        if 'subject' in fields:
            subject = fields['subject']
        if 'message' in fields:
            content = fields['message']

        creds = Credentials(token)

        try:
            service = build('gmail', 'v1', credentials=creds,  requestBuilder=HttpRequestWrapper)
            message = EmailMessage()

            message.set_content(content)

            message['To'] = to
            message['From'] = 'djangodeveloper961018@gmail.com'
            message['Cc'] = cc
            message['Bcc'] = bcc
            message['Subject'] = subject

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {
                'raw': encoded_message
            }
            service.users().messages().send(userId="me", body=create_message).execute()

            response = {
                'jsonrpc': '2.0',
                'result': {
                    'key': key,
                    'sessionId': session_id,
                    'payload': fields
                },
                'id': id
            }
            await self.send_json(response)

        except HttpError as error:
            print(f'An error occurred: {error}')
            send_message = None