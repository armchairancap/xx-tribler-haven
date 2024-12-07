# libtorrent-1.2.19 does not support python 3.11 yet
FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libsodium23=1.0.18-1 patch tzdata \
    && rm -rf /var/lib/apt/lists/*

# AA: Set the timezone to London
ENV TZ="Europe/London" \
    DEBIAN_FRONTEND=noninteractive

# Install Xvfb for headless GUI
RUN apt-get update -y \
  && apt-get -y install \
    xvfb nodejs npm git \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Set up a user in the container
RUN useradd -ms /bin/bash --home-dir /home/user user
USER user

# Clone the repository with arguments
WORKDIR /home/user/tribler
ARG GIT_REPO=${GIT_REPO:-"https://github.com/tribler/tribler.git"}
ARG GIT_BRANCH=${GIT_BRANCH:-"main"}
RUN echo "Cloning $GIT_REPO on branch $GIT_BRANCH"
# RUN git remote add origin "$GIT_REPO"
RUN git clone --recursive --branch "$GIT_BRANCH" "$GIT_REPO" /home/user/tribler

# AA - v8.0.6 + small files: https://github.com/Tribler/tribler/commit/0a2742cf66070e3f206edddd6657d87e234092ef 
ARG GIT_COMMIT_SHA="0a2742cf66070e3f206edddd6657d87e234092ef"

# AA: patch Tribler to allow access from localhost (127.0.0.1) and Haven
ADD tribler.patch tribler.patch
RUN git reset --hard ${GIT_COMMIT_SHA} && cd /home/user/tribler/src/tribler/core/restapi/ && patch --backup-if-mismatch /home/user/tribler/src/tribler/core/restapi/rest_manager.py /home/user/tribler/tribler.patch

# Install NPM dependencies
WORKDIR /home/user/tribler/src/tribler/ui
RUN npm install \
    && npm run build

# Install Python dependencies
WORKDIR /home/user/tribler
RUN pip3 install -r requirements.txt

# Set IPv8 on pythonpath
ENV PYTHONPATH=pyipv8

# Run the application using Xvfb
# AA: containerized xvfb sometimes fails
# CMD xvfb-run python3 src/run_tribler.py
CMD xvfb-run --auto-servernum --server-num=1 python3 src/run_tribler.py
