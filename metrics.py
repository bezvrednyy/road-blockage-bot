from time import sleep
import boto3

CloudWatch = boto3.client('cloudwatch')

def send_metrics():
  wait_time = 4*60
  while True:
    CloudWatch.put_metric_data(
      Namespace='Test_Namespace',
      MetricData = [{
        'MetricName': '12 MetricName',
        'Value': 1
      }],
    )
    sleep(wait_time)