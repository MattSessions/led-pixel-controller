# Art-Net protocol for Fadecandy
#Adapted from https://github.com/chunk100/Glediator-with-Fadecandy

#Fadecandy stuff
import opc, time

#Artnet stuff
from twisted.internet import protocol, endpoints
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

#Initialise Fadecandy stuff
numLEDs = 1024
client = opc.Client('172.20.0.2:7890')
black = (0, 0, 0)
x_size = 16    #number of strands
y_size = 64    #numbe of lights per strand

# This tells the software where the split between 2 universes is
uni_1_y_size = 17
uni_2_y_size = 8


gridarray = [ [0],
[1, 0, 64, 128, 192, 256, 320, 384, 448],
[1, 1, 65, 129, 193, 257, 321, 385, 449],
[1, 2, 66, 130, 194, 258, 322, 386, 450],
[1, 3, 67, 131, 195, 259, 323, 387, 451],
[1, 4, 68, 132, 196, 260, 324, 388, 452],
[1, 5, 69, 133, 197, 261, 325, 389, 453],
[1, 6, 70, 134, 198, 262, 326, 390, 454],
[1, 7, 71, 135, 199, 263, 327, 391, 455],
[1, 8, 72, 136, 200, 264, 328, 392, 456],
[1, 9, 73, 137, 201, 265, 329, 393, 457],
[1, 10, 74, 138, 202, 266, 330, 394, 458],
[1, 11, 75, 139, 203, 267, 331, 395, 459],
[1, 12, 76, 140, 204, 268, 332, 396, 460],
[1, 13, 77, 141, 205, 269, 333, 397, 461],
[1, 14, 78, 142, 206, 270, 334, 398, 462],
[1, 15, 79, 143, 207, 271, 335, 399, 463],
[1, 16, 80, 144, 208, 272, 336, 400, 464],
[1, 17, 81, 145, 209, 273, 337, 401, 465],
[1, 18, 82, 146, 210, 274, 338, 402, 466],
[1, 19, 83, 147, 211, 275, 339, 403, 467],
[1, 20, 84, 148, 212, 276, 340, 404, 468],
[1, 21, 85, 149, 213, 277, 341, 405, 469],
[1, 22, 86, 150, 214, 278, 342, 406, 470],
[1, 23, 87, 151, 215, 279, 343, 407, 471],
[1, 24, 88, 152, 216, 280, 344, 408, 472],
[1, 25, 89, 153, 217, 281, 345, 409, 473],
[1, 26, 90, 154, 218, 282, 346, 410, 474],
[1, 27, 91, 155, 219, 283, 347, 411, 475],
[1, 28, 92, 156, 220, 284, 348, 412, 476],
[1, 29, 93, 157, 221, 285, 349, 413, 477],
[1, 30, 94, 158, 222, 286, 350, 414, 478],
[1, 31, 95, 159, 223, 287, 351, 415, 479],
[1, 32, 96, 160, 224, 288, 352, 416, 480],
[1, 33, 97, 161, 225, 289, 353, 417, 481],
[1, 34, 98, 162, 226, 290, 354, 418, 482],
[1, 35, 99, 163, 227, 291, 355, 419, 483],
[1, 36, 100, 164, 228, 292, 356, 420, 484],
[1, 37, 101, 165, 229, 293, 357, 421, 485],
[1, 38, 102, 166, 230, 294, 358, 422, 486],
[1, 39, 103, 167, 231, 295, 359, 423, 487],
[1, 40, 104, 168, 232, 296, 360, 424, 488],
[1, 41, 105, 169, 233, 297, 361, 425, 489],
[1, 42, 106, 170, 234, 298, 362, 426, 490],
[1, 43, 107, 171, 235, 299, 363, 427, 491],
[1, 44, 108, 172, 236, 300, 364, 428, 492],
[1, 45, 109, 173, 237, 301, 365, 429, 493],
[1, 46, 110, 174, 238, 302, 366, 430, 494],
[1, 47, 111, 175, 239, 303, 367, 431, 495],
[1, 48, 112, 176, 240, 304, 368, 432, 496],
[1, 49, 113, 177, 241, 305, 369, 433, 497],
[1, 50, 114, 178, 242, 306, 370, 434, 498],
[1, 51, 115, 179, 243, 307, 371, 435, 499],
[1, 52, 116, 180, 244, 308, 372, 436, 500],
[1, 53, 117, 181, 245, 309, 373, 437, 501],
[1, 54, 118, 182, 246, 310, 374, 438, 502],
[1, 55, 119, 183, 247, 311, 375, 439, 503],
[1, 56, 120, 184, 248, 312, 376, 440, 504],
[1, 57, 121, 185, 249, 313, 377, 441, 505],
[1, 58, 122, 186, 250, 314, 378, 442, 506],
[1, 59, 123, 187, 251, 315, 379, 443, 507],
[1, 60, 124, 188, 252, 316, 380, 444, 508],
[1, 61, 125, 189, 253, 317, 381, 445, 509],
[1, 62, 126, 190, 254, 318, 382, 446, 510],
[1, 63, 127, 191, 255, 319, 383, 447, 511]]


class ArtNet(DatagramProtocol):
    def __init__(self):
        self.pixels = [ black ] * numLEDs
        self.uni_1_data_received = 0
        self.uni_2_data_received = 0

    def write_pixels(self):
        if self.uni_1_data_received == 1 and self.uni_2_data_received == 1:
            client.put_pixels(self.pixels, 1)
            self.uni_1_data_received = 0
            self.uni_2_data_received = 0

    def datagramReceived(self, data, (host, port)):
        if ((len(data) > 18) and (data[0:8] == "Art-Net\x00")):
            rawbytes = map(ord, data)
            # print(rawbytes)
            opcode = rawbytes[8] + (rawbytes[9] << 8)
            protocolVersion = (rawbytes[10] << 8) + rawbytes[11]
            if ((opcode == 0x5000) and (protocolVersion >= 14)):
                sequence = rawbytes[12]
                physical = rawbytes[13]
                sub_net = (rawbytes[14] & 0xF0) >> 4
                universe = rawbytes[14] & 0x0F
                net = rawbytes[15]
                rgb_length = (rawbytes[16] << 8) + rawbytes[17]
                # print "seq %d phy %d sub_net %d uni %d net %d len %d" % \
                    # (sequence, physical, sub_net, universe, net, rgb_length)
                idx = 18
                x = 1

                if universe == 1:
                    y = 1

                    while ((idx < (rgb_length+18)) and (y <= uni_1_y_size)):
                        r = rawbytes[idx]
                        idx += 1
                        g = rawbytes[idx]
                        idx += 1
                        b = rawbytes[idx]
                        idx += 1
                        # print("x= " + str(x) + ", y=" + str(y) + " r=" + str(r) + ", g=" + str(g) + "b= " +str(b))
                        self.pixels[gridarray[y][x]] = (r, g, b)
                        x += 1
                        if (x > x_size):
                            x = 1
                            y += 1

                    self.uni_1_data_received = 1

                if universe == 2:
                    y = y_size - uni_2_y_size + 1

                    while ((idx < (rgb_length+18)) and (y <= y_size)):
                        r = rawbytes[idx]
                        idx += 1
                        g = rawbytes[idx]
                        idx += 1
                        b = rawbytes[idx]
                        idx += 1
                        # print("x= " + str(x) + ", y=" + str(y) + " r=" + str(r) + ", g=" + str(g) + "b= " +str(b))
                        self.pixels[gridarray[y][x]] = (r, g, b)
                        x += 1
                        if (x > x_size):
                            x = 1
                            y += 1

                    self.uni_2_data_received = 1


                self.write_pixels()


reactor.listenUDP(6454, ArtNet())
reactor.run()
