#!/usr/bin/env bash

# Build Haven and Tribler Docker images
# 
# Usage: ./build.sh
#
# License: MIT 
# (c) 2025, https://armchairancap.github.io 
# 

if [ ! -d "haven" ] || [ ! -d "tribler" ]; then
    echo "haven or tribler directory not found. Are you in the right directory? (./build)?"
    exit 1
fi

docker build -t haven-for-tribler:latest haven
docker build -t tribler-haven:latest tribler

echo -e ""
echo -e "If build completed w/o errors, create "tribler-downloads" subdirectory for Tribler downloads in this subdirectory:\n"
echo -e "mkdir tribler-downloads\n"
echo -e ""
echo -e "Run Docker Compose to start Haven and Tribler containers:\n"
echo -e "docker compose up\n"
echo -e ""
echo -e "After the containers are up, you can access Haven at http://localhost:3000  and see a Tribler iFrame in the same browser tab/window.\n"
echo -e ""
echo -e "NOTE 1): You can't access Tribler directly this way. See compose.yaml and Security in README.md for more info.\n"
echo -e ""
echo -e "NOTE 2: If you change CORE_API_KEY in docker-compose.yaml, you need to set the same password in the Haven patch, and rebuild & restart Haven container.\n"
