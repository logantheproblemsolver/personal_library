FROM python:3.9

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 5001


RUN python -m build --wheel
RUN ls
CMD [ "waitress-serve", "--call" , "--listen=0.0.0.0:5001", "personal_library:create_app" ]

# 
# python -m build --wheel