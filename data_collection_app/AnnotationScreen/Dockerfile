# pull official base image
FROM node:latest as build

# set work directory
WORKDIR /usr/local/annotation_screen/

COPY ./ /usr/local/annotation_screen/

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Install all the dependencies
RUN npm install

# Generate the build of the application
RUN npm run build

# Stage 2: Serve app with nginx server
FROM nginx:latest


## Copy our default nginx config which will replace the existing default.conf
COPY nginx/default.conf /etc/nginx/conf.d/

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

## From ‘builder’ stage copy over the artifacts in dist folder to default nginx public folder
COPY --from=build /usr/local/annotation_screen/dist/example-app/ /usr/share/nginx/html

EXPOSE 80
