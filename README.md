# basic-python-qlik-sse
This repository provides a basic example of a server-side extension (SSE) for Qlik Sense built using Python.

# Prerequisites
Python 3.7+ installed on your server

# Required Python packages
```bash
pip install grpcio grpcio-tools
```
# Generate gRPC Protocol Files
Download the QlikSense SSE protocol files from:
https://github.com/qlik-oss/server-side-extension/tree/master

Run the following command to generate files:
```bash
python -m grpc_tools.protoc -I proto --proto_path=. --python_out=. --grpc_python_out=. ServerSideExtension.proto
```
This creates:

<img width="525" height="320" alt="gRPC Protocol Files" src="https://github.com/user-attachments/assets/3fa7a5c4-af06-4bc7-a1fb-d15e810a69da" />

# Start the SSE server
```bash
python ssePyTools.py
```
Verify port: Ensure port that you goes to use is not blocked by firewall

<img width="652" height="249" alt="Python SSE Server" src="https://github.com/user-attachments/assets/82874a34-2af2-4587-b1fd-9bbed7253fbf" />

# Qlik Sense
Set up a new analytic connection

<img width="752" height="349" alt="Qlik Sense Analytic Connection" src="https://github.com/user-attachments/assets/08e63d53-d31b-4d72-83e4-09ad25b97c1c" />

Restart Qlik Sense Engine Service

<img width="500" height="149" alt="Qlik Sense Services" src="https://github.com/user-attachments/assets/2066cab6-3242-49c9-a9a2-5d8ee8b079a7" />

In your app verify your regional configurations, for example money o number formats:

```Qlik Script
SET DecimalSep='.';
SET ThousandSep=',';
```

In this basic example we can calculate bmi using the function ssePyTools.calcBMI

```Qlik Script
TempTable:
LOAD * INLINE [
Name, Weight, Height
John Doe, 75, 1.75
Lali Castillo, 59.2, 1.55
Wilson Chavez, 85, 1.80
Jane Doe, 60, 1.60
];

FinalTable:
LOAD
Name,
Weight,
Height,
ssePyTools.calcBmi(Weight, Height) as BMI
RESIDENT TempTable;

DROP TABLE TempTable;
```

If the function is configured correctly it should be highlighted and Qlik Sense will display help to indicate the input values that the function receives.

<img width="450" height="600" alt="Load script example" src="https://github.com/user-attachments/assets/b38345d4-8047-4edf-85fe-2854d972b1ed" />

Finally, perform a Load to see the results of the operation

<img width="650" height="700" alt="Result of the function" src="https://github.com/user-attachments/assets/f9b6da0d-f479-4588-ba5c-ede98ed4cc42" />
