#!/bin/bash
# run_exomy- A script to run containers for dedicated functions of exomy

help_text="Usage: "$0" [MODE] [OPTIONS]
    A script to run ExoMy in different configurations
    Options:
        -a, --autostart     Toggles autostart mode on or off
        -c, --config        Runs the motor configuration of ExoMy
        -d, --devel         Runs the development mode to change some code of ExoMy 
        -h, --help          Shows this text
"

### Main
# Initialize parameters 
container_name="exomy"
image_name="exomy"

# Process parameters
if [ "$1" != "" ]; then
    case $1 in
        -a | --autostart)       
                                container_name="${container_name}_autostart"
                                start_command="autostart"
                                options="--restart always"
                                 
                                ;;
        -s | --stop_autostart)  
                                docker container stop "${container_name}_autostart"
                                exit     
                                ;;
        -c | --config)          
                                container_name="${container_name}_config"
                                start_command="config"
                                options="--rm"
                                ;;
        -d | --devel)           
                                container_name="${container_name}_devel"
                                start_command="devel"
                                options="--restart always"
                                ;;  
        -h | --help )           echo "$help_text"
                                exit
                                ;;
        * )                     echo "ERROR: Not a valid mode!"
                                echo "$help_text"
                                exit 1
    esac
else
    echo "ERROR: You need to specify a mode!"
    echo "$help_text"
    exit
fi

# Build docker image from Dockerfile in directory 
directory=$( dirname "$0" )
docker build -t $image_name $directory

# Stop any of the 3 containers if running
RUNNING_CONTAINERS=$( docker container ls -a -q --filter ancestor=exomy )
if [ -n "$RUNNING_CONTAINERS" ]; then
    docker rm -f "$RUNNING_CONTAINERS"
fi

# Run docker container
docker run \
    -it \
    -v ~/ExoMy_Software:/root/exomy_ws/src/exomy \
    -v ~/ExoMy_Software/modules/ros-imu-bno055:/root/exomy_ws/src/ros-imu-bno055 \
    -v ~/ExoMy_Software/modules/vl53l0x-ros:/root/exomy_ws/src/vl53l0x-ros \
    -v ~/ExoMy_Software/modules/gps_umd_orig:/root/exomy_ws/src/gps_umd \
    -v ~/ExoMy_Software/modules/traffic-cone:/root/exomy_ws/src/traffic-cone \
    -p 8000:8000 \
    -p 8080:8080 \
    -p 9090:9090 \
    --privileged \
    -v /dev/serial0:/dev/serial0 \
    ${options} \
    --name "${container_name}" \
    "${image_name}" \
    "${start_command}"



    # -v ~/ExoMy_Software/modules/gps_umd/gps_common:/root/exomy_ws/src/gps_umd/gps_common \
    # -v ~/ExoMy_Software/modules/gps_umd/gps_umd:/root/exomy_ws/src/gps_umd/gps_umd \
    # -v ~/ExoMy_Software/modules/gps_umd/gps_client:/root/exomy_ws/src/gps_umd/gps_client \