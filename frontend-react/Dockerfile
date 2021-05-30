FROM node:14

WORKDIR /app/

COPY package.json yarn.lock /app/

RUN yarn && \
  yarn global add serve

COPY public /app/public/
COPY src /app/src/

RUN yarn build

EXPOSE 3000

CMD [ "serve", "--listen", "tcp://0.0.0.0:3000", "--single", "build", "--no-clipboard" ]
