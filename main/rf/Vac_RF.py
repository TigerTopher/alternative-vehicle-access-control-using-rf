from RF_protocol import *

class Vac_RF(RF_protocol):
    def __init__(self):
        RF_protocol.__init__(self, "vac")
        self.vac_info = self.database.select_query("*", "vac_info", "")[0]
        self.source = self.vac_info[0]
        self.ca_public_key = self.vac_info[1]
