from botocore.exceptions import ClientError
from pathlib import Path
import boto3
import boto3.session
import json
import os
from dataclasses import dataclass
from datetime import datetime


class SSO:
    def __init__(self) -> None:
        self.region = 'us-east-1'
        user_profile_directory = Path(os.getenv('USERPROFILE'))
        sso_cache_directory = user_profile_directory / '.aws' / 'sso' / 'cache'
        sso_cache_files = sso_cache_directory.glob('*.json')
        sso_cache_file = max(sso_cache_files, key=lambda x: x.stat().st_mtime)

        self.access_token = json.loads(sso_cache_file.read_text())[
            'accessToken']

        self.client = boto3.client('sso', region_name=self.region)
        self.cred_table = {}

    def getAccounts(self):
        return self.client.list_accounts(accessToken=self.access_token)

    def getCreds(self, account_id):
        if account_id in self.cred_table:
            timestamp = datetime.timestamp(datetime.now())
            if timestamp < self.cred_table[account_id].expiration - 60:
                return self.cred_table[account_id]
        try:
            creds = self.client.get_role_credentials(
                accountId=account_id, accessToken=self.access_token, roleName='AWSPowerUserAccess')
            self.cred_table[account_id] = Credentials(access_key=creds['roleCredentials']['accessKeyId'], secret_access_key=creds['roleCredentials']
                                                      ['secretAccessKey'], session_token=creds['roleCredentials']['sessionToken'], expiration=creds['roleCredentials']['expiration'])
            return self.cred_table[account_id]

        except ClientError as e:
            print(account_id, e)
            return

    def getRegions(self):
        initAccount = self.getAccounts()['accountList'][0]['accountId']
        initCreds = self.getCreds(initAccount)
        ec2 = boto3.client('ec2', region_name='us-east-1', aws_access_key_id=initCreds.access_key,
                           aws_secret_access_key=initCreds.secret_access_key, aws_session_token=initCreds.session_token)
        return [region['RegionName']
                for region in ec2.describe_regions()['Regions']]


@dataclass
class Credentials:
    access_key: str
    secret_access_key: str
    session_token: str
    expiration: int