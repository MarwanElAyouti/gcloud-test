FROM node:17-alpine

WORKDIR /code/

COPY package.json /code/

RUN npm install -g vite

RUN npm install

COPY . /code

EXPOSE 4173

CMD ["npm", "start"]
