# Base image
FROM ros:melodic 

ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654

# Basic tools
RUN apt-get update
RUN apt-get install vim nano git tmux wget curl python-pip net-tools iputils-ping -y

# Install additional ros packages
RUN apt-get update && apt-get install ros-melodic-rosbridge-server ros-melodic-joy -y
RUN pip install adafruit-pca9685

# Install packages for web application
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get update && \
    apt-get install nodejs -y
RUN npm install http-server -g

# Install packages for camera use
RUN apt-get update && \
    apt-get install ros-melodic-web-video-server ros-melodic-usb-cam -y

# install gpsd and clients
RUN apt-get update
RUN apt-get install gpsd gpsd-clients i2c-tools libi2c-dev -y

# Add ros sourcing to bashrc
RUN echo ". /opt/ros/melodic/setup.bash" >> ~/.bashrc

# Create Ros workspace
ENV EXOMY_WS=/root/exomy_ws
RUN mkdir -p $EXOMY_WS/src

WORKDIR /root

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
