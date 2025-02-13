FROM python:3.13.1

RUN pip install --root-user-action=ignore --upgrade pip 

WORKDIR /app

COPY . /app
 
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

EXPOSE 3002

CMD [ "python" , "main.py" ]
