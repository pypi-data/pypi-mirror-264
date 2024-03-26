# PyIPe

PyIPe is a Python library for retrieving location information and implementing anti-VPN measures.

## Installation

Install PyIPe via pip:

```bash
pip install PyIPe




How to Use

Get Your IP Address

from PyIPe import PyAD

ad = PyAD()
my_ip = ad.ip()
print(my_ip)



Get IP Latitude and Longitude

from PyIPe import PyLO

lo = PyLO()
ip_address = "IP ADDRESS HERE"
lat, lon = lo.get_location(ip_address)
print(lat, lon)


Get IP Country and Capital


from PyIPe import PyCU

cu = PyCU()
country, region = cu.get_country(ip_address)
print(f"Country: {country}, Region: {region}")


Implement Anti-VPN


from PyIPe import PyLT

lt = PyLT()

while True:
    try:
        if lt.check_ip():
            pass
        else:
            print("IP address has changed.")
            break
    except Exception:
        continue



Note
Replace "IP ADDRESS HERE" with the actual IP address you want to query.

This README provides a brief overview of PyIPe functionalities. For more detailed documentation and examples, please visit the documentation page.


Replace `URL_TO_DOCUMENTATION` with the actual URL to your documentation page if you have one. This README structure should display neatly on PyPI and provide users with clear instructions on how to install and use your library.

