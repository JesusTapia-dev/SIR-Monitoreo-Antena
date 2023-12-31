FROM python:3.9.16-slim-bullseye

# set working directory
RUN mkdir /radarsys
WORKDIR /radarsys

# Install python dependences
ADD requirements.txt ./requirements.txt
RUN apt-get clean && apt-get update && apt-get install -y --no-install-recommends \
	gcc \
    g++ \
    && pip install -v --timeout 120 -r requirements.txt --no-cache-dir \
    && apt-get purge -y --auto-remove gcc g++\
	&& rm -rf /var/lib/apt/lists/*

# Copy the main application.
COPY . ./

# Copy the entrypoint to collectstatic and load data automatically
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

EXPOSE 8000

