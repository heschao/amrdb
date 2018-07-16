# AMRDB -- Read Utility Meters Over The Air
Chao Chen  
July 15, 2018

## Description
Use rtlamr project and rtl-sdr radio to read utility meters over 900MHz band. 
Save results to a database table for further analysis.

## Usage
Clone the repository:
```
clone https://github.com/heschao/amrdb
```
Set the database credentials as an environment variable:
```
export AMR_CONNECTION_STRING=postgresql+psycopg2://username:password@dbhost:dbport/dbinstance
``` 
Set the host and port of rtl_tcp process:
```
export RTL_TCP_HOST_PORT=host:port
```
Make sure you have docker and docker-compose installed. Run the init.sh script
```
cd amrdb
./init.sh
```
This will 
* create a docker image with go and python
* start a docker container and map the amrdb folder
* run amrdb/reader.py which will record the packets it captures over the air

Then the thing should be running. You can check on the progress by querying the database:
```docker-compose run amr-console python amrdb/reader.py status```
And it should tell you how many messages it has received. 
