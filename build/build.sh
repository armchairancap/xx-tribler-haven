#!/usr/bin/env bash

if [ ! -d "haven" ] || [ ! -d "tribler" ]; then
    echo "haven or tribler directory not found. Are you in the right directory (build)?"
    exit 1
fi

cd haven
echo -e "\n=== Building Haven ===\n"
echo -e "\nThis may take several minutes!\n"
docker build -t haven-for-tribler:latest .

cd ../tribler
echo -e "\n=== Building Tribler ===\n"
docker build -t tribler-haven:latest .
cd ../

echo -e "\n=== Done! List tribler-related images ===\n"
docker images | grep tribler


echo -e '''\n
Edit tribler/compose.yaml and in that directory create "tribler-downloads" subdirectory for Tribler downloads:

cd tribler 
vim compose.yaml
mkdir tribler-downloads
docker compose up

After the container is up, you can access Haven at http://localhost:3000 
and see a Tribler iFrame on the same page.

If you change CORE_API_KEY, you need to set the same password in the Haven patch, 
and rebuild & restart Haven container.
'''
