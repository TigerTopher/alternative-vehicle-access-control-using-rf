from RF_protocol import *

class VH_RF(RF_protocol):
    def __init__(self):
        RF_protocol.__init__(self, "vh")
        self.vh_info = self.database.select_query("*", "vh_info", "")[0]
        self.source = self.vh_info[0]
