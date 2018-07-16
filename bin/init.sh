# pull docker image and run unittests

# create docker image
docker build . -t amr -f docker/Dockerfile

# create tables
docker-compose -f docker/docker-compose.yml \
 run amr-console python3 amrdb/reader.py create-tables

# run unittests
docker-compose -f docker/docker-compose.yml \
 run amr-console nosetests amrdb --all-modules --exe

