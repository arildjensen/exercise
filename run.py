import docker
import json
import csv
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

# Create a background task that will query the container metrics and write output to a file
def background_task(pause_event):
    # Connect to Docker API and get stats, wait, then repeat
    
    while True:
        if pause_event.is_set():
            # If we are paused, do nothing
            pause_event.wait()
        else:
            # If we are NOT paused, read config settings
            f = open('config.json')
            config_data = json.load(f)
            f.close()
            local_run_freq = (config_data['initial_freq'])
            local_container_name = (config_data['container_name'])
            local_output_file    = (config_data['output_file'])
            local_format         = (config_data['format'])
            # Get metrics from running Docker container
            client = docker.from_env()
            container = client.containers.get(local_container_name)
            stats = container.stats(decode=None, stream = False)
            # Write to output file
            with open(local_output_file, 'a') as json_file:
                json.dump(stats, json_file, indent=2)
            client.close()
            # Pause a set time until we repeat what we just did
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
        print(" output : set the name of the output file")
        print(" exit : exits this program")
        user_input = input("> ")
        if user_input == "start":
            # Unpause the background process and start collecting metrics
            pause_event.clear()
            print("start")
        elif user_input == "stop":
            # Stop the background process and the collection of metrics
            pause_event.set()
            print("stop")
        elif user_input == "freq":
            # Set the collection frequency and write to the config file
            print("Current frequency is: " + str(run_freq) + " seconds")
            run_freq = input("Please enter new frequency: ")
            config_data['initial_freq'] = int(run_freq)
            with open('config.json', 'w') as json_file:
                json.dump(config_data, json_file, indent=2)
        elif user_input == "format":
            # Set the output format and write to the config file
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
        elif user_input == "output":
            # Set the output file name and write to the config file
            print("Current output is " + output_file)
            output_file = input("Pleasae enter new output file name: ")
            config_data['output_file'] = output_file
            with open('config.json','w') as json_file:
                json.dump(config_data, json_file, indent=2)
        elif user_input == "exit":
            # Stop the background process and exit this script
            background_process.terminate()
            break
        else:
            print("Invalid input!")
