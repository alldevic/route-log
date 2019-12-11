from fastapi import FastAPI
from requests import Session
from zeep.cache import InMemoryCache
from requests.auth import HTTPBasicAuth
import zeep
from zeep.transports import Transport
import os

env = os.environ
cache = InMemoryCache()
session = Session()
session.auth = HTTPBasicAuth(env['SOAP_USER'], env['SOAP_PASS'])

transport = Transport(session=session,
                      cache=cache)

client = zeep.Client(wsdl=env['SOAP_WSDL'],
                     transport=transport)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world!"}


@app.get("/getAllDevices")
def get_all_devices():
    return client.service.getAllDevices()


@app.get("/getAllDeviceGroups")
def get_all_device_groups():
    return client.service.GetAllDeviceGroups()


@app.get("/getAllDrivers")
def get_all_drivers():
    return client.service.getAllDrivers()


@app.get("/getAllGeoZones")
def get_all_geo_zones():
    return client.service.getAllGeoZones()

# getAllRoutes(dt from, dt to)
# @app.get("/getAllDevices")
# def read_item():
#     return json.dumps(client.service.getAllDevices())


@app.get("/getChannelDescriptors/{device_id}")
def get_channel_descriptors(device_id: int):
    return client.service.getChannelDescriptors(device_id)


@app.get("/getFlatTableSimple/{device_id},{year},{month},{day}")
def get_flat_table_simple(device_id: int, year: int, month: int, day: int):
    day0 = day-1
    if day < 10:
        day = f"0{day}"
        day0 = f"0{day0}"
    date_from = f"{year}-{month}-{day0}T16:00:00"
    date_to = f"{year}-{month}-{day}T16:59:59"
    return client.service.getFlatTableSimple(device_id, date_from, date_to,
                                             10000, [0, ], ['Rw', ])
