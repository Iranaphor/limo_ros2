#FROM westonrobot/ros:humble-ci
FROM westonrobot/limo_ros:humble_22082023

ENV DEBIAN_FRONTEND=noninteractive
# Set up user account
#RUN useradd -ms /bin/bash ros && echo "ros:ros" | chpasswd && adduser ros sudo
RUN adduser ros video
RUN adduser ros audio

# Builder dependencies installation
RUN apt-get update \
    && apt-get install -qq -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libssl-dev \
    libusb-1.0-0-dev \
    pkg-config \
    libgtk-3-dev \
    libglfw3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libglvnd0 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
    curl \  
    libusb-1.0* \
    udev \
    apt-transport-https \
    ca-certificates \
    curl \
    swig \
    software-properties-common \
    python3-pip \
    ros-humble-simulation \
    ros-humble-rmw-cyclonedds-cpp \
    ros-humble-rviz2* \
    ros-humble-cartographer* \
    ros-humble-nav* \
    ros-humble-teleop-twist-keyboard \
    ros-humble-joint-state-publisher* \
    ros-humble-robot-state-publisher* \ 
    ros-humble-xacro \
    ros-humble-imu-tools \
    libgflags-dev \
    nlohmann-json3-dev \
    ros-humble-image-* \
    && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/YDLIDAR/YDLidar-SDK.git &&\
    mkdir -p YDLidar-SDK/build && \
    cd YDLidar-SDK/build &&\
    cmake ..&&\
    make &&\
    make install &&\
    cd .. &&\
    pip install . &&\
    cd .. && rm -r YDLidar-SDK 
RUN wget -c https://github.com/google/glog/archive/refs/tags/v0.6.0.tar.gz  -O glog-0.6.0.tar.gz &&\
    tar -xzvf glog-0.6.0.tar.gz &&\
    cd glog-0.6.0 &&\
    mkdir build && cd build &&\
    cmake .. && make -j4 &&\
    sudo make install &&\
    sudo ldconfig &&\
    cd ../.. && rm -r glog-*
RUN wget -c https://github.com/Neargye/magic_enum/archive/refs/tags/v0.8.0.tar.gz -O  magic_enum-0.8.0.tar.gz &&\
    tar -xzvf magic_enum-0.8.0.tar.gz &&\
    cd magic_enum-0.8.0 &&\
    mkdir build && cd build &&\
    cmake .. && make -j4 &&\
    sudo make install &&\
    sudo ldconfig &&\
    cd ../.. && rm -r magic_enum*
RUN git clone https://github.com/libuvc/libuvc.git &&\
    cd libuvc &&\
    mkdir build && cd build &&\
    cmake .. && make -j4 &&\
    sudo make install &&\
    sudo ldconfig  &&\
    cd ../.. && rm -r libuvc*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Add scripts to the bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> /home/ros/.bashrc
RUN echo "source /workspaces/limo_ros2/install/setup.bash" >> /home/ros/.bashrc
RUN echo "echo 'LIMO ready for action!'" >> /home/ros/.bashrc
RUN echo "echo 'Dont forget to run an sudo apt update when you first connect!'" >> /home/ros/.bashrc
RUN apt-get update

# Execute any PIP installs
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install tmule==1.5.9

# Install development utilities
RUN apt-get install -qq -y --no-install-recommends nano 
RUN apt-get install -qq -y --no-install-recommends tmux
RUN apt-get install -qq -y --no-install-recommends tree

# Install network moonitoring utilities
RUN apt-get install -qq -y --no-install-recommends net-tools
RUN apt-get install -qq -y --no-install-recommends iputils-ping

# PIP installs for custom_package: verbaliser
RUN apt-get install -qq -y --no-install-recommends espeak
RUN apt-get install -qq -y --no-install-recommends alsa-utils
RUN apt-get install -qq -y --no-install-recommends sox
RUN apt-get install -qq -y --no-install-recommends portaudio19-dev
RUN apt-get install -qq -y --no-install-recommends flac
RUN python3 -m pip install SpeechRecognition
RUN python3 -m pip install PyAudio
RUN python3 -m pip install openai==0.27.8

# Installs for nav2
RUN apt-get update
RUN apt-get install -qq -y --no-install-recommends ros-humble-joy*
RUN apt-get install -qq -y --no-install-recommends ros-humble-teleop-twist-joy
RUN apt-get install -qq -y --no-install-recommends ros-humble-dwb*
RUN apt-get install -qq -y --no-install-recommends ros-humble-nav2*
RUN apt-get install -qq -y --no-install-recommends --upgrade ros-humble-*ehaviortre*
# ros-humble-behaviortree-cpp-dbgsym/jammy,now 4.5.1-2jammy.20240219.085211 arm64 [installed]
# ros-humble-behaviortree-cpp-v3-dbgsym/jammy,now 3.8.6-1jammy.20240219.085242 arm64 [installed]
# ros-humble-behaviortree-cpp-v3/jammy,now 3.8.6-1jammy.20240219.085242 arm64 [installed]
# ros-humble-behaviortree-cpp/jammy,now 4.5.1-2jammy.20240219.085211 arm64 [installed]

# Installs for vrviz
RUN apt-get update
RUN apt-get install -qq -y --no-install-recommends mosquitto

# PIP installs for custom_package: my_limo mqtt publishing
RUN python3 -m pip install msgpack
RUN python3 -m pip install paho-mqtt

# Setup working shell
RUN sed -i 's/\#force_color_prompt=yes/force_color_prompt=yes/g' /home/ros/.bashrc
RUN echo "source /workspaces/limo_ros2/src/custom_packages/my_limo/bash/local_bashrc.sh" >> /home/ros/.bashrc
RUN echo "" >> /home/ros/.bashrc

# Initial login required functionality
#RUN sudo apt update
#RUN . /workspaces/limo_ros2/build.sh