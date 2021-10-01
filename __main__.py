from cli import cli
from botocore.exceptions import ClientError

try:
    cli()
except ClientError as e:
    print(
        'Cannot Authorize, Please reauth with aws sso login --profile AWSPowerUserAccess' if e.response['Error']['Code'] == 'UnauthorizedException' else e)
