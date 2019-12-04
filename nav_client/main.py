from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport

import os

env = os.environ

session = Session()
session.auth = HTTPBasicAuth(env['SOAP_USER'], env['SOAP_PASS'])

client = Client(wsdl=env['SOAP_WSDL'],
                transport=Transport(session=session))

print(client.service.getAllDevices())
