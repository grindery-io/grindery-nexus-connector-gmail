import json
import os
import asyncio
import requests
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from channels.generic.websocket import AsyncJsonWebsocketConsumer


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
        key = params['key']
        session_id = params['sessionId']
        credentials = params['credentials']
        fields = params['fields']

        token = ''
        refresh_token = ''
        expiry = ''

        if 'access_token' in credentials:
            token = credentials['access_token']
        if 'refresh_token' in credentials:
            refresh_token = credentials['refresh_token']
        # if 'expires_in' in credentials:
        #     expiry = credentials['expires_in']
        token_uri = os.environ['token_uri']
        client_id = os.environ['client_id']
        client_secret = os.environ['client_secret']
        scopes = ["https://www.googleapis.com/auth/gmail.send"]

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

        data = {
            'token': token,
            'refresh_token': refresh_token,
            'token_uri': token_uri,
            'client_id': client_id,
            'client_secret': client_secret,
            'scopes': scopes
        }

        creds = Credentials.from_authorized_user_info(data, scopes)

        try:
            service = build('gmail', 'v1', credentials=creds)
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