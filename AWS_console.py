import boto3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from operator import itemgetter
import logging
from botocore.exceptions import ClientError
import time
from readings import *


#listing of files in a bucket
def list_buckets(s3_client):
    response = s3_client.list_buckets()
    print('Buckets:')
    for bucket in response['Buckets']:
        print(bucket['Name'])

#creating a bucket
def create_bucket(s3_resource):
    bucket_name = input('Enter a valid bucket name: ')
    region = input('Enter a valid region name (e.g., eu-north-1): ')
    try:
        s3_resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f'Bucket "{bucket_name}" created successfully')
    except ClientError as e:
        print(e)

#deleting a bucket function
def delete_bucket(s3_client):
    bucket_name = input('Enter a valid bucket name to be deleted: ')
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f'Bucket "{bucket_name}" deleted successfully')
    except ClientError as e:
        print(e)

#uploading a file to a bucket
def upload_file(s3_resource):
    bucket_name = input('Enter the bucket name: ')
    file_path = input('Enter the file path: ')
    file_name = input('Enter the file name: ')
    try:
        s3_resource.meta.client.upload_file(file_path, bucket_name, file_name)
        print(f'File "{file_name}" uploaded successfully to bucket "{bucket_name}"')
    except ClientError as e:
        print(e)

#downlaoding a file from a bucket
def download_file(s3_client):
    bucket_name = input('Enter the bucket name: ')
    file_name = input('Enter the file name: ')
    try:
        s3_client.download_file(bucket_name, file_name, file_name)
        print(f'File "{file_name}" downloaded successfully from bucket "{bucket_name}"')
    except ClientError as e:
        print(e)

#deleting a file from a bucket
def delete_file(s3_resource):
    bucket_name = input('Enter the bucket name: ')
    file_name = input('Enter the file name: ')
    try:
        s3_resource.Object(bucket_name, file_name).delete()
        print(f'File "{file_name}" deleted successfully from bucket "{bucket_name}"')
    except ClientError as e:
        print(e)

#emptying the contents of a bucket
def empty_bucket(s3_resource):
    bucket_name = input('Enter the bucket name: ')
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.delete()
        print(f'Bucket "{bucket_name}" emptied successfully')
    except ClientError as e:
        print(e)

#starting an ec2 instance
def start_instance(ec2_resource):
    instance_id = input('Enter the instance ID: ')
    try:
        response = ec2_resource.start_instances(InstanceIds=[instance_id], DryRun=True)
        if 'DryRunOperation' not in response:
            raise ClientError("Dry run failed.")
    except ClientError as e:
        print(e)
        return

    try:
        response = ec2_resource.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(f'Instance "{instance_id}" started successfully')
    except ClientError as e:
        print(e)

def stop_instance(ec2_resource):
    instance_id = input('Enter the instance ID: ')
    try:
        response = ec2_resource.stop_instances(InstanceIds=[instance_id], DryRun=True)
        if 'DryRunOperation' not in response:
            raise ClientError("Dry run failed.")
    except ClientError as e:
        print(e)
        return

    try:
        response = ec2_resource.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(f'Instance "{instance_id}" stopped successfully')
    except ClientError as e:
        print(e)


def terminate_instance(ec2_resource):
    instance_id = input('Enter the instance ID: ')
    try:
        response = ec2_resource.terminate_instances(InstanceIds=[instance_id], DryRun=True)
        if 'DryRunOperation' not in response:
            raise ClientError("Dry run failed.")
    except ClientError as e:
        print(e)
        return

    try:
        response = ec2_resource.terminate_instances(InstanceIds=[instance_id], DryRun=False)
        print(f'Instance "{instance_id}" terminated successfully')
    except ClientError as e:
        print(e)


def plot_readings():
    plot()


def main():
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')
    ec2_resource = boto3.resource('ec2')

    print('AWS CLI\n')
    print('1. S3')
    print('2. EC2')
    print('3. CloudWatch')

    user_choice = input('Enter your choice (1-3): ')
    options = {
        '1': {
            '1': lambda: list_buckets(s3_client),
            '2': lambda: create_bucket(s3_resource),
            '3': lambda: delete_bucket(s3_client),
            '4': lambda: upload_file(s3_resource),
            '5': lambda: download_file(s3_client),
            '6': lambda: delete_file(s3_resource),
            '7': lambda: empty_bucket(s3_resource)
        },
        '2': {
            '1': lambda: start_instance(ec2_resource),
            '2': lambda: stop_instance(ec2_resource),
            '3': lambda: terminate_instance(ec2_resource)
        },
        '3': {
            '1': plot()
        }
    }

    if user_choice in options:
        print(f'\nSelected: {options[user_choice]["1"].__name__}\n')
        while True:
            print('Actions:')
            if user_choice == '1':
                print('1. List buckets')
                print('2. Create bucket')
                print('3. Delete bucket')
                print('4. Upload file')
                print('5. Download file')
                print('6. Delete file')
                print('7. Empty bucket')
                print('0. Back')
            elif user_choice == '2':
                print('1. Start instance')
                print('2. Stop instance')
                print('3. Terminate instance')
                print('0. Back')
            elif user_choice == '3':
                print('1. Plot')
                print('0. Back')

            action = input('Enter your action (0 to go back): ')
            if action == '0':
                break

            if action in options[user_choice]:
                options[user_choice][action]()
            else:
                print('Invalid action')
    else:
        print('Invalid choice')

    print('Done')


if __name__ == "__main__":
    main()
