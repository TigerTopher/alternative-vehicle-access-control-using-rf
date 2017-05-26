from RF_protocol import *

class VH_RF(RF_protocol):
    def __init__(self):
        RF_protocol.__init__(self, "vh")
        self.vh_info = self.database.select_query("*", "vh_info", "")[0]
        self.source = self.vh_info[0]

        l = list(self.vh_info[1])
        l.remove('[')
        l.remove(']')
        temp = ""
        self.nfc_uid = []
        for i in l:
            if i == ",":
                self.nfc_uid.append(int(temp, 10))
                temp = ""
                continue
            if i != " ":
                temp += i

        l = list(self.vh_info[2])
        l.remove('[')
        l.remove(']')
        temp = ""
        self.key = []
        for i in l:
            if i == ",":
                self.key.append(int(temp, 10))
                temp = ""
                continue
            if i != " ":
                temp += i

        self.nfc_sector = self.vh_info[3]
        self.key_A = bool(self.vh_info[4])

        self.vacs_accessible = self.database.select_query("vac_no", "vacs_accessible", "")
        self.vacs_public_key = self.database.select_query("public_key", "vacs_accessible", "")

        self.vacs_accessible = [1082267] # get from dB

v = VH_RF()
packet = v.reliable_data_transfer_receive()
data = v.get_data_from_packet(packet)
print data
v.end_session()
