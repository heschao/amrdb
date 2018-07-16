# AMRDB -- Read Utility Meters Over The Air
Chao Chen  
July 15, 2018

## Description
Use rtlamr project and rtl-sdr radio to read utility meters over 900MHz band. 
Save results to a database table for further analysis.

## Usage
Clone the repository:
```git clone https://github.com/heschao/amrdb```
Create a postgresql database and user:
```
psql -Upostgres -c "create database <dbinstance>"
psql -Upostgres -c "create user <dbuser> with password '<dbpass>'"
```
Set the database credentials as an environment variable:
```export AMR_CONNECTION_STRING=postgresql+psycopg2://<dbuser>:<dbpass>@<dbhost>:<dbport>/<dbinstance>``` 
Set the host and port of rtl_tcp process:
```export RTL_TCP_HOST_PORT=host:port```
Make sure you have docker and docker-compose installed. Run the init.sh script
```
cd amrdb
bin/init.sh
```
This will 
* create a docker image with go and python
* start a docker container and map the amrdb folder
Then run:
```
bin/read-meters.sh
```
This will run amrdb/reader.py which will record the packets it captures over the air. You can check \
on the progress by querying the database:
```
docker-compose -f docker/docker-compose.yml run amr-console python amrdb/reader.py status
```
And it should tell you how many messages it has received like this:
```
52 message recorded
19 distinct device ids
timetamps 2018-07-16 02:30:22.913219 --> 2018-07-16 02:51:49.592933
```
