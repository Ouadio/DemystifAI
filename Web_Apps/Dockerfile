# Choosing the base image
FROM tiangolo/uwsgi-nginx-flask:python3.6

# Creating the working directory inside the docker container
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Installing requirements
# Note that only the requirements file is copied first, in order to
# take advantage of docker layers, and not having to re-install requirements
# everytime the image is re-built, until the requirements change.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copying the rest of the project
COPY . ./

# Running Flask database migrations
ENV FLASK_APP=app.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN flask db init
RUN flask db migrate -m "migration done"
#RUN flask db upgrade

# Running the project
EXPOSE 8080
ENTRYPOINT python3 ./app.py

