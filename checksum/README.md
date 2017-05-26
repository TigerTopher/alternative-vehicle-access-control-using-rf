# Checksum
## Description
Checksum is a class to compute the Fletcher's checksum, specifically through the Fletcher-16 algorithm.

## Usage
### Initialization
The *bits_per_block* and *modulo* variables inside the *\_\_init\_\_* function can be changed to convert the algorithm to a Fletcher-16, Fletcher-32 or Fletcher-64 algorithm. The following are their respective values:

| Algorithm | *bits_per_block* |
| --- | --- |
| Fletcher-16 | 8 |
| Fletcher-32 | 16 |
| Fletcher-64 | 32 |

### Checksum for Transmission
The *transmitter_checksum* function takes in a *packet* as an input, appends its checksum at its end, and returns this as *packet_with_checksum*.

### Checking Packet Checksum
The *receiver_checksum* function takes in a *packet* and checks if the data in it was not tampered during transmission by using *Fletcher's Algorithm* and checking if both sums add up to 0.
