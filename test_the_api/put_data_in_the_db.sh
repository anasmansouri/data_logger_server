

echo "create a slave id : 2 "

curl -X POST -H "Content-Type: application/json" \
 -d '{
        "slave_address":2,
        "name": "power meter",
        "enable": true,
        "mac": "74-DE-AA-38-30-12",

        "setting": {
            "baudrate": 19200,
            "parity": "E",
            "stopbits": 1,
            "bytesize": 8,
            "timeout":0.5
        }


}' \
http://127.0.0.1:8000/slaves_app/Slaves/




echo "create a memory zone with id : 1 for slave  id : 1 "

curl -X POST -H "Content-Type: application/json" \
 -d '{
            "start_registers_address": 0,
            "name":"Voltage",
            "unit":"V",
            "type_of_value":"INT32",
            "number_of_decimals":1,
            "slave":1
        }  ' \
http://127.0.0.1:8000/slaves_app/MemoryZone/



echo "create a memory zone with id : 2 for slave  id : 1 "

curl -X POST -H "Content-Type: application/json" \
 -d '{
            "start_registers_address": 2,
            "name":"Voltage",
            "unit":"V",
            "type_of_value":"INT32",
            "number_of_decimals":1,
            "slave":1
        }  ' \
http://127.0.0.1:8000/slaves_app/MemoryZone/




echo "get all slaves in data base"

curl 127.0.0.1:8000/slaves_app/Slaves/

echo "get all memory zones of the slave with id : 1"

curl http://127.0.0.1:8000/slaves_app/MemoryZone/


echo "get all memory zones of the slave with id : 2"

curl http://127.0.0.1:8000/slaves_app/MemoryZone/

declare -A memory_zones_of_all_slaves=$(curl http://127.0.0.1:8000/slaves_app/MemoryZone/)

for memory_zone in memory_zones_of_all_slaves
do
    if[$memory_zone['slave']]
done


for n in $(cat lists.txt )
do
    echo "Working on $n file name now"
    # do something on $n below, say count line numbers
    # wc -l "$n"
done

