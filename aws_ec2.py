import boto3
import os

def get_running_instance() -> None:
    ec2 =  boto3.client('ec2',region_name="us-east-2")
    reservations = ec2.describe_instances(Filters=[
        {
            "Name":"instance-state-name",
            "Values":["running"],
        }
    ]).get("Reservations")
    for reservation in reservations:
        for instance in reservation["Instances"]:
            print(f"Instance Id:{instance['InstanceId']}, Instance Type: {instance['InstanceType']}, public ip: {instance['PublicIpAddress']}, private ip: {instance['PrivateIpAddress']}")

def stop_ec2_instance(instance_id: str) -> None:
    ec2 = boto3.client("ec2",region_name="us-east-2")
    response = ec2.stop_instances(InstanceIds=[instance_id])
    print(response)

def terminate_ec2_instance(instance_id: str) -> None:
    ec2 = boto3.client("ec2",region_name="us-east-2")
    response = ec2.terminate_instances(InstanceIds=[instance_id])
    print(response)

def create_key_pair() -> None:
    ec2 = boto3.client("ec2",region_name="us-east-2")
    key_pair = ec2.create_key_pair(KeyName="my-ec2-keypair")
    private_key  =  key_pair["KeyMaterial"]

    with os.fdopen(os.open("aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(private_key)

def create_instance() -> None:
    ec2 = boto3.client("ec2",region_name="us-east-2")
    instances = ec2.run_instances(
        ImageId="ami-0d718c3d715cec4a7",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="my-ec2-keypair"
    )

    print(instances["Instances"][0]["InstanceId"])


create_instance()
#create_key_pair()
#terminate_ec2_instance("i-08983c5153fecdf43")
#stop_ec2_instance("i-08983c5153fecdf43")
#get_running_instance()