import pika
import json
import pika
import time
message_stored={}

def process_message(channel, method, properties, body):
   
    print(f'Received message: {body.decode()}')  # Print the message content
    message_data = json.loads(body)

    print('Message Pulled')
    print(message_data)
    '''message_stored['gender']=message_data['gender']
    message_stored['age']=message_data['age']
    message_stored['plan']=message_data['plan']
    message_stored['ethnicity']=message_data['ethnicity']
    message_stored['email']=message_data['email']
    message_stored['runid']=message_data['runid']
    message_stored['input_image_location']=message_data['input_image_location']'''

    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)
    channel.stop_consuming()
    print("ack sent")


'''def delete_from_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))'''

while True:
    if message_stored:
        #input_path_loc = blob_name = parse_url(message_stored['input_image_location'])
        gender = message_stored['gender']
        age = message_stored['age']
        plan = message_stored['plan']
        ethnicity = message_stored['ethnicity']
        email = message_stored['email']
        runid = message_stored['runid']

        '''output_path_loc = input_path_loc.replace('input.zip', 'output.zip')
        output_path_loc1 = input_path_loc.replace('input.zip','output_images/')
        output_path_loc2 = input_path_loc.replace('input.zip','small_images/')
        print('Downloding Zip')
        pull_blob(input_path_loc)
        print('Downloading Completed')
        print('Deleting the Previous Models if present')
        delete_from_folder(output_model_path)
        print('Completed the deletion of the Previous Models if present')


        start_training(input_zip_path = input_path, output_path=output_model_path)

        torch.cuda.empty_cache()


        from infer_model import complete_inference

        complete_inference(out_path = output_path, age = age, gender=gender, plan=plan, ethnicity=ethnicity)

        torch.cuda.empty_cache()
        #delete_from_folder(output_path + '.ipynb_checkpoints')
        print('Training and Inference Completed')
        files = os.listdir('output_images')
        for image in files:
            foo  = Image.open('output_images/' + image)
            foo = foo.resize((384,384),PIL.Image.Resampling.LANCZOS)
            foo.save('small_images/'+image, 'PNG')
            print('images saved to small_images')

        print('Pushing to Blob')
        push_blob(output_path_loc)
        push_blob_images(output_path_loc1,output_path)
        push_blob_images(output_path_loc2,output_small)

        print('Pused Sucessful')

        #Deleting the Input and Output Files.

        os.remove(input_path)
        delete_from_folder(output_path)
        delete_from_folder(output_small)
        delete_from_folder(output_model_path)

        data = {
            "operation":"message_processed",
            "runId":runid,
            "email":email
            }
        try:
            # Send the POST request with JSON data
            response = requests.post(post_url, data=json.dumps(data), headers=headers)

                # Check if the request was successful (status code 200)
            if response.status_code == 200:
                print("API request successful")
                print("Response:", response.text)
            else:
                print("API request failed with status code:", response.status_code)
                print("Response:", response.text)

        except Exception as e:
            print("An error occurred:", str(e))'''
        message_stored={}
    try:
        credentials = pika.PlainCredentials('admin', 'admin')
        connection = pika.BlockingConnection(pika.ConnectionParameters('172.172.230.65', credentials=credentials,heartbeat=1800))
        channel = connection.channel()
        # Declare the queue
        print("start consumer is activated")
        queue_name = "Queue_tostore_messages"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)

        queue_declare_result = channel.queue_declare(queue=queue_name, passive=True)
        q_len = queue_declare_result.method.message_count

        print("1", q_len)
        if q_len == 0:
            time.sleep(100)
            queue_declare_result = channel.queue_declare(queue=queue_name, passive=True)
            q_len = queue_declare_result.method.message_count
            print("2", q_len)
            '''if q_len == 0:
                channel.stop_consuming()'''

        # Consume messages from the queue
        channel.basic_consume(queue=queue_name, on_message_callback=process_message)

        print("Consumer is waiting for messages. To exit, press Ctrl+C")
        # Start consuming messages
        channel.start_consuming()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

