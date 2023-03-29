#include <A7585lib.h>
#include <Wire.h>
#include <stdio.h>
#include <stdlib.h>

#define DEV_ADDRESS 0x70

A7585 A7585_dev;

// Initialize device
void  InitNIPM(int  device_address)
{
	A7585_dev.Init(device_address);
	A7585_dev.Set_Mode(0);				//SET MODE DIGITAL
	A7585_dev.Set_MaxV(80);				//SET COMPLIANCE 80V
	A7585_dev.Set_MaxI(10);				//SET MAXIMUM CURRENT 10mA
	A7585_dev.Set_RampVs(25);			//SET RAMP UP SPEED 25V/s
}

void setup()  {
	Serial.begin(115200);
	Wire.begin();
	InitNIPM(DEV_ADDRESS);
	
	if  (A7585_dev.GetConnectionStatus())
		Serial.println("Probe connection successful");
	else
		Serial.println("Error  connecting device ");
	
	A7585_dev.Set_V(50);				//SET VOUT=50V		
	A7585_dev.Set_Enable(true);			//ENABLE HV
}

void loop()  {
	cvout  = A7585_dev.GetVout();		//READ VOLTAGE
	ciout  = A7585_dev.GetIout();		//READ CURRENT
	Serial.print(" V: ");  Serial.print(cvout);  Serial.print(" I: ");  Serial.println(ciout);
	delay(1000);
}