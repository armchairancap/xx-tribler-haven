# AA: Use Ubuntu 24.04 instead of the official Dockerfile's 20.04
FROM ubuntu:24.04

ARG SPEAKEASY_VER="main"
ENV SPEAKEASY_VER=$SPEAKEASY_VER

# AA: Set the timezone to London
ENV TZ="Europe/London" \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git patch tzdata && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs && apt-get clean
ARG GIT_REPO=${GIT_REPO:-"https://git.xx.network/elixxir/speakeasy-web.git"}
ARG GIT_COMMIT_SHA="5afa715e257cf78a42173f5cf5785e339095a46b"

# AA: Patch the DefaultLayout.tsx file and modify .env for invites to go to localhost:3000
RUN mkdir /speakeasy-web && git clone -b $SPEAKEASY_VER ${GIT_REPO} /speakeasy-web
WORKDIR /speakeasy-web
RUN git reset --hard ${GIT_COMMIT_SHA} && sed -i 's/haven.xx.network/haven:3000/g' .env
ADD patched-DefaultLayout.tsx ./src/layouts/DefaultLayout/DefaultLayout.tsx
RUN npm install && npm run build

ENTRYPOINT [ "npm", "run", "start" ]
