
#!/bin/bash

echo Enter the path
read PATH

cd "$PATH"

rm -f gwbuild-Dual WriteRawLogData

echo "==== Compiling gwbuild ===="

/home/elmpc-357/vinoth/SDK/host/usr/bin/aarch64-linux-gnu-gcc \
thread_try.c \
web_server.c \
responce_post.c \
convert.c \
Uart_data.c \
waveform.c \
mytimer.c \
TimerCallback.c \
File_decode.c \
netmask_cal.c \
mqtt_thread.c \
RTC.c \
Data.c \
mqtt_defi.c \
usb.c \
Data_recovery.c \
switch_reset.c \
-lpthread \
-ljson-c \
-lm \
-lmicrohttpd \
-lpaho-mqtt3as \
-lcurl \
-lrt \
-o gwbuild-Dual

if [ $? -eq 0 ] && [ -f "$PATH/gwbuild-Dual" ]; then
    echo "==== gwbuild Compilation Successful ===="
    echo "   "
else
    echo "==== gwbuild Compilation Failed ===="
fi

echo "==== Compiling WriteRawLogData ===="

/home/elmpc-357/vinoth/SDK/host/usr/bin/aarch64-linux-gnu-gcc \
WriteRawLogData.c \
mytimer.c \
-lpthread -lrt -lm -lcurl -ljson-c \
-o WriteRawLogData

if [ $? -eq 0 ] && [ -f "$PATH/WriteRawLogData" ]; then
    echo "==== WriteRawLogData Compilation Successful ===="
else
    echo "==== WriteRawLogData Compilation Failed ===="
fi

