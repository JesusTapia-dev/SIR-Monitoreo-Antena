FROM python:2.7-slim

# set working directory
RUN mkdir /radarsys
WORKDIR /radarsys

# Install python dependences
ADD requirements.txt ./requirements.txt
RUN apt-get clean && apt-get update && apt-get install -y --no-install-recommends \
	gcc \
    g++ \
    && pip install -v --timeout 120 -r requirements.txt --no-cache-dir --index-url http://10.10.20.128:8010/simple --trusted-host 10.10.20.128 \
    && apt-get purge -y --auto-remove gcc g++\
	&& rm -rf /var/lib/apt/lists/*

# Copy the main application.
COPY . ./

EXPOSE 8000

