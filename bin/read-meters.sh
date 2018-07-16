# read meters

nohup docker-compose -f docker/docker-compose.yml \
  run amr-console \
  python3 amrdb/reader.py read >> reader.log 2>&1 &