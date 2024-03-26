import requests
import time


class PyAD:
    def ip(self):
        response_ip = requests.get('https://api.ipify.org?format=json')
        public_ip = response_ip.json()['ip']
        return public_ip
    
    

class PyLO:
    def get_location(self, ip_address):
        response_geo = requests.get(f'http://ip-api.com/json/{ip_address}')
        geo_data = response_geo.json()
        if geo_data['status'] == 'success':
            return geo_data['lat'], geo_data['lon']
        else:
            return None, None

class PyCU:
    def get_country(self , ip_address):
        response_geo = requests.get(f'http://ip-api.com/json/{ip_address}')
        geo =response_geo.json()
        if geo['status'] == 'success':
            return geo['country'], geo['regionName']
        else:
            return None ,None
        

class PyLT:
    def __init__(self):
        self.first_ip = PyAD().ip()
        self.blocked_ips = []

    def check_ip(self):
        current_ip = PyAD().ip()
        if current_ip != self.first_ip:
            self.blocked_ips.append(self.first_ip)
            self.first_ip = current_ip
            return False
        else:
            return True
   
   
 
 
# PA = PyLT()

# while True:
#     try:
#         example = PA.check_ip()
#         if example :
#             pass
#         else:
#             print("\r\033[91mUser using VPN\033[0m" , end='' ,flush=True)
#             break
#     except Exception:
#         continue 
   
######################   

# ip_address = 'عنوان الip هنا'

# latitude, longitude = ad.get_location(ip_address)
# if latitude and longitude:
#     print(f"Latitude: {latitude}, Longitude: {longitude}")
# else:
#     print("عنوان IP غير صالح أو حدث خطأ في الاستعلام.")