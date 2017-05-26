from Database import *
from Checksum import *
from random import *
from receiver import *
from transmitter import *
from time import *

class RF_protocol(object):
    def __init__(self, device_type):
        self.device_type = device_type
        self.transmitter_pin = 5
        self.receiver_pin = 4
        self.other_device_type = "vh" if self.device_type == "vac" else "vac"

        self.checksum = Checksum()
        self.database = Database(device_type, "avracardabra", "localhost", "password")
        self.destination = 0

        self.data_length = 128
        self.address_length = 24
        self.checksum_length = 16

        self.data_extractor = 2 ** self.data_length - 1
        self.address_extractor = 2 ** self.address_length - 1
        self.checksum_extractor = 2 ** self.checksum_length - 1

        self.packet_length = 192
        self.frame_length = 32
        self.frame_data_length = 24
        self.sequence_length = self.frame_length - self.frame_data_length - 1
        self.number_of_frames = self.packet_length/self.frame_data_length

        self.frame_data_extractor = (2 ** self.frame_data_length) - 1
        self.frame_sequence_extractor = ((2 ** self.sequence_length) - 1) << (self.frame_data_length + 1)
        self.frame_ack_extractor = 1 << (self.frame_data_length)

        self.first_sequence_numbers = {"vac": range(self.number_of_frames, (2 ** (self.sequence_length - 1)), self.number_of_frames), "vh":range(2 ** (self.sequence_length - 1), 2 ** self.sequence_length, self.number_of_frames)}

    def get_source(self):
        return self.source

    def get_destination(self):
        return self.destination

    def form_packet(self, data):
        destination = self.get_destination()
        source = self.get_source()
        packet = (destination << 152) + (source << 128) + data
        return self.checksum.transmitter_checksum(packet)

    def get_data_from_packet(self, packet):
        checksum = packet & self.checksum_extractor
        packet = packet >> self.checksum_length

        data = packet  & self.data_extractor
        packet = packet >> self.data_length

        source = packet & self.address_extractor
        packet = packet >> self.address_length

        destination = packet & self.address_extractor

        return [destination, source, data, checksum]

    def transmit_frame(self, sequence_no, ack, data):
        print sequence_no, ack, data
        frame = (sequence_no << (self.frame_data_length + 1)) + (ack << self.frame_data_length) + data
        transmit(self.transmitter_pin, frame)

    def get_data_from_frame(self, frame):
        sequence = (frame & self.frame_sequence_extractor) >> (self.frame_data_length + 1)

        ack = (frame & self.frame_ack_extractor) >> (self.frame_data_length)

        data = frame & self.frame_data_extractor

        return [sequence, ack, data]

    def reliable_data_transfer_transmit(self, packet):
        used = True
        self.receiver_setup()
        while used:
            sequence = sample(self.first_sequence_numbers[self.device_type], 1)[0]

            # these are all the sequence numbers that are going to be used
            # these are saved to check the acks later on
            expected_sequence_numbers = range(sequence, sequence + self.number_of_frames)
            if(available()):
                frame = getReceivedValue()
                data = self.get_data_from_frame()
                used = data[0] in expected_sequence_numbers
                resetAvailable()
            else:
                used = False

        j = 1
        data_sent = []
        for i in expected_sequence_numbers:
            # chop the data
            data = (packet >> (self.frame_data_length * (self.number_of_frames - j))) & self.frame_data_extractor
            # transmit [sequence number, ack number, data]
            self.transmit_frame(i, 0, data)
            data_sent.append(data)
            j += 1

        # check for acks
        prev_frame = -1
        # timer to send again
        start_time = time()
        while True:
            curr_time = time()
            if(available()):
                frame = getReceivedValue()

                # avoids repetition of frames
                if(frame != prev_frame):
                    prev_frame = frame
                    data = self.get_data_from_frame(frame)

                    # check for which sequence number the frame is
                    for i in range(0, len(expected_sequence_numbers)):
                        # check if it is an ack/nack
                        if data[0] == expected_sequence_numbers[i] and data[1] == 1:
                            # if nack send again
                            if data[2] == 0:
                                # since nack is received it means the ones before the sequence number is received so start from there
                                new_first_sequence_number = data[0] - expected_sequence_numbers[0]

                                print expected_sequence_numbers, data_sent

                                sleep(0.5)
                                self.transmit_frame(expected_sequence_numbers[new_first_sequence_number], 0, data_sent[new_first_sequence_number])
                            # if receive one ack, it means the receiver is transmitting the acks for everything
                            else:
                                return
                            break

                            # reset timer if received an ack/nack
                            start_time = time()
                resetAvailable()

            # if timer reaches 5 seconds (amount of time to transmit/receive), send everything again
            elif curr_time - start_time > 5:
                for i in range(new_first_sequence_number, len(expected_sequence_numbers)):
                    self.transmit_frame(expected_sequence_numbers[i], 0, data_sent[i])

                # reset timer if send again
                start_time = time()

    def send(self, destination, data):
        if destination != -1:
            self.destination = destination
        packet = self.form_packet(data)
        self.reliable_data_transfer_transmit(packet)

    def receiver_setup(self):
        if wiringPiSetup() == -1:
            print "Error"
            return 0

        enableReceivePin(self.receiver_pin)

    def reliable_data_transfer_receive(self):
        self.receiver_setup()

        prev_frame = -1
        frame_no = 0
        frame_data = [0, 0, 0, 0, 0, 0, 0, 0] # this is where the data is saved
        nacks = False # determines if we are just waiting for data that wasn't received in between
        while True:
            if(available()):
                # receiving value from transmitter
                frame = getReceivedValue()

                # makes sure frame never repeats (frames never repeat due to sequence numbers)
                if(frame != prev_frame):
                    prev_frame = frame

                    # get data from frame
                    data = self.get_data_from_frame(frame)
                    print data

                    # makes sure that it is not an ack and it is for the device_type
                    if data[0] in self.first_sequence_numbers[self.other_device_type] and data[1] == 0 and frame_no == 0:
                        # makes sure that the message destination is self or broadcast (for vh)
                        if data[2] == self.source or (self.device_type == "vh" and data[2] == 0):
                            first_sequence_number = data[0]
                            expected_sequence_numbers = range(data[0] + 1, data[0] + self.number_of_frames)
                            frame_data[0] = data[2]
                            frame_no += 1
                    elif frame_no > 0:
                        # makes sure that the data being gotten is from the same packet
                        if data[0] in expected_sequence_numbers:
                            if frame_no == 1:
                                # makes sure that vh or vac is supposed to be talked to
                                if (self.device_type == "vh" and data[2] not in self.vacs_accessible) or (self.device_type == "vac" and data[2] not in self.vehicles_registered):
                                    frame_no = 0
                                    expected_sequence_numbers = 0
                                    continue
                            frame_data[data[0] - first_sequence_number] = data[2]
                            frame_no += 1
                            expected_sequence_numbers.remove(data[0])
                            # all frames received
                            if expected_sequence_numbers == []:
                                nacks = False
                                break
                            # last frame received but not all so send nack
                            if (data[0] == first_sequence_number + self.number_of_frames - 1) or nacks:
                                nacks = True
                                sleep(0.5)
                                self.transmit_frame(expected_sequence_numbers[0], 1, 0)
                resetAvailable()
        print frame_data

        # send acknowledgements for all the frames after sending
        sleep(0.7)
        for i in range(first_sequence_number, first_sequence_number + (self.number_of_frames/2)):
            self.transmit_frame(i, 1, self.frame_data_extractor)

        packet = 0
        for i in range(0, self.number_of_frames):
            packet += frame_data[i]
            if i != (self.number_of_frames - 1):
                packet = packet << self.frame_data_length

        if self.checksum.receiver_checksum(packet):
            return packet
        self.reliable_data_transfer_receive()

    def end_session(self):
        self.database.disconnect()
