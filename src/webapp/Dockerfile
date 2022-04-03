FROM python:3.8-slim

WORKDIR /usr/src/app

# Copy python dependancy list
ADD ./requirements.txt /usr/src/app/

# Install dependancies
RUN pip install -r requirements.txt

# Copy all source files
COPY *.py ./

# Copy html templates
COPY templates ./templates

# Setup DB
# mysql-server + DB schema + setup script for user?

# Run app
CMD ["python","./app_base.py"]
