#!/bin/bash

fail_count=0
while true
do
    python3 fetch.sh
    r_code=$?
    if [ ${r_code} = 1 ];then
        fail_count=$((${fail_count}+1))
        continue
        if [[ ${fail_count} > 3 ]];then
            echo -e "-> Fetch failed."
            exit 1
        fi
    elif [ ${r_code} = 0 ];then
        sleep 3600
    else
        exit 1
    fi
done


