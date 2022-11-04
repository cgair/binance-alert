#!/bin/bash

# exit when the command exits with a non-zero status
set -e

name="/home/uni01/workplace/binance-alert/start.py"

echo "Starting..."
while [ 1 ]
do 
    export http_proxy=http://127.0.0.1:1081/
    source /home/uni01/workplace/binance-alert/venv/bin/activate
    nohup python3 /home/uni01/workplace/binance-alert/start.py > /home/uni01/workplace/binance-alert/binance.log 2>&1 &
    sleep 5
    # get process's pid

    # two common ways to assign the execution result of a command to a variable:
    # 1. variable=`command`
    # 2. variable=$(command)
    task_pid=$(ps -ef | grep "$name" | grep -v grep | awk '{print $2}')
    found=$(ps -ef | grep " $task_pid " | grep -v grep | awk '{print $2}')
    echo 
    # task_pid=$!
    while [ $found -gt 0 ]
    do
        echo "PID: $task_pid is still running."
        sleep 30
    done

    echo "PID: $task_pid is done."
    sleep 60
    echo "Restarting..."
done