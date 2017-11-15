FROM python:2.7.11

# set working directory
RUN mkdir /radarsys
WORKDIR /radarsys

# Copy the main application.
COPY . ./

# Install python dependences
RUN pip install -v --timeout 120 -r requirements.txt --no-cache-dir

EXPOSE 3000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
# Para produccion:
CMD ["gunicorn", "radarsys.wsgi:application", "--bind", "0.0.0.0:3000"]

