import docker
import json
import multiprocessing
import time

# Read in the scripts configuration settings
f = open('config.json')
config_data = json.load(f)
f.close()
container_name = (config_data['container_name'])
run_freq       = (config_data['initial_freq'])
output_file    = (config_data['output_file'])
file_format    = (config_data['format'])

def background_task(pause_event):
    # Connect to Docker API and get stats, wait, then repeat
    
    while True:
        if pause_event.is_set():
            pause_event.wait()
        else:
            f = open('config.json')
            config_data = json.load(f)
            f.close()
            local_run_freq = (config_data['initial_freq'])
            local_container_name = (config_data['container_name'])
            local_output_file    = (config_data['output_file'])
            local_format         = (config_data['format'])
            client = docker.from_env()
            container = client.containers.get(local_container_name)
            stats = container.stats(decode=None, stream = False)
            with open(local_output_file, 'a') as json_file:
                json.dump(stats, json_file, indent=2)
            client.close()
            time.sleep(local_run_freq)

if __name__ == "__main__":
    # Create an event to control the pause/resume state
    pause_event = multiprocessing.Event()
    # Create a background process
    background_process = multiprocessing.Process(target=background_task, args=(pause_event,))
    # Start the process and immediately pause it
    background_process.start()
    pause_event.set()

    # Loop on user input until exit command
    while True:
        print ("")
        print("The following commands are available:")
        print(" start : starts the monitoring process")
        print(" stop : stops the monitoring process")
        print(" freq : sets monitoring frequency")
        print(" format : switches between json and csv")
        print(" exit : exits this program")
        user_input = input("> ")
        if user_input == "start":
            pause_event.clear()
            print("start")
        elif user_input == "stop":
            pause_event.set()
            print("stop")
        elif user_input == "freq":
            print("Current frequency is: " + str(run_freq) + " seconds")
            run_freq = input("Please enter new frequency: ")
            config_data['initial_freq'] = int(run_freq)
            with open('config.json', 'w') as json_file:
                json.dump(config_data, json_file, indent=2)
        elif user_input == "format":
            print("Current format is " + file_format)
            print(file_format)
            file_format = input("Please enter new format (json or csv): ")
            if "csv" in file_format:
                print("Using csv as file format")
                file_format = "csv"
            elif "json" in file_format:
                print("Using json as file format")
                file_format = "json"
            else:
                print("Invalid input, using json as file format")
                file_format = "json"
            config_data['format'] = file_format
            with open('config.json','w') as json_file:
                json.dump(config_data, json_file, indent=2)
        elif user_input == "exit":
            background_process.terminate()
            break
        else:
            print("Invalid input!")
