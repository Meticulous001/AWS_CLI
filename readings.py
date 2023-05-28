import boto3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from operator import itemgetter


# client = boto3.client('cloudwatch', aws_access_key_id='AKIAVD3NS4W7IU5YPBUT',
#     aws_secret_access_key='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', region_name='eu-north-1')

client = boto3.client('cloudwatch', region_name='eu-north-1')

#Getting CP Utilization for our instance
def utilization(instance_id):
    response1 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[

            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ],

        StartTime=datetime.now() - timedelta(hours=2),
        EndTime=datetime.now(),
        Period=300,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )

    y1 = []
    x1 = []

    LatencyList1 = []
    for item in response1['Datapoints']:
        LatencyList1.append(item)

    LatencyList1 = sorted(LatencyList1, key=itemgetter('Timestamp'))


    for i in range(0, len(LatencyList1), 1):

        y1.append(LatencyList1[i]['Average'])
        x1.append(LatencyList1[i]['Timestamp'])

    return y1,x1

#Getting Packets IN for our instance
def NetworkIn():

    response2 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='NetworkIn',
        Dimensions=[

            {
                'Name': 'InstanceId',
                'Value': 'i-0eb0378fa1e6fe0fd'
            },
        ],

        StartTime=datetime.now() - timedelta(hours=2),
        EndTime=datetime.now(),
        Period=300,
        Statistics=[
            'Average',
        ],
        Unit='Bytes'
    )

    y2 = []
    x2 = []

    LatencyList2 = []
    for item in response2['Datapoints']:
        LatencyList2.append(item)

    LatencyList2 = sorted(LatencyList2, key=itemgetter('Timestamp'))


    for i in range(0, len(LatencyList2), 1):

        y2.append(LatencyList2[i]['Average'])
        x2.append(LatencyList2[i]['Timestamp'])

    return y2,x2

#Getting Status Check Failed for our instance
def StatusCheckFailed():

    response3 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='StatusCheckFailed',
        Dimensions=[

            {
                'Name': 'InstanceId',
                'Value': 'i-0eb0378fa1e6fe0fd'
            },
        ],

        StartTime=datetime.now() - timedelta(hours=2),
        EndTime=datetime.now(),
        Period=300,
        Statistics=[
            'Average',
        ],
        Unit='Count'
    )

    y3 = []
    x3 = []

    LatencyList3 = []
    for item in response3['Datapoints']:
        LatencyList3.append(item)

    LatencyList3 = sorted(LatencyList3, key=itemgetter('Timestamp'))


    for i in range(0, len(LatencyList3), 1):

        y3.append(LatencyList3[i]['Average'])
        x3.append(LatencyList3[i]['Timestamp'])

    return y3,x3

#Getting NetworkOut for our instance

def NetworkOut():

    response4 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='NetworkOut',
        Dimensions=[

            {
                'Name': 'InstanceId',
                'Value': 'i-0eb0378fa1e6fe0fd'
            },
        ],

        StartTime=datetime.now() - timedelta(hours=2),
        EndTime=datetime.now(),
        Period=300,
        Statistics=[
            'Average',
        ],
        Unit='Bytes'
    )

    y4 = []
    x4 = []

    LatencyList4 = []
    for item in response4['Datapoints']:
        LatencyList4.append(item)

    LatencyList4 = sorted(LatencyList4, key=itemgetter('Timestamp'))


    for i in range(0, len(LatencyList4), 1):

        y4.append(LatencyList4[i]['Average'])
        x4.append(LatencyList4[i]['Timestamp'])

    return y4,x4



#################### PLOTTING ###############################3
def plot():
    instance_id = input('Enter the instance id \n')
    y1,x1 = utilization(instance_id)
    y2,x2 = StatusCheckFailed()
    y3,x3 = NetworkIn()
    y4,x4 = NetworkOut()

    # Initialise the subplot function using number of rows and columns
    figure, axis = plt.subplots(2, 2)

    # For CPU utilization
    axis[0, 0].plot(x1,y1)
    axis[0, 0].set_title('CPU utilization')
    axis[0, 0].set_ylabel('Average Percent %')

    #for self status check
    axis[0, 1].plot(x2,y2)
    axis[0, 1].set_title('Status Check Failed')
    axis[0, 1].set_ylabel('Count')

    # For Network In
    axis[1, 0].plot(x3,y3)
    axis[1, 0].set_title("Network In")
    axis[1, 0].set_ylabel('Bytes')

    # For Network In
    axis[1, 1].plot(x4,y4)
    axis[1, 1].set_title("Network Out")
    axis[1, 1].set_ylabel('Bytes')


    plt.show()
