# AA: Use Ubuntu 24.04 instead of the official Dockerfile's 20.04
FROM ubuntu:24.04

ARG SPEAKEASY_VER="main"
ENV SPEAKEASY_VER=$SPEAKEASY_VER

# AA: Set the timezone to London
ENV TZ="Europe/London" \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git patch tzdata

# AA: Install Node.js 18.x instead of the official Dockerfile's 16.x
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs

ARG GIT_REPO=${GIT_REPO:-"https://git.xx.network/elixxir/speakeasy-web.git"}
ARG GIT_COMMIT_SHA="5afa715e257cf78a42173f5cf5785e339095a46b"

# RUN mkdir /speakeasy-web && git clone --depth=1 -b $SPEAKEASY_VER https://git.xx.network/elixxir/speakeasy-web.git /speakeasy-web && cd /speakeasy-web && npm install && npm run build
# AA: Modify the above "official" line to allow for patching the DefaultLayout.tsx file
RUN mkdir /speakeasy-web && git clone --depth=1 -b $SPEAKEASY_VER ${GIT_REPO} /speakeasy-web
ADD haven-DefaultLayout.tsx.patch /speakeasy-web/haven-DefaultLayout.tsx.patch
WORKDIR /speakeasy-web
RUN git reset --hard ${GIT_COMMIT_SHA} && patch -p1 --backup-if-mismatch src/layouts/DefaultLayout/DefaultLayout.tsx haven-DefaultLayout.tsx.patch && npm install && npm run build

ENTRYPOINT [ "npm", "run", "start" ]
