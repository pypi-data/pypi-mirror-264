import SunSynk

Sun = SunSynk.SunSynk("email","password")#Login and get plant details

print("################################################")

Sun.Plant_realtime()#show plant realtime data

Sun.Plant_flow()#show plant flow data

Sun.inverters_realtime()#show inverter data

realBat = Sun.battery_realtime()#show battery realtime data
print(realBat['data']['voltage'])#print voltage from battery real time data
