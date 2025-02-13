FROM python:3.9

RUN apt update && apt install -y postgresql-client

RUN pip install --root-user-action=ignore --upgrade pip 

WORKDIR /app

COPY . /app
 
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

EXPOSE 3003

CMD [ "python" , "main.py" ]
