FROM node:lts-slim

WORKDIR /app/

COPY package.json /app/
COPY package-lock.json /app/

RUN npm ci

COPY . /app/

RUN mkdir /app/node_modules/.cache && chmod -R 777 /app/node_modules/.cache

EXPOSE 3000

CMD npm start
