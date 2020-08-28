declare -A memory_zones_of_all_slaves=$(curl http://127.0.0.1:8000/slaves_app/MemoryZone/)

for memory_zone in memory_zones_of_all_slaves
do
    echo $memory_zone
done