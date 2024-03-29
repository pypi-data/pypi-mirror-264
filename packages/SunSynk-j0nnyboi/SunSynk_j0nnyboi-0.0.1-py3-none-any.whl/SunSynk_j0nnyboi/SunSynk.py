
import sys
import requests
import json
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

class SunSynk(object):
    def __init__(self, username,password):

        self.user_email=username
        self.user_password=password

        OK = self.login()
        if(OK == True):
            self.Plants()#used to get details on login
            self.Plant_Details()
            self.inverters()

    def Send_Request(self,URL,PAYLOAD):
        if (self.Token_expires <= datetime.now()):#check to make sure access token hasnt run out
            self.login()#if it has login before sending comand

        if(PAYLOAD == None):
            raw_data = requests.get(URL, headers=self.headers_and_token).json()
        else:
            raw_data = requests.get(URL, params=PAYLOAD, headers=self.headers_and_token).json()
        return raw_data

    def login(self):

        headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
            }

        payload = {
            "username": self.user_email,
            "password": self.user_password,
            "grant_type":"password",
            "client_id":"csp-web"
            }
        raw_data = requests.post('https://api.sunsynk.net/oauth/token', json=payload, headers=headers).json()

        # Your access token extracted from response
        if(raw_data['success'] == False):#check to make sure respones is succcesful
            print(raw_data)
            return False
        self.bearer_token = ('Bearer '+ raw_data["data"]["access_token"])
        print("Your Token = %s" % self.bearer_token)
        self.Token_expires = datetime.now() + timedelta(seconds=int(raw_data["data"]['expires_in']))
        print("Token expires in : %s" % self.Token_expires)
        self.Refresh_Token = raw_data["data"]['refresh_token']
        print("Token refresh : %s" % self.Refresh_Token)

        self.headers_and_token = {
            'Content-type':'application/json', 
            'Accept':'application/json',
            'Authorization': self.bearer_token
            }
        return True
        

    def Plants(self):
        self.headers_and_token = {
            'Content-type':'application/json', 
            'Accept':'application/json',
            'Authorization': self.bearer_token
            }
        payload={"page": 1,
                    "limit":1
                }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plants", payload)
        #print(data_response)
        self.plant_id = data_response['data']['infos'][0]['id']
        print('Your plant id: %s' % self.plant_id)
        

        

    def Plant_Details(self):
        payload={"lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/%s"%self.plant_id, payload)
        #print(data_response)
        self.userID = (data_response['data']['master']['id'])
        print("userID = %s" %self.userID)
        return data_response
        
    def Plant_realtime(self):
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/%s/realtime"%self.plant_id,None)
        print(data_response)
        return data_response

    def Plant_flow(self):
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/energy/%s/flow"%self.plant_id,None)
        print(data_response)
        return data_response

    def Plant_inverter(self):
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/%s/inverters"%self.plant_id, None)
        print(data_response)
        return data_response

    def Plant_status(self):
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/user/%s/plantCount"%self.userID,None)
        print(data_response)
        return data_response
    
    def Day_Chart(self,date):
        payload={"date":str(date),#date in yyyy-MM-dd formate
            "lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/energy/%s/day"%self.plant_id,payload)
        print(data_response)
        return data_response

    def Month_Chart(self,date):
        payload={"date":str(date),#date in yyyy-MM formate
            "lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/energy/%s/month"%self.plant_id,payload)
        print(data_response)
        return data_response

    def Year_Chart(self,date):
        payload={"date":str(date),#date in yyyy formate
            "lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/energy/%s/year"%self.plant_id,payload)
        print(data_response)
        return data_response

    def Total_Chart(self):
        payload={"lan": "en"
            }
        rata_response = self.Send_Request("https://api.sunsynk.net/api/v1/plant/energy/%s/total"%self.plant_id,payload)
        print(data_response)
        return data_response
    def Status_count(self):
        payload={"type": -1
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverters/count",payload)
        print(data_response)
        return data_response

    def inverters(self):
        payload={"page": 1,
                 "limit": 20,
                 "type": -1,
                 "status":1,
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverters",payload)
        #print(data_response)
        self.inverterSerial = data_response['data']['infos'][0]['sn']
        print("My Serial number = %s"% self.inverterSerial)
        

    def inverters_realtime(self):
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/%s/realtime/output"%self.inverterSerial,None)
        print(data_response)
        return data_response

    def inverters_Day(self,date,column):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "column": column,#vac1,vac2,vac3/iac1,iac2,iac3/fac/pac/p_total
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/%s/output/day"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def inverters_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/%s/month"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def inverters_Year(self,date):
        payload={"date": str(date),#yyyyformate
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/%s/year"%self.inverterSerial,payload)
        print(data_response)
        return data_response
    
    def inverters_Total(self):
        payload={"lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/%s/total"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def grid_realtime(self):
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/grid/%s/realtime"%self.inverterSerial,None)
        print(data_response)
        return data_response

    def grid_Day(self,date):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "Column":"pac"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/grid/%s/day"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def grid_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/grid/%s/month"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def grid_Year(self,date):
        payload={"date": str(date),#yyyy formate
                 "lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/grid/%s/year"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def grid_Total(self):
        payload={
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/grid/%s/total"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def battery_realtime(self):
        payload={"lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/battery/%s/realtime"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def battery_Day(self,date):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "Column":"pac"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/battery/%s/day"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def battery_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/battery/%s/month"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def battery_Year(self,date):
        payload={"date": str(date),#yyyy formate
                 "lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/battery/%s/year"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def battery_Total(self):
        payload={
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/battery/%s/total"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def load_realtime(self):
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/load/%s/realtime"%self.inverterSerial,None)
        print(data_response)
        return data_response

    def load_Day(self,date):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "Column":"pac"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/load/%s/day"%self.inverterSerial,payload)
        print(data_response)
        return data_response

    def load_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/load/%s/month"%self.inverterSerial,payload)
        print(data_response)
        return data_response
    def load_Year(self,date):
        payload={"date": str(date),#yyyy formate
                 "lan": "en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/load/%s/year"%self.inverterSerial,payload)
        print(data_response)
        return data_response
    
    def load_Total(self):
        payload={
                 "lan": "en",
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/inverter/load/%s/total"%self.inverterSerial,payload)
        print(data_response)
        return data_response

        
    def event(self,types):
        payload={"sdate": str(Sdate),#yyyy-mm-dd formate
                 "edate": str(Edate),#yyyy-mm-dd formate
                 "type": types, #1info,2warning,3fault
                 "page":1,
                 "limit":20,
                 "lan":"en"
            }
        data_response = self.Send_Request("https://api.sunsynk.net/api/v1/event",payload,None)
        print(data_response)
        return data_response

