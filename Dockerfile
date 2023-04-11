FROM python:slim-bullseye

WORKDIR /app

# install external python modules 
# use [pip freeze > requirements.txt] to get all external modules into a single file
COPY requirements.txt ./

RUN apt-get update && apt-get install python-dev python-tk

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyinstaller

# copies every python file from the project folder into the container project folder
#COPY *.py .
RUN ls

CMD [ "python", "main.py" ]
