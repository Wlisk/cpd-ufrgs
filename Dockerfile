FROM python:3

WORKDIR /usr/src/app

# install external python modules 
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copies every python file from the project folder into the container project folder
COPY *.py .

CMD [ "python", "proccess_csv.py" ]
