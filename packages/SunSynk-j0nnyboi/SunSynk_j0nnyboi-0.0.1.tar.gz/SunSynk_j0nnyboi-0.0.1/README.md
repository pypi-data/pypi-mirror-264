# SunSynk API 
This is a python class to make it easier to get your data off the sunsynk V2 servers throught there API

# Requirements
create your SunSynk account on https://sunsynk.net/, Please make sure sunsynk inverter has internet connectivity using the wifi enable data logger and is connected. 

# Steps
1) Confirm connectivity to inverter.

3) call the class from your python project then interacter will get the data you require.

The command example would be:
```
import SunSynk
Sun = SunSynk.SunSynk(username,password)#your username and password your created on https://sunsynk.net/ 
Sun.interters_realtime() #to get inverter data
Sun.battery_realtime() #to get battery data 
```

if you get a Certificate error please run 'pip3 install --upgrade certifi', this should fix the error

Not 100% tested yet