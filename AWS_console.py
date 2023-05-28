import boto3
import time
from botocore.exceptions import ClientError
from readings import *


# Function to upload a file to a bucket
def upload_file(s3_resource, bucket_name, file_path, file_name):
    try:
        data = open(file_path, 'rb')
        start = time.time()
        s3_resource.Bucket(bucket_name).put_object(Key=file_name, Body=data)
        end = time.time()

    except ClientError as e:
        print(e)
        return 0
    print(f'"{file_name}" uploaded successfully')
    return end - start


# Function to download a file from a bucket
def download_file(s3_client, bucket_name, file_name):
    try:
        start = time.time()
        s3_client.download_file(bucket_name, file_name, file_name)
        end = time.time()

    except ClientError as e:
        print(e)
        return 0
    print(f'"{file_name}" downloaded successfully')
    return end - start


# Function to delete a file from a bucket
def delete_file(s3_resource, bucket_name, file_name):
    try:
        s3_resource.Object(bucket_name, file_name).delete()

    except ClientError as e:
        print(e)
        return False

    print(f'File "{file_name}" deleted successfully')
    return True


# Function to create a bucket
def create_bucket(s3_resource, bucket_name, region=None):
    try:
        if region is None:
            s3_resource.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_resource.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    except ClientError as e:
        print(e)
        return False
    print(f'Bucket "{bucket_name}" created successfully')
    return True


# Function to delete a bucket
def delete_bucket(s3_client, bucket_name):
    try:
        _ = s3_client.delete_bucket(Bucket=bucket_name)

    except ClientError as e:
        print(e)
        return False
    print(f'Bucket "{bucket_name}" deleted successfully')
    return True


# Function to empty a bucket
def empty_bucket(s3_resource, bucket_name):
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.all().delete()

    except ClientError as e:
        print(e)
        return False
    print(f'Bucket "{bucket_name}" emptied successfully')
    return True


# Function to list the buckets
def list_bucket(s3_client, region_name=None):
    if region_name:
        response = s3_client.list_buckets()
        for bucket in response["Buckets"]:
            if s3_client.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == region_name:
                print(bucket["Name"])
    else:
        response = s3_client.list_buckets()
        for bucket in response["Buckets"]:
            print(bucket["Name"])


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


def get_instance_status(ec2_resource):
    instance_id = input('Enter the instance ID: ')
    instance = ec2_resource.Instance(instance_id)
    print(f'EC2 instance "{instance_id}" state: {instance.state["Name"]}')


def main():
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    ec2_resource = boto3.resource('ec2')

    print('########## Welcome to AWS CLI #####')
    print('\nChoose an AWS Service:')
    user_sel1 = int(input('1. S3\n2. EC2\n3. CloudWatch\n'))

    if user_sel1 == 1:
        print('\nSelected: S3')
        print('1. List Buckets')
        print('2. Create a Bucket')
        print('3. Delete a Bucket')
        print('4. Upload a File')
        print('5. Download a File')
        print('6. Delete a File')
        print('7. Empty Bucket')

        user_sel2 = int(input('\nEnter your choice: '))
        if user_sel2 == 1:
            list_bucket(s3_client)
        elif user_sel2 == 2:
            bucket_name = input('Enter a valid bucket name: ')
            region = input('Enter a valid region name (e.g., eu-north-1): ')
            create_bucket(s3_resource, bucket_name, region)
        elif user_sel2 == 3:
            bucket_name = input('Enter a valid bucket name to be deleted: ')
            delete_bucket(s3_client, bucket_name)
        elif user_sel2 == 4:
            bucket_name = input('Enter the bucket name: ')
            file_path = input('Enter the file path: ')
            file_name = input('Enter the file name: ')
            upload_file(s3_resource, bucket_name, file_path, file_name)
        elif user_sel2 == 5:
            bucket_name = input('Enter the bucket name: ')
            file_name = input('Enter the file name: ')
            download_file(s3_client, bucket_name, file_name)
        elif user_sel2 == 6:
            bucket_name = input('Enter the bucket name: ')
            file_name = input('Enter the file name: ')
            delete_file(s3_resource, bucket_name, file_name)
        elif user_sel2 == 7:
            bucket_name = input('Enter the bucket name: ')
            empty_bucket(s3_resource, bucket_name)
        else:
            print('Invalid choice')

    elif user_sel1 == 2:
        print('\nSelected: EC2')
        region_name = input('\nEnter a valid region name: ')
        ec2_resource = boto3.resource('ec2', region_name=region_name)

        print('1. Start an Instance')
        print('2. Stop an Instance')
        print('3. Get Instance Status')

        user_sel3 = int(input('\nEnter your choice: '))
        if user_sel3 == 1:
            start_instance(ec2_resource)
        elif user_sel3 == 2:
            stop_instance(ec2_resource)
        elif user_sel3 == 3:
            get_instance_status(ec2_resource)
        else:
            print('Invalid choice')

    elif user_sel1 == 3:
        print('\nSelected: CloudWatch')
        plot()

    else:
        print('Invalid choice')

    print('Done')


if __name__ == "__main__":
    main()
