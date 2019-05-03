# Scar Recognition

handler.py - wrapper for aws

index.py - wrapper for Zeit Now

Use either handler or index depending on where you will deploy it.

process.py - does the image processing and finds the scar. Its called in both handler.py and index.py and returns appropriate scar data

##Deployment

Follow this in depth guide for development environment and deployment https://serverless.com/blog/serverless-python-packaging/
