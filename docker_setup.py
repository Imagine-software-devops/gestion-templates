import os 
import docker

# os.system('sudo apt install docker.io')
# os.system('python.exe -m pip install --upgrade pip')
client = docker.from_env()
# Create container
container = client.containers.create(
    image='ubuntu:latest',  
    command='/bin/bash',    
    detach=True,            # Run the container in the background
    tty=True                # Allocate a pseudo-TTY (useful for interactive processes)
)
# Start container
container.start()
# Stop container
# container.stop()
# # get logs
# logs = container.logs()
# # Create a volume
# volume = client.volumes.create()
# # Attach the volume to a container
# container = client.containers.create(
#     image='your_image:tag',
#     volumes={'/path/in/container': {'bind': '/path/in/host', 'mode': 'rw'}}
# )

# # Create a network
# network = client.networks.create('your_network')

# # Attach the network to a container
# container = client.containers.create(
#     image='your_image:tag',
#     network='your_network'
# )
# # if need to remove
# # Remove a container
# container.remove()

# # Remove a volume
# volume.remove()

# # Remove a network
# network.remove()