import boto3
import logging
import os

__version__ = '0.1a'

LOGGER = logging.getLogger(__name__)


class S3Library:
    u"""
    A test library providing AWS S3 support.

        ``S3Library`` is a Robot Framework third party library that enables test to access and upload files to S3.

        == Table of contents ==

        - `Usage`
        - `Examples`
        - `Author`
        - `Developer Manual`
        - `Importing`
        - `Shortcuts`
        - `Keywords`


    = Usage =

    | =Settings= | =Value=         | =Parameter= | =Parameter= | =Parameter= |
    | Library    | S3Library       | ACCESS_KEY  |  SECRET_KEY | BUCKET_NAME |


    = Examples =

    | =Settings= | =Value=         | =Parameter= | =Parameter= | =Parameter= |
    | Library    | S3Library       | ACCESS_KEY  |  SECRET_KEY | BUCKET_NAME |

    = Author =

    Created: 03/25/2024

    Author: Shiela Buitizon | email:shiela.buitizon@mnltechnology.com

    = Developer Manual =

        Compiling this pip package:
            - python setup.py bdist_wheel

        Uploading build to pip
            - python -m twine upload dist/*
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, access_key_id=None, secret_access_key=None, bucket_name=None):
        """
        Initialize with  credentials
        """
        self.aws_access_key_id = access_key_id
        self.aws_secret_access_key = secret_access_key
        self.bucket_name = bucket_name

    def upload_dir_to_s3(self, local_directory, destination):
        """Enumerates and uploads files in local path directory to specified AWS S3 destination path

        Example:
        *** Settings ***
        | Library    | S3Library        | ACCESS_KEY  |  SECRET_KEY | BUCKET_NAME |

        | Upload Directory To S3  | ../target/ | destination/ |
        """
        # Initialize client to None
        client = None
        try:
            client = boto3.client('s3',
                                  aws_access_key_id=self.aws_access_key_id,
                                  aws_secret_access_key=self.aws_secret_access_key)
            for root, dirs, files in os.walk(local_directory):
                for filename in files:

                    # construct the full local path
                    local_path = os.path.join(root, filename)

                    # construct the full dropbox path
                    relative_path = os.path.relpath(local_path, local_directory)
                    s3_path = os.path.join(destination, relative_path)

                    # relative_path = os.path.relpath(os.path.join(root, filename))

                    # print('Searching "%s" in "%s"' % (s3_path, self.bucket_name))
                    # Check if the object exists on S3
                    try:
                        client.head_object(Bucket=self.bucket_name, Key=s3_path)
                        print("Path found on S3! Skipping %s..." % s3_path)
                    except Exception as e:
                        if e.response['Error']['Code'] == '404':
                            # Object does not exist, upload it
                            print("Uploading %s..." % s3_path)
                            client.upload_file(local_path, self.bucket_name, s3_path)
                        else:
                            # Handle other errors
                            print("An error occurred while checking %s: %s" % (s3_path, e))
        finally:
            # Close client
            if client is not None:
                client.close()
