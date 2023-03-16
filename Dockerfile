FROM python:slim-bullseye

WORKDIR /app

# install external python modules 
# use [pip freeze > requirements.txt] to get all external modules into a single file
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copies every python file from the project folder into the container project folder
COPY *.py .

CMD [ "python", "proccess_csv.py" ]
