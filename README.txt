
STEP1
#download requirements for project
pip3 -r ./requirements.txt


STEP 2
##build proto files if needed
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./cluster/proto/cluster.proto
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./file_service/proto/fileservice.proto

STEP 3
#begin main cluster server
python3 ./cluster/cluster_server.py


STEP 4
#begin file server(nodes)
python file_service/file_server.py "50051" "localhost" "50053"


STEP 5
#run file client to test upload and download
python3 ./file_service/file_client.py

# To do file upload download and other operations please go to the ""./file_service/file_client.py" and uncomment the lines below