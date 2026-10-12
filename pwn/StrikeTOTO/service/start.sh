#!/bin/bash

exec socat \
    TCP-LISTEN:6767,reuseaddr,fork \
    EXEC:"./luckyDraw3",pty,stderr
