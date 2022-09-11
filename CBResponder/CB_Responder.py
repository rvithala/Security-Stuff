#!/usr/bin/python
import requests
from cortexutils.responder import Responder
from cbc_sdk.platform import Device
from cbc_sdk import CBCloudAPI

class CBResponder(Responder):
    def __init__(self):
        
        Responder.__init__(self)
        self.cburi = self.get_param('config.cb_uri', None , " Uri is missing")
        self.api_ID = self.get_param('config.api_id', None , "API Key is missing")
        self.org_key = self.get_param('config.org_key' , None , "Org Key is missing")
        self.cb_key= self.get_param('config.cb_key',None,"Secret Key is missing")
#        hostname = self.get_param('data.data', None, 'No Hostname Provided') 
#        datatype = self.get_param('data.dataType',None,'No Datatype Provided')

    def run(self):
         Responder.run(self)
         datatype = self.get_param('data.dataType',None,'No Datatype Provided')
         hostname = self.get_param('data.data', None, 'No Hostname Provided')
         if(self.cburi and self.cb_key):
            token = self.cb_key + '/' + self.api_ID
            cb = CBCloudAPI(url=self.cburi, token=token, org_key=self.org_key)
         if(datatype == 'hostname'):
            comp_devices = cb.select(Device).where('name:'+hostname).quarantine(True)
         if not datatype == 'hostname':
            self.error("Wrong Datatype")  

    def operations(self,raw):
        return [
            self.build_operation(
                "AddTagtoArtifact", tag="Device Quarantined"
            )
        ]
if __name__ == "__main__":
    CBResponder().run()
        
       
