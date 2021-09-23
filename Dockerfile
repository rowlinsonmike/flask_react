FROM nikolaik/python-nodejs:latest
WORKDIR /usr/src/app
COPY . .
RUN npm run setup && \
    npm run bootstrap && \  
    npm run build
EXPOSE 8000
CMD ["/bin/bash", "-c", "npm run deploy"]