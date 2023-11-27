import pika
from pika.exceptions import AMQPError
import time
from data import *
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential

def count_messages():
    while True:
        try:
            while True:
                Total_cluster = len(gpu_cluster)
                print(Total_cluster)
            
                # RabbitMQ credentials
                rabbitmq_username = 'admin'
                rabbitmq_password = 'admin'
                
                # Set up a connection to the RabbitMQ server
                credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
                connection = pika.BlockingConnection(pika.ConnectionParameters('172.172.230.65', credentials=credentials,heartbeat=1800))
                channel = connection.channel()

                # Declare the queue you want to consume messages from
                queue_name = 'Queue_tostore_messages'
                channel.queue_declare(queue=queue_name, durable=True)
                
                # Initialize the DefaultAzureCredential using managed identity
                credentials = ClientSecretCredential(client_id=Client_ID, client_secret=Secret_ID, tenant_id=Tenent_ID)

                # Initialize the compute management client with the credential
                compute_client = ComputeManagementClient(credentials, Subscription_ID)
                # Get the message count from the queue
                queue_declare_result = channel.queue_declare(queue=queue_name, passive=True)
                message_count = queue_declare_result.method.message_count
                print(f'Number of messages in the queue "{queue_name}": {message_count}')
                print(message_count)
                break
                if message_count > 0:
                    for j in range(Total_cluster):
                        try:
                            vm = compute_client.virtual_machines.get(gpu_cluster[j][0], gpu_cluster[j][1], expand='instanceView')
                            power_state = next((status for status in vm.instance_view.statuses if 'PowerState' in status.code), None)
                            if power_state.code == 'PowerState/running':
                                print('The VM is running.',gpu_cluster[j][1])
                                continue
                            else:
                                async_op = compute_client.virtual_machines.begin_start(gpu_cluster[j][0], gpu_cluster[j][1])
                                async_op.wait()
                                print('VM started',gpu_cluster[j][1])
                                break
                        except Exception as e:
                            print(f"Error: {str(e)}")
                            
                # Wait for a specific interval before checking again
                time.sleep(10)  # Adjust the interval as needed
        except Exception as e:
            print(f'Error: Unable to count messages - {e}')
            continue

if __name__ == '__main__':
    count_messages()
