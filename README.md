# basic-python-qlik-sse
This repository provides a basic example of a server-side extension (SSE) for Qlik Sense built using Python.

# Prerequisites
Python 3.7+ installed on your server

# Required Python packages
pip install grpcio grpcio-tools

# Generate gRPC Protocol Files
Download the QlikSense SSE protocol files from:
https://github.com/qlik-oss/server-side-extension/tree/master

Run the following command to generate files
python -m grpc_tools.protoc -I proto --proto_path=. --python_out=. --grpc_python_out=. ServerSideExtension.proto

This creates:
ServerSideExtension_pb2.py
ServerSideExtension_pb2_grpc.py

# Start the SSE server
python ssePyTools.py

Verify port: Ensure port that you goes to use is not blocked by firewall

# Qlik Sense
Set up a new analytics connection
Restart Qlik Sense Engine Service

In your app verify your Regional configurations, for example money formats:
SET DecimalSep='.';
SET ThousandSep=',';