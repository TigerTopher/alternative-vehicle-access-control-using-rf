from RF_protocol import *

class Vac_RF(RF_protocol):
    def __init__(self):
        RF_protocol.__init__(self, "vac")
        self.vac_info = self.database.select_query("*", "vac_info", "")[0]
        self.source = self.vac_info[0]
        self.ca_public_key = self.vac_info[1]
        self.vehicles_registered = self.database.select_query("vin", "vehicles_registered", "")
        self.vehicle_public_keys = self.database.select_query("public_key", "vehicles_registered", "")

v = Vac_RF()
packet = v.send(-1, 24)
#data = v.get_data_from_packet(packet)
#print data
v.end_session()
