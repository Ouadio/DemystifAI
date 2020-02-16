# Choosing the base image
FROM ubuntu:latest

# Installing pip3
RUN apt-get update
RUN apt-get install python3-pip --assume-yes

# Creating the working directory inside the docker container
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Installing requirements
# Note that only the requirements file is copied first, in order to
# take advantage of docker layers, and not having to re-install requirements
# everytime the image is re-built, until the requirements change.
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Downloading the model file
RUN apt-get install wget --assume-yes
RUN wget https://uc33b5461dce5afe9ab7a0d8a1bb.dl.dropboxusercontent.com/cd/0/get/AyMfeHtukaPlndU8KdzcFN2E9pswwvnFW8NtkR7tPIeWnfJgwVr-7lGx3uAzEujAE2EWLM2ihkhUg9xzMxb183_EaR-7XNwZluytr08QE_9PcbrYAI0HPlBK-eZ4pvZ0lWo/file -O VGG_FNN_Tuned_Weights.h5


# Copying the rest of the project
COPY . ./
RUN mv VGG_FNN_Tuned_Weights.h5 flowers_recogn/ML_Models/

# Running Flask database migrations
ENV FLASK_APP=app.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN flask db init
RUN flask db migrate -m "migration done"
RUN flask db upgrade

# Running the project
EXPOSE 5000
ENTRYPOINT python3 ./app.py

