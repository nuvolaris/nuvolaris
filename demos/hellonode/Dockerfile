FROM alpine
RUN apk add nodejs npm
RUN adduser -D nuv
WORKDIR /home/nuv
USER nuv
ADD app.js package.json /home/nuv/
RUN npm install
EXPOSE 8080
CMD node app.js