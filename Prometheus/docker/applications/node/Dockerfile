FROM node:alpine

WORKDIR /app

COPY . /app

RUN npm install -g npm@11.1.0

RUN npm install

EXPOSE 3001

CMD [ "node", "index.js" ]

