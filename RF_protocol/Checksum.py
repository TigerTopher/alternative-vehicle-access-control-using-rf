class Checksum: # Fletcher's checksum
    def __init__(self):
        self.bits_per_block = 8 # Fletcher-16
        self.modulo = 2 ** self.bits_per_block - 1

    def divider(self, packet): # divides the packet into k-bit blocks
        bits = 0 # check how many bits the packet has
        while (packet >> bits) != 0:
            bits += 1

        i = 0
        converted_bits = 0
        while converted_bits < bits: # check how many bits it has in terms of a multiple of bits_per_block
            converted_bits = i * self.bits_per_block
            i += 1

        blocks = []
        for i in range(converted_bits - self.bits_per_block, -1, -self.bits_per_block):
            blocks.append((packet >> i) & self.modulo)
            # one block is the packet shifted n number of times where n is a multiple of bits_per_block
            # with an and operation with the modulo

        return blocks

    def fletcher_algorithm(self, blocks):
        # Fletcher's algorithm
        sum_1 = 0 # C0
        sum_2 = 0 # C1
        for block in blocks:
            sum_1 = (sum_1 + block) % self.modulo # C0 = (C0prev + B) % modulo
            sum_2 = (sum_2 + sum_1) % self.modulo # C1 = (C1prev + C0) % modulo

        return [sum_1, sum_2]

    def transmitter_checksum(self, packet):
        blocks = self.divider(packet)

        sums = self.fletcher_algorithm(blocks) # [C0, C1]

        check_block_1 = self.modulo - ((sums[0] + sums[1]) % self.modulo) # CB0
        check_block_2 = self.modulo - ((sums[0] + check_block_1) % self.modulo) # CB1

        # incorporating checksum to packet
        packet_with_checksum = (packet << (self.bits_per_block * 2)) + (check_block_1 << self.bits_per_block) + check_block_2

        return packet_with_checksum

    def receiver_checksum(self, packet):
        blocks = self.divider(packet)

        sums = self.fletcher_algorithm(blocks)
        if sums[0] == sums[1] == 0: # packet with checkblocks should have blocks that add up to 0
            return True
        return False
