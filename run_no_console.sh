#!/bin/bash
# Ejecuta CountdownPet sin terminal
nohup python3 main.py > /dev/null 2>&1 &
echo "CountdownPet ejecutándose en background (PID: $!)"
