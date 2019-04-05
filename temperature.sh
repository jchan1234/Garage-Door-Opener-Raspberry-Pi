#!/bin/bash
cpu=$(</sys/class/thermal/thermal_zone0/temp)
echo "$((cpu/1000))c"
