#!/bin/bash

exec socat TCP-LISTEN:31337,reuseaddr,fork EXEC:"python3 lockdown.py"
