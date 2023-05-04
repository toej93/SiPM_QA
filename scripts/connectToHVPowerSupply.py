#!/usr/bin/python

import serial, time, os
import numpy as np
import pandas as pd
#initialization and open the port
bias_arr = []
I_arr = []
#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"

ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

try: 
	ser.open()
	time.sleep(1)

except Exception:
	print("error open serial port")
	exit()

if(ser.isOpen()):
	print("Connected\n")
	cmd="AT+MACHINE\n\r"
	ser.write(cmd.encode())

	cmd="AT+SET,2,25.00\n\r"
	ser.write(cmd.encode())
	cmd="AT+SET,0,1\n\r"
	ser.write(cmd.encode())
	cmd="AT+GET,2\n\r"
	ser.write(cmd.encode())
	msg=ser.read(64)
	print(msg)
	time.sleep(3)
	for Vbias in np.arange(52,55.5,0.05):
		cmd="AT+SET,2,%f\n\r"%Vbias
		ser.write(cmd.encode())
		time.sleep(3)

		cmd="AT+GET,231\n\r"
		ser.write(cmd.encode())
		msg=ser.read(64)
		bias = (msg.decode()).replace('OK=', '')
		# print(bias)
		print("Bias is:%s"%(bias))
		bias = bias.rstrip()
		bias_arr.append(Vbias)
		I_arr_temp = []
		for i in range(0,5):
			cmd="AT+GET,232\n\r"
			ser.write(cmd.encode())
			msg=ser.read(64)
			curr = (msg.decode()).replace('OK=', '')
			# time.sleep(0.01)
			curr = curr.rstrip()
			I_arr_temp.append(float(curr))
		I_arr.append(np.mean(I_arr_temp))
	cmd="AT+SET,0,0\n\r"
	ser.write(cmd.encode())
print(bias_arr, I_arr)
ser.close()

list_of_tuples = list(zip(bias_arr, I_arr))
df = pd.DataFrame(list_of_tuples,
                  columns=['bias', 'current'])
  
# Print data.
print(df)
df.to_pickle("./IV.pkl")