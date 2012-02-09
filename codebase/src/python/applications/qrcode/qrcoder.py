import math
from PIL import Image, ImageDraw

# QRCode for Python
#
# Ported from the Javascript library by Sam Curren
#
# Corrections for image drawing, refactoring, additional utility functions,
# formatting and commenting by Andrew Laws
#
# QRCode for Javascript
# http://d-project.googlecode.com/svn/trunk/misc/qrcode/js/qrcode.js
# http://d-project.googlecode.com/svn/trunk/misc/qrcode/
#
#
# Copyright (c) 2009 Kazuhiko Arase
#
# URL: http://www.d-project.com/
#
# Licensed under the MIT license:
#    http://www.opensource.org/licenses/mit-license.php
#
# The word "QR Code" is registered trademark of
# DENSO WAVE INCORPORATED
#   http://www.denso-wave.com/qrcode/faqpatent-e.html


class QRMode:
    NUMBER = 1 << 0
    ALPHA_NUM = 1 << 1
    BYTE = 1 << 2
    KANJI = 1 << 3


class QRErrorCorrectLevel:
    L = 1 # 7% of codewords can be restored
    M = 0 # 15% of codewords can be restored
    Q = 3 # 25% of codewords can be restored
    H = 2 # 30% of codewords can be restored


class QR8bitByte:

    def __init__(self, data):
        self.mode = QRMode.BYTE
        self.data = data


    def getLength(self):
        return len(self.data)


    def write(self, buffer):
        for i in range(len(self.data)):
            #// not JIS ...
            buffer.put(ord(self.data[i]), 8)


    def __repr__(self):
        return self.data


class QRCode:
    def __init__(self, versionNumber, errorCorrectLevel):
        self.versionNumber = versionNumber
        self.errorCorrectLevel = errorCorrectLevel
        self.modules = None
        self.moduleCount = 0
        self.dataCache = None
        self.dataList = []

    ##
    # Determine the size of the QR code (how many modules per side)
    def getSize(self):
        return 17 + self.versionNumber*4

    ##
    # Determine the area of the QR code (number of bits, raw)
    def getArea(self):
        s = self.getSize()
        return s*s


    def addData(self, data):
        newData = QR8bitByte(data)
        self.dataList.append(newData)
        self.dataCache = None


    def isDark(self, row, col):
        if (row < 0 or self.moduleCount <= row or col < 0 or self.moduleCount <= col):
            raise Exception("%s,%s - %s" % (row, col, self.moduleCount))
        return self.modules[row][col]


    def getModuleCount(self):
        return self.moduleCount


    def make(self):
        self.makeImpl(False, self.getBestMaskPattern() )


    def makeImpl(self, test, maskPattern):
        self.moduleCount = self.versionNumber * 4 + 17
        self.modules = [None for x in range(self.moduleCount)]

        for row in range(self.moduleCount):
            self.modules[row] = [None for x in range(self.moduleCount)]
            for col in range(self.moduleCount):
                self.modules[row][col] = None #//(col + row) % 3;

        self.setupPositionProbePattern(0, 0)
        self.setupPositionProbePattern(self.moduleCount - 7, 0)
        self.setupPositionProbePattern(0, self.moduleCount - 7)
        self.setupPositionAdjustPattern()
        self.setupTimingPattern()
        self.setupTypeInfo(test, maskPattern)

        if (self.versionNumber >= 7):
            self.setupTypeNumber(test)

        if (self.dataCache == None):
            self.dataCache = QRCode.createData(self.versionNumber, self.errorCorrectLevel, self.dataList)
        self.mapData(self.dataCache, maskPattern)


    def setupPositionProbePattern(self, row, col):
        for r in range(-1, 8):
            if (row + r <= -1 or self.moduleCount <= row + r):
                continue

            for c in range(-1, 8):
                if (col + c <= -1 or self.moduleCount <= col + c):
                    continue

                if ( (0 <= r and r <= 6 and (c == 0 or c == 6) )
                        or (0 <= c and c <= 6 and (r == 0 or r == 6) )
                        or (2 <= r and r <= 4 and 2 <= c and c <= 4) ):
                    self.modules[row + r][col + c] = True;
                else:
                    self.modules[row + r][col + c] = False;


    def getBestMaskPattern(self):
        minLostPoint = 0
        pattern = 0
        for i in range(8):
            self.makeImpl(True, i);
            lostPoint = QRUtil.getLostPoint(self);
            if (i == 0 or minLostPoint > lostPoint):
                minLostPoint = lostPoint
                pattern = i

        return pattern


    def createMovieClip(self):
        raise Exception("Method not relevant to Python port")

    ##
    # Make the QR Code image
    # @param boxsize pixels per box
    # @param offset number of boxes for border (should be 4, according to the specification notes at
    #        http://www.denso-wave.com/qrcode/qrgene4-e.html)
    # @return the QR code image
    def makeImage(self, boxsize=10, offset=4):
        pixelsize = (self.getModuleCount() + offset + offset) * boxsize
        im = Image.new("RGB", (pixelsize, pixelsize), "white")
        d = ImageDraw.Draw(im)

        for r in range(self.getModuleCount()):
            for c in range(self.getModuleCount()):
                if (self.isDark(r, c) ):
                    x = (c + offset) * boxsize
                    y = (r + offset) * boxsize
                    b = [(x,y),(x+boxsize-1,y+boxsize-1)]
                    d.rectangle(b,fill="black")

        del d
        return im


    def setupTimingPattern(self):
        for r in range(8, self.moduleCount - 8):
            if (self.modules[r][6] != None):
                continue
            self.modules[r][6] = (r % 2 == 0)

        for c in range(8, self.moduleCount - 8):
            if (self.modules[6][c] != None):
                continue
            self.modules[6][c] = (c % 2 == 0)


    def setupPositionAdjustPattern(self):
        pos = QRUtil.getPatternPosition(self.versionNumber)
        for i in range(len(pos)):
            for j in range(len(pos)):
                row = pos[i]
                col = pos[j]
                if (self.modules[row][col] != None):
                    continue
                for r in range(-2, 3):
                    for c in range(-2, 3):
                        if (r == -2 or r == 2 or c == -2 or c == 2 or (r == 0 and c == 0) ):
                            self.modules[row + r][col + c] = True
                        else:
                            self.modules[row + r][col + c] = False


    def setupTypeNumber(self, test):
        bits = QRUtil.getBCHTypeNumber(self.versionNumber)
        for i in range(18):
            mod = (not test and ( (bits >> i) & 1) == 1)
            self.modules[i // 3][i % 3 + self.moduleCount - 8 - 3] = mod;
        for i in range(18):
            mod = (not test and ( (bits >> i) & 1) == 1)
            self.modules[i % 3 + self.moduleCount - 8 - 3][i // 3] = mod;


    def setupTypeInfo(self, test, maskPattern):
        data = (self.errorCorrectLevel << 3) | maskPattern
        bits = QRUtil.getBCHTypeInfo(data)

        #// vertical
        for i in range(15):
            mod = (not test and ( (bits >> i) & 1) == 1)
            if (i < 6):
                self.modules[i][8] = mod
            elif (i < 8):
                self.modules[i + 1][8] = mod
            else:
                self.modules[self.moduleCount - 15 + i][8] = mod

        #// horizontal
        for i in range(15):
            mod = (not test and ( (bits >> i) & 1) == 1);
            if (i < 8):
                self.modules[8][self.moduleCount - i - 1] = mod
            elif (i < 9):
                self.modules[8][15 - i - 1 + 1] = mod
            else:
                self.modules[8][15 - i - 1] = mod

        #// fixed module
        self.modules[self.moduleCount - 8][8] = (not test)


    def mapData(self, data, maskPattern):
        inc = -1
        row = self.moduleCount - 1
        bitIndex = 7
        byteIndex = 0
        for col in range(self.moduleCount - 1, 0, -2):
            if (col == 6): col-=1
            while (True):
                for c in range(2):
                    if (self.modules[row][col - c] == None):
                        dark = False
                        if (byteIndex < len(data)):
                            dark = ( ( (data[byteIndex] >> bitIndex) & 1) == 1)
                        mask = QRUtil.getMask(maskPattern, row, col - c)
                        if (mask):
                            dark = not dark
                        self.modules[row][col - c] = dark
                        bitIndex-=1
                        if (bitIndex == -1):
                            byteIndex+=1
                            bitIndex = 7
                row += inc

                if (row < 0 or self.moduleCount <= row):
                    row -= inc
                    inc = -inc
                    break
    PAD0 = 0xEC
    PAD1 = 0x11


    ##
    # Calculates the required capacity (in bits) for a QR code to store the given number of
    # characters in the provided mode. Error correction level is taken to be 'L'
    # @param characterCount the number of characters to store
    # @param versionNumber the version of the QR code (1 - 40)
    # @return the number of bits required to store the given number of characters
    @staticmethod
    def requiredCapacityInBits(characterCount, versionNumber, mode=QRMode.ALPHA_NUM):
        # for calculation details, refer to http://www.denso-wave.com/qrcode/databit-e.html
        required_capacity = 0
        lengthInBits = QRUtil.getLengthInBits(mode, versionNumber)
        if mode == QRMode.NUMBER:
            required_capacity = versionNumber + lengthInBits + ( 10 * (characterCount / 3 )) + (0,4,7)[characterCount % 3]
        elif mode == QRMode.ALPHA_NUM:
            required_capacity = versionNumber + lengthInBits + ( 11 * (characterCount / 2 )) + (0,6)[lengthInBits % 2]
        elif mode == QRMode.BYTE:
            required_capacity = versionNumber + lengthInBits + ( 8 * characterCount )
        elif mode == QRMode.KANJI:
            required_capacity = versionNumber + lengthInBits + ( 13 * characterCount )
        return required_capacity


    @staticmethod
    def createData(versionNumber, errorCorrectLevel, dataList):
        rsBlocks = QRRSBlock.getRSBlocks(versionNumber, errorCorrectLevel)
        buffer = QRBitBuffer();

        for i in range(len(dataList)):
            data = dataList[i]
            buffer.put(data.mode, 4)
            buffer.put(data.getLength(), QRUtil.getLengthInBits(data.mode, versionNumber) )
            data.write(buffer)

        #// calc num max data.
        totalDataCount = 0;
        for i in range(len(rsBlocks)):
            totalDataCount += rsBlocks[i].dataCount

        if (buffer.getLengthInBits() > totalDataCount * 8):
            raise Exception("code length overflow. (%d > %d)" % (buffer.getLengthInBits(), (totalDataCount * 8)) )

        #// end code
        if (buffer.getLengthInBits() + 4 <= totalDataCount * 8):
            buffer.put(0, 4)

        #// padding
        while (buffer.getLengthInBits() % 8 != 0):
            buffer.putBit(False)

        #// padding
        while (True):
            if (buffer.getLengthInBits() >= totalDataCount * 8):
                break
            buffer.put(QRCode.PAD0, 8)

            if (buffer.getLengthInBits() >= totalDataCount * 8):
                break
            buffer.put(QRCode.PAD1, 8)

        return QRCode.createBytes(buffer, rsBlocks)


    @staticmethod
    def createBytes(buffer, rsBlocks):
        offset = 0
        maxDcCount = 0
        maxEcCount = 0
        dcdata = [0 for x in range(len(rsBlocks))]
        ecdata = [0 for x in range(len(rsBlocks))]

        for r in range(len(rsBlocks)):
            dcCount = rsBlocks[r].dataCount
            ecCount = rsBlocks[r].totalCount - dcCount
            maxDcCount = max(maxDcCount, dcCount)
            maxEcCount = max(maxEcCount, ecCount)

            dcdata[r] = [0 for x in range(dcCount)]

            for i in range(len(dcdata[r])):
                dcdata[r][i] = 0xff & buffer.buffer[i + offset]
            offset += dcCount

            rsPoly = QRUtil.getErrorCorrectPolynomial(ecCount)
            rawPoly = QRPolynomial(dcdata[r], rsPoly.getLength() - 1)

            modPoly = rawPoly.mod(rsPoly)
            ecdata[r] = [0 for x in range(rsPoly.getLength()-1)]
            for i in range(len(ecdata[r])):
                modIndex = i + modPoly.getLength() - len(ecdata[r])
                if (modIndex >= 0):
                    ecdata[r][i] = modPoly.get(modIndex)
                else:
                    ecdata[r][i] = 0

        totalCodeCount = 0
        for i in range(len(rsBlocks)):
            totalCodeCount += rsBlocks[i].totalCount

        data = [None for x in range(totalCodeCount)]
        index = 0

        for i in range(maxDcCount):
            for r in range(len(rsBlocks)):
                if (i < len(dcdata[r])):
                    data[index] = dcdata[r][i]
                    index+=1

        for i in range(maxEcCount):
            for r in range(len(rsBlocks)):
                if (i < len(ecdata[r])):
                    data[index] = ecdata[r][i]
                    index+=1

        return data


class QRMaskPattern:
    PATTERN000 = 0
    PATTERN001 = 1
    PATTERN010 = 2
    PATTERN011 = 3
    PATTERN100 = 4
    PATTERN101 = 5
    PATTERN110 = 6
    PATTERN111 = 7


class QRUtil(object):
    PATTERN_POSITION_TABLE = [
        [],
        [6, 18],
        [6, 22],
        [6, 26],
        [6, 30],
        [6, 34],
        [6, 22, 38],
        [6, 24, 42],
        [6, 26, 46],
        [6, 28, 50],
        [6, 30, 54],
        [6, 32, 58],
        [6, 34, 62],
        [6, 26, 46, 66],
        [6, 26, 48, 70],
        [6, 26, 50, 74],
        [6, 30, 54, 78],
        [6, 30, 56, 82],
        [6, 30, 58, 86],
        [6, 34, 62, 90],
        [6, 28, 50, 72, 94],
        [6, 26, 50, 74, 98],
        [6, 30, 54, 78, 102],
        [6, 28, 54, 80, 106],
        [6, 32, 58, 84, 110],
        [6, 30, 58, 86, 114],
        [6, 34, 62, 90, 118],
        [6, 26, 50, 74, 98, 122],
        [6, 30, 54, 78, 102, 126],
        [6, 26, 52, 78, 104, 130],
        [6, 30, 56, 82, 108, 134],
        [6, 34, 60, 86, 112, 138],
        [6, 30, 58, 86, 114, 142],
        [6, 34, 62, 90, 118, 146],
        [6, 30, 54, 78, 102, 126, 150],
        [6, 24, 50, 76, 102, 128, 154],
        [6, 28, 54, 80, 106, 132, 158],
        [6, 32, 58, 84, 110, 136, 162],
        [6, 26, 54, 82, 110, 138, 166],
        [6, 30, 58, 86, 114, 142, 170]
    ]

    G15 = (1 << 10) | (1 << 8) | (1 << 5) | (1 << 4) | (1 << 2) | (1 << 1) | (1 << 0)
    G18 = (1 << 12) | (1 << 11) | (1 << 10) | (1 << 9) | (1 << 8) | (1 << 5) | (1 << 2) | (1 << 0)
    G15_MASK = (1 << 14) | (1 << 12) | (1 << 10) | (1 << 4) | (1 << 1)

    ##
    # A lookup table containing the capacities of all combinations of QR Code versions, error
    # correction levels and data types
    # see http://www.denso-wave.com/qrcode/vertable1-e.html
    CAPACITY_LOOKUP = {
        1:    {QRErrorCorrectLevel.L: {'bits':152, QRMode.NUMBER:41, QRMode.ALPHA_NUM:25, QRMode.BYTE:17, QRMode.KANJI:10},
               QRErrorCorrectLevel.M: {'bits':128, QRMode.NUMBER:34, QRMode.ALPHA_NUM:20, QRMode.BYTE:14, QRMode.KANJI:8},
               QRErrorCorrectLevel.Q: {'bits':104, QRMode.NUMBER:27, QRMode.ALPHA_NUM:16, QRMode.BYTE:11, QRMode.KANJI:7},
               QRErrorCorrectLevel.H: {'bits':72, QRMode.NUMBER:17, QRMode.ALPHA_NUM:10, QRMode.BYTE:7, QRMode.KANJI:4}
            },
        2:    {QRErrorCorrectLevel.L: {'bits':272, QRMode.NUMBER:77, QRMode.ALPHA_NUM:47, QRMode.BYTE:32, QRMode.KANJI:20},
               QRErrorCorrectLevel.M: {'bits':224, QRMode.NUMBER:63, QRMode.ALPHA_NUM:38, QRMode.BYTE:26, QRMode.KANJI:16},
               QRErrorCorrectLevel.Q: {'bits':176, QRMode.NUMBER:48, QRMode.ALPHA_NUM:29, QRMode.BYTE:20, QRMode.KANJI:12},
               QRErrorCorrectLevel.H: {'bits':128, QRMode.NUMBER:34, QRMode.ALPHA_NUM:20, QRMode.BYTE:14, QRMode.KANJI:8}
            },
        3:    {QRErrorCorrectLevel.L: {'bits':440, QRMode.NUMBER:127, QRMode.ALPHA_NUM:77, QRMode.BYTE:53, QRMode.KANJI:32},
               QRErrorCorrectLevel.M: {'bits':352, QRMode.NUMBER:101, QRMode.ALPHA_NUM:61, QRMode.BYTE:42, QRMode.KANJI:26},
               QRErrorCorrectLevel.Q: {'bits':272, QRMode.NUMBER:77, QRMode.ALPHA_NUM:47, QRMode.BYTE:32, QRMode.KANJI:20},
               QRErrorCorrectLevel.H: {'bits':208, QRMode.NUMBER:58, QRMode.ALPHA_NUM:35, QRMode.BYTE:24, QRMode.KANJI:15}
            },
        4:    {QRErrorCorrectLevel.L: {'bits':640, QRMode.NUMBER:187, QRMode.ALPHA_NUM:114, QRMode.BYTE:78, QRMode.KANJI:48},
               QRErrorCorrectLevel.M: {'bits':512, QRMode.NUMBER:149, QRMode.ALPHA_NUM:90, QRMode.BYTE:62, QRMode.KANJI:38},
               QRErrorCorrectLevel.Q: {'bits':384, QRMode.NUMBER:111, QRMode.ALPHA_NUM:67, QRMode.BYTE:46, QRMode.KANJI:28},
               QRErrorCorrectLevel.H: {'bits':288, QRMode.NUMBER:82, QRMode.ALPHA_NUM:50, QRMode.BYTE:34, QRMode.KANJI:21}
            },
        5:    {QRErrorCorrectLevel.L: {'bits':864, QRMode.NUMBER:255, QRMode.ALPHA_NUM:154, QRMode.BYTE:106, QRMode.KANJI:65},
               QRErrorCorrectLevel.M: {'bits':688, QRMode.NUMBER:202, QRMode.ALPHA_NUM:122, QRMode.BYTE:84, QRMode.KANJI:52},
               QRErrorCorrectLevel.Q: {'bits':496, QRMode.NUMBER:144, QRMode.ALPHA_NUM:87, QRMode.BYTE:60, QRMode.KANJI:37},
               QRErrorCorrectLevel.H: {'bits':368, QRMode.NUMBER:106, QRMode.ALPHA_NUM:64, QRMode.BYTE:44, QRMode.KANJI:27}
            },
        6:    {QRErrorCorrectLevel.L: {'bits':1088, QRMode.NUMBER:322, QRMode.ALPHA_NUM:195, QRMode.BYTE:134, QRMode.KANJI:82},
               QRErrorCorrectLevel.M: {'bits':864, QRMode.NUMBER:255, QRMode.ALPHA_NUM:154, QRMode.BYTE:106, QRMode.KANJI:65},
               QRErrorCorrectLevel.Q: {'bits':608, QRMode.NUMBER:178, QRMode.ALPHA_NUM:108, QRMode.BYTE:74, QRMode.KANJI:45},
               QRErrorCorrectLevel.H: {'bits':480, QRMode.NUMBER:139, QRMode.ALPHA_NUM:84, QRMode.BYTE:58, QRMode.KANJI:36}
            },
        7:    {QRErrorCorrectLevel.L: {'bits':1248, QRMode.NUMBER:370, QRMode.ALPHA_NUM:224, QRMode.BYTE:154, QRMode.KANJI:95},
               QRErrorCorrectLevel.M: {'bits':992, QRMode.NUMBER:293, QRMode.ALPHA_NUM:178, QRMode.BYTE:122, QRMode.KANJI:75},
               QRErrorCorrectLevel.Q: {'bits':704, QRMode.NUMBER:207, QRMode.ALPHA_NUM:125, QRMode.BYTE:86, QRMode.KANJI:53},
               QRErrorCorrectLevel.H: {'bits':528, QRMode.NUMBER:154, QRMode.ALPHA_NUM:93, QRMode.BYTE:64, QRMode.KANJI:39}
            },
        8:    {QRErrorCorrectLevel.L: {'bits':1552, QRMode.NUMBER:461, QRMode.ALPHA_NUM:279, QRMode.BYTE:192, QRMode.KANJI:118},
               QRErrorCorrectLevel.M: {'bits':1232, QRMode.NUMBER:365, QRMode.ALPHA_NUM:221, QRMode.BYTE:152, QRMode.KANJI:93},
               QRErrorCorrectLevel.Q: {'bits':880, QRMode.NUMBER:259, QRMode.ALPHA_NUM:157, QRMode.BYTE:108, QRMode.KANJI:66},
               QRErrorCorrectLevel.H: {'bits':688, QRMode.NUMBER:202, QRMode.ALPHA_NUM:122, QRMode.BYTE:84, QRMode.KANJI:52}
            },
        9:    {QRErrorCorrectLevel.L: {'bits':1856, QRMode.NUMBER:552, QRMode.ALPHA_NUM:335, QRMode.BYTE:230, QRMode.KANJI:141},
               QRErrorCorrectLevel.M: {'bits':1456, QRMode.NUMBER:432, QRMode.ALPHA_NUM:262, QRMode.BYTE:180, QRMode.KANJI:111},
               QRErrorCorrectLevel.Q: {'bits':1056, QRMode.NUMBER:312, QRMode.ALPHA_NUM:189, QRMode.BYTE:130, QRMode.KANJI:80},
               QRErrorCorrectLevel.H: {'bits':800, QRMode.NUMBER:235, QRMode.ALPHA_NUM:143, QRMode.BYTE:98, QRMode.KANJI:60}
            },
        10:    {QRErrorCorrectLevel.L: {'bits':2192, QRMode.NUMBER:652, QRMode.ALPHA_NUM:395, QRMode.BYTE:271, QRMode.KANJI:167},
                QRErrorCorrectLevel.M: {'bits':1728, QRMode.NUMBER:513, QRMode.ALPHA_NUM:311, QRMode.BYTE:213, QRMode.KANJI:131},
                QRErrorCorrectLevel.Q: {'bits':1232, QRMode.NUMBER:364, QRMode.ALPHA_NUM:221, QRMode.BYTE:151, QRMode.KANJI:93},
                QRErrorCorrectLevel.H: {'bits':976, QRMode.NUMBER:288, QRMode.ALPHA_NUM:174, QRMode.BYTE:119, QRMode.KANJI:74}
            },
        11:    {QRErrorCorrectLevel.L: {'bits':2592, QRMode.NUMBER:772, QRMode.ALPHA_NUM:468, QRMode.BYTE:321, QRMode.KANJI:198},
                QRErrorCorrectLevel.M: {'bits':2032, QRMode.NUMBER:604, QRMode.ALPHA_NUM:366, QRMode.BYTE:251, QRMode.KANJI:155},
                QRErrorCorrectLevel.Q: {'bits':1440, QRMode.NUMBER:427, QRMode.ALPHA_NUM:259, QRMode.BYTE:177, QRMode.KANJI:109},
                QRErrorCorrectLevel.H: {'bits':1120, QRMode.NUMBER:331, QRMode.ALPHA_NUM:200, QRMode.BYTE:137, QRMode.KANJI:85}
            },
        12:    {QRErrorCorrectLevel.L: {'bits':2960, QRMode.NUMBER:883, QRMode.ALPHA_NUM:535, QRMode.BYTE:367, QRMode.KANJI:226},
                QRErrorCorrectLevel.M: {'bits':2320, QRMode.NUMBER:691, QRMode.ALPHA_NUM:419, QRMode.BYTE:287, QRMode.KANJI:177},
                QRErrorCorrectLevel.Q: {'bits':1648, QRMode.NUMBER:489, QRMode.ALPHA_NUM:296, QRMode.BYTE:203, QRMode.KANJI:125},
                QRErrorCorrectLevel.H: {'bits':1264, QRMode.NUMBER:374, QRMode.ALPHA_NUM:227, QRMode.BYTE:155, QRMode.KANJI:96}
            },
        13:    {QRErrorCorrectLevel.L: {'bits':3424, QRMode.NUMBER:1022, QRMode.ALPHA_NUM:619, QRMode.BYTE:425, QRMode.KANJI:262},
                QRErrorCorrectLevel.M: {'bits':2672, QRMode.NUMBER:796, QRMode.ALPHA_NUM:483, QRMode.BYTE:331, QRMode.KANJI:204},
                QRErrorCorrectLevel.Q: {'bits':1952, QRMode.NUMBER:580, QRMode.ALPHA_NUM:352, QRMode.BYTE:241, QRMode.KANJI:149},
                QRErrorCorrectLevel.H: {'bits':1440, QRMode.NUMBER:427, QRMode.ALPHA_NUM:259, QRMode.BYTE:177, QRMode.KANJI:109}
            },
        14:    {QRErrorCorrectLevel.L: {'bits':3688, QRMode.NUMBER:1101, QRMode.ALPHA_NUM:667, QRMode.BYTE:458, QRMode.KANJI:282},
                QRErrorCorrectLevel.M: {'bits':2920, QRMode.NUMBER:871, QRMode.ALPHA_NUM:528, QRMode.BYTE:362, QRMode.KANJI:223},
                QRErrorCorrectLevel.Q: {'bits':2088, QRMode.NUMBER:621, QRMode.ALPHA_NUM:376, QRMode.BYTE:258, QRMode.KANJI:159},
                QRErrorCorrectLevel.H: {'bits':1576, QRMode.NUMBER:468, QRMode.ALPHA_NUM:283, QRMode.BYTE:194, QRMode.KANJI:120}
            },
        15:    {QRErrorCorrectLevel.L: {'bits':4184, QRMode.NUMBER:1250, QRMode.ALPHA_NUM:758, QRMode.BYTE:520, QRMode.KANJI:320},
                QRErrorCorrectLevel.M: {'bits':3320, QRMode.NUMBER:991, QRMode.ALPHA_NUM:600, QRMode.BYTE:412, QRMode.KANJI:254},
                QRErrorCorrectLevel.Q: {'bits':2360, QRMode.NUMBER:703, QRMode.ALPHA_NUM:426, QRMode.BYTE:292, QRMode.KANJI:180},
                QRErrorCorrectLevel.H: {'bits':1784, QRMode.NUMBER:530, QRMode.ALPHA_NUM:321, QRMode.BYTE:220, QRMode.KANJI:136}
            },
        16:    {QRErrorCorrectLevel.L: {'bits':4712, QRMode.NUMBER:1408, QRMode.ALPHA_NUM:854, QRMode.BYTE:586, QRMode.KANJI:361},
                QRErrorCorrectLevel.M: {'bits':3624, QRMode.NUMBER:1082, QRMode.ALPHA_NUM:656, QRMode.BYTE:450, QRMode.KANJI:277},
                QRErrorCorrectLevel.Q: {'bits':2600, QRMode.NUMBER:775, QRMode.ALPHA_NUM:470, QRMode.BYTE:322, QRMode.KANJI:198},
                QRErrorCorrectLevel.H: {'bits':2024, QRMode.NUMBER:602, QRMode.ALPHA_NUM:365, QRMode.BYTE:250, QRMode.KANJI:154}
            },
        17:    {QRErrorCorrectLevel.L: {'bits':5176, QRMode.NUMBER:1548, QRMode.ALPHA_NUM:938, QRMode.BYTE:644, QRMode.KANJI:397},
                QRErrorCorrectLevel.M: {'bits':4056, QRMode.NUMBER:1212, QRMode.ALPHA_NUM:734, QRMode.BYTE:504, QRMode.KANJI:310},
                QRErrorCorrectLevel.Q: {'bits':2936, QRMode.NUMBER:876, QRMode.ALPHA_NUM:531, QRMode.BYTE:364, QRMode.KANJI:224},
                QRErrorCorrectLevel.H: {'bits':2264, QRMode.NUMBER:674, QRMode.ALPHA_NUM:408, QRMode.BYTE:280, QRMode.KANJI:173}
            },
        18:    {QRErrorCorrectLevel.L: {'bits':5768, QRMode.NUMBER:1725, QRMode.ALPHA_NUM:1046, QRMode.BYTE:718, QRMode.KANJI:442},
                QRErrorCorrectLevel.M: {'bits':4504, QRMode.NUMBER:1346, QRMode.ALPHA_NUM:816, QRMode.BYTE:560, QRMode.KANJI:345},
                QRErrorCorrectLevel.Q: {'bits':3176, QRMode.NUMBER:948, QRMode.ALPHA_NUM:574, QRMode.BYTE:394, QRMode.KANJI:243},
                QRErrorCorrectLevel.H: {'bits':2504, QRMode.NUMBER:746, QRMode.ALPHA_NUM:452, QRMode.BYTE:310, QRMode.KANJI:191}
            },
        19:    {QRErrorCorrectLevel.L: {'bits':6360, QRMode.NUMBER:1903, QRMode.ALPHA_NUM:1153, QRMode.BYTE:792, QRMode.KANJI:488},
                QRErrorCorrectLevel.M: {'bits':5016, QRMode.NUMBER:1500, QRMode.ALPHA_NUM:909, QRMode.BYTE:624, QRMode.KANJI:384},
                QRErrorCorrectLevel.Q: {'bits':3560, QRMode.NUMBER:1063, QRMode.ALPHA_NUM:644, QRMode.BYTE:442, QRMode.KANJI:272},
                QRErrorCorrectLevel.H: {'bits':2728, QRMode.NUMBER:813, QRMode.ALPHA_NUM:493, QRMode.BYTE:338, QRMode.KANJI:208}
            },
        20:    {QRErrorCorrectLevel.L: {'bits':6888, QRMode.NUMBER:2061, QRMode.ALPHA_NUM:1249, QRMode.BYTE:858, QRMode.KANJI:528},
                QRErrorCorrectLevel.M: {'bits':5352, QRMode.NUMBER:1600, QRMode.ALPHA_NUM:970, QRMode.BYTE:666, QRMode.KANJI:410},
                QRErrorCorrectLevel.Q: {'bits':3880, QRMode.NUMBER:1159, QRMode.ALPHA_NUM:702, QRMode.BYTE:482, QRMode.KANJI:297},
                QRErrorCorrectLevel.H: {'bits':3080, QRMode.NUMBER:919, QRMode.ALPHA_NUM:557, QRMode.BYTE:382, QRMode.KANJI:235}
            },
        21:    {QRErrorCorrectLevel.L: {'bits':7456, QRMode.NUMBER:2232, QRMode.ALPHA_NUM:1352, QRMode.BYTE:929, QRMode.KANJI:572},
                QRErrorCorrectLevel.M: {'bits':5712, QRMode.NUMBER:1708, QRMode.ALPHA_NUM:1035, QRMode.BYTE:711, QRMode.KANJI:438},
                QRErrorCorrectLevel.Q: {'bits':4096, QRMode.NUMBER:1224, QRMode.ALPHA_NUM:742, QRMode.BYTE:509, QRMode.KANJI:314},
                QRErrorCorrectLevel.H: {'bits':3248, QRMode.NUMBER:969, QRMode.ALPHA_NUM:587, QRMode.BYTE:403, QRMode.KANJI:248}
            },
        22:    {QRErrorCorrectLevel.L: {'bits':8048, QRMode.NUMBER:2409, QRMode.ALPHA_NUM:1460, QRMode.BYTE:1003, QRMode.KANJI:618},
                QRErrorCorrectLevel.M: {'bits':6256, QRMode.NUMBER:1872, QRMode.ALPHA_NUM:1134, QRMode.BYTE:779, QRMode.KANJI:480},
                QRErrorCorrectLevel.Q: {'bits':4544, QRMode.NUMBER:1358, QRMode.ALPHA_NUM:823, QRMode.BYTE:565, QRMode.KANJI:348},
                QRErrorCorrectLevel.H: {'bits':3536, QRMode.NUMBER:1056, QRMode.ALPHA_NUM:640, QRMode.BYTE:439, QRMode.KANJI:270}
            },
        23:    {QRErrorCorrectLevel.L: {'bits':8752, QRMode.NUMBER:2620, QRMode.ALPHA_NUM:1588, QRMode.BYTE:1091, QRMode.KANJI:672},
                QRErrorCorrectLevel.M: {'bits':6880, QRMode.NUMBER:2059, QRMode.ALPHA_NUM:1248, QRMode.BYTE:857, QRMode.KANJI:528},
                QRErrorCorrectLevel.Q: {'bits':4912, QRMode.NUMBER:1468, QRMode.ALPHA_NUM:890, QRMode.BYTE:611, QRMode.KANJI:376},
                QRErrorCorrectLevel.H: {'bits':3712, QRMode.NUMBER:1108, QRMode.ALPHA_NUM:672, QRMode.BYTE:461, QRMode.KANJI:284}
            },
        24:    {QRErrorCorrectLevel.L: {'bits':9392, QRMode.NUMBER:2812, QRMode.ALPHA_NUM:1704, QRMode.BYTE:1171, QRMode.KANJI:721},
                QRErrorCorrectLevel.M: {'bits':7312, QRMode.NUMBER:2188, QRMode.ALPHA_NUM:1326, QRMode.BYTE:911, QRMode.KANJI:561},
                QRErrorCorrectLevel.Q: {'bits':5312, QRMode.NUMBER:1588, QRMode.ALPHA_NUM:963, QRMode.BYTE:661, QRMode.KANJI:407},
                QRErrorCorrectLevel.H: {'bits':4112, QRMode.NUMBER:1228, QRMode.ALPHA_NUM:744, QRMode.BYTE:511, QRMode.KANJI:315}
            },
        25:    {QRErrorCorrectLevel.L: {'bits':10208, QRMode.NUMBER:3057, QRMode.ALPHA_NUM:1853, QRMode.BYTE:1273, QRMode.KANJI:784},
                QRErrorCorrectLevel.M: {'bits':8000, QRMode.NUMBER:2395, QRMode.ALPHA_NUM:1451, QRMode.BYTE:997, QRMode.KANJI:614},
                QRErrorCorrectLevel.Q: {'bits':5744, QRMode.NUMBER:1718, QRMode.ALPHA_NUM:1041, QRMode.BYTE:715, QRMode.KANJI:440},
                QRErrorCorrectLevel.H: {'bits':4304, QRMode.NUMBER:1286, QRMode.ALPHA_NUM:779, QRMode.BYTE:535, QRMode.KANJI:330}
            },
        26:    {QRErrorCorrectLevel.L: {'bits':10960, QRMode.NUMBER:3283, QRMode.ALPHA_NUM:1990, QRMode.BYTE:1367, QRMode.KANJI:842},
                QRErrorCorrectLevel.M: {'bits':8496, QRMode.NUMBER:2544, QRMode.ALPHA_NUM:1542, QRMode.BYTE:1059, QRMode.KANJI:652},
                QRErrorCorrectLevel.Q: {'bits':6032, QRMode.NUMBER:1804, QRMode.ALPHA_NUM:1094, QRMode.BYTE:751, QRMode.KANJI:462},
                QRErrorCorrectLevel.H: {'bits':4768, QRMode.NUMBER:1425, QRMode.ALPHA_NUM:864, QRMode.BYTE:593, QRMode.KANJI:365}
            },
        27:    {QRErrorCorrectLevel.L: {'bits':11744, QRMode.NUMBER:3514, QRMode.ALPHA_NUM:2132, QRMode.BYTE:1465, QRMode.KANJI:902},
                QRErrorCorrectLevel.M: {'bits':9024, QRMode.NUMBER:2701, QRMode.ALPHA_NUM:1637, QRMode.BYTE:1125, QRMode.KANJI:692},
                QRErrorCorrectLevel.Q: {'bits':6464, QRMode.NUMBER:1933, QRMode.ALPHA_NUM:1172, QRMode.BYTE:805, QRMode.KANJI:496},
                QRErrorCorrectLevel.H: {'bits':5024, QRMode.NUMBER:1501, QRMode.ALPHA_NUM:910, QRMode.BYTE:625, QRMode.KANJI:385}
            },
        28:    {QRErrorCorrectLevel.L: {'bits':12248, QRMode.NUMBER:3669, QRMode.ALPHA_NUM:2223, QRMode.BYTE:1528, QRMode.KANJI:940},
                QRErrorCorrectLevel.M: {'bits':9544, QRMode.NUMBER:2857, QRMode.ALPHA_NUM:1732, QRMode.BYTE:1190, QRMode.KANJI:732},
                QRErrorCorrectLevel.Q: {'bits':6968, QRMode.NUMBER:2085, QRMode.ALPHA_NUM:1263, QRMode.BYTE:868, QRMode.KANJI:534},
                QRErrorCorrectLevel.H: {'bits':5288, QRMode.NUMBER:1581, QRMode.ALPHA_NUM:958, QRMode.BYTE:658, QRMode.KANJI:405}
            },
        29:    {QRErrorCorrectLevel.L: {'bits':13048, QRMode.NUMBER:3909, QRMode.ALPHA_NUM:2369, QRMode.BYTE:1628, QRMode.KANJI:1002},
                QRErrorCorrectLevel.M: {'bits':10136, QRMode.NUMBER:3035, QRMode.ALPHA_NUM:1839, QRMode.BYTE:1264, QRMode.KANJI:778},
                QRErrorCorrectLevel.Q: {'bits':7288, QRMode.NUMBER:2181, QRMode.ALPHA_NUM:1322, QRMode.BYTE:908, QRMode.KANJI:559},
                QRErrorCorrectLevel.H: {'bits':5608, QRMode.NUMBER:1677, QRMode.ALPHA_NUM:1016, QRMode.BYTE:698, QRMode.KANJI:430}
            },
        30:    {QRErrorCorrectLevel.L: {'bits':13880, QRMode.NUMBER:4158, QRMode.ALPHA_NUM:2520, QRMode.BYTE:1732, QRMode.KANJI:1066},
                QRErrorCorrectLevel.M: {'bits':10984, QRMode.NUMBER:3289, QRMode.ALPHA_NUM:1994, QRMode.BYTE:1370, QRMode.KANJI:843},
                QRErrorCorrectLevel.Q: {'bits':7880, QRMode.NUMBER:2358, QRMode.ALPHA_NUM:1429, QRMode.BYTE:982, QRMode.KANJI:604},
                QRErrorCorrectLevel.H: {'bits':5960, QRMode.NUMBER:1782, QRMode.ALPHA_NUM:1080, QRMode.BYTE:742, QRMode.KANJI:457}
            },
        31:    {QRErrorCorrectLevel.L: {'bits':14744, QRMode.NUMBER:4417, QRMode.ALPHA_NUM:2677, QRMode.BYTE:1840, QRMode.KANJI:1132},
                QRErrorCorrectLevel.M: {'bits':11640, QRMode.NUMBER:3486, QRMode.ALPHA_NUM:2113, QRMode.BYTE:1452, QRMode.KANJI:894},
                QRErrorCorrectLevel.Q: {'bits':8264, QRMode.NUMBER:2473, QRMode.ALPHA_NUM:1499, QRMode.BYTE:1030, QRMode.KANJI:634},
                QRErrorCorrectLevel.H: {'bits':6344, QRMode.NUMBER:1897, QRMode.ALPHA_NUM:1150, QRMode.BYTE:790, QRMode.KANJI:486}
            },
        32:    {QRErrorCorrectLevel.L: {'bits':15640, QRMode.NUMBER:4686, QRMode.ALPHA_NUM:2840, QRMode.BYTE:1952, QRMode.KANJI:1201},
                QRErrorCorrectLevel.M: {'bits':12328, QRMode.NUMBER:3693, QRMode.ALPHA_NUM:2238, QRMode.BYTE:1538, QRMode.KANJI:947},
                QRErrorCorrectLevel.Q: {'bits':8920, QRMode.NUMBER:2670, QRMode.ALPHA_NUM:1618, QRMode.BYTE:1112, QRMode.KANJI:684},
                QRErrorCorrectLevel.H: {'bits':6760, QRMode.NUMBER:2022, QRMode.ALPHA_NUM:1226, QRMode.BYTE:842, QRMode.KANJI:518}
            },
        33:    {QRErrorCorrectLevel.L: {'bits':16568, QRMode.NUMBER:4965, QRMode.ALPHA_NUM:3009, QRMode.BYTE:2068, QRMode.KANJI:1273},
                QRErrorCorrectLevel.M: {'bits':13048, QRMode.NUMBER:3909, QRMode.ALPHA_NUM:2369, QRMode.BYTE:1628, QRMode.KANJI:1002},
                QRErrorCorrectLevel.Q: {'bits':9368, QRMode.NUMBER:2805, QRMode.ALPHA_NUM:1700, QRMode.BYTE:1168, QRMode.KANJI:719},
                QRErrorCorrectLevel.H: {'bits':7208, QRMode.NUMBER:2157, QRMode.ALPHA_NUM:1307, QRMode.BYTE:898, QRMode.KANJI:553}
            },
        34:    {QRErrorCorrectLevel.L: {'bits':17528, QRMode.NUMBER:5253, QRMode.ALPHA_NUM:3183, QRMode.BYTE:2188, QRMode.KANJI:1347},
                QRErrorCorrectLevel.M: {'bits':13800, QRMode.NUMBER:4134, QRMode.ALPHA_NUM:2506, QRMode.BYTE:1722, QRMode.KANJI:1060},
                QRErrorCorrectLevel.Q: {'bits':9848, QRMode.NUMBER:2949, QRMode.ALPHA_NUM:1787, QRMode.BYTE:1228, QRMode.KANJI:756},
                QRErrorCorrectLevel.H: {'bits':7688, QRMode.NUMBER:2301, QRMode.ALPHA_NUM:1394, QRMode.BYTE:958, QRMode.KANJI:590}
            },
        35:    {QRErrorCorrectLevel.L: {'bits':18448, QRMode.NUMBER:5529, QRMode.ALPHA_NUM:3351, QRMode.BYTE:2303, QRMode.KANJI:1417},
                QRErrorCorrectLevel.M: {'bits':14496, QRMode.NUMBER:4343, QRMode.ALPHA_NUM:2632, QRMode.BYTE:1809, QRMode.KANJI:1113},
                QRErrorCorrectLevel.Q: {'bits':10288, QRMode.NUMBER:3081, QRMode.ALPHA_NUM:1867, QRMode.BYTE:1283, QRMode.KANJI:790},
                QRErrorCorrectLevel.H: {'bits':7888, QRMode.NUMBER:2361, QRMode.ALPHA_NUM:1431, QRMode.BYTE:983, QRMode.KANJI:605}
            },
        36:    {QRErrorCorrectLevel.L: {'bits':19472, QRMode.NUMBER:5836, QRMode.ALPHA_NUM:3537, QRMode.BYTE:2431, QRMode.KANJI:1496},
                QRErrorCorrectLevel.M: {'bits':15312, QRMode.NUMBER:4588, QRMode.ALPHA_NUM:2780, QRMode.BYTE:1911, QRMode.KANJI:1176},
                QRErrorCorrectLevel.Q: {'bits':10832, QRMode.NUMBER:3244, QRMode.ALPHA_NUM:1966, QRMode.BYTE:1351, QRMode.KANJI:832},
                QRErrorCorrectLevel.H: {'bits':8432, QRMode.NUMBER:2524, QRMode.ALPHA_NUM:1530, QRMode.BYTE:1051, QRMode.KANJI:647}
            },
        37:    {QRErrorCorrectLevel.L: {'bits':20528, QRMode.NUMBER:6153, QRMode.ALPHA_NUM:3729, QRMode.BYTE:2563, QRMode.KANJI:1577},
                QRErrorCorrectLevel.M: {'bits':15936, QRMode.NUMBER:4775, QRMode.ALPHA_NUM:2894, QRMode.BYTE:1989, QRMode.KANJI:1224},
                QRErrorCorrectLevel.Q: {'bits':11408, QRMode.NUMBER:3417, QRMode.ALPHA_NUM:2071, QRMode.BYTE:1423, QRMode.KANJI:876},
                QRErrorCorrectLevel.H: {'bits':8768, QRMode.NUMBER:2625, QRMode.ALPHA_NUM:1591, QRMode.BYTE:1093, QRMode.KANJI:673}
            },
        38:    {QRErrorCorrectLevel.L: {'bits':21616, QRMode.NUMBER:6479, QRMode.ALPHA_NUM:3927, QRMode.BYTE:2699, QRMode.KANJI:1661},
                QRErrorCorrectLevel.M: {'bits':16816, QRMode.NUMBER:5039, QRMode.ALPHA_NUM:3054, QRMode.BYTE:2099, QRMode.KANJI:1292},
                QRErrorCorrectLevel.Q: {'bits':12016, QRMode.NUMBER:3599, QRMode.ALPHA_NUM:2181, QRMode.BYTE:1499, QRMode.KANJI:923},
                QRErrorCorrectLevel.H: {'bits':9136, QRMode.NUMBER:2735, QRMode.ALPHA_NUM:1658, QRMode.BYTE:1139, QRMode.KANJI:701}
            },
        39:    {QRErrorCorrectLevel.L: {'bits':22496, QRMode.NUMBER:6743, QRMode.ALPHA_NUM:4087, QRMode.BYTE:2809, QRMode.KANJI:1729},
                QRErrorCorrectLevel.M: {'bits':17728, QRMode.NUMBER:5313, QRMode.ALPHA_NUM:3220, QRMode.BYTE:2213, QRMode.KANJI:1362},
                QRErrorCorrectLevel.Q: {'bits':12656, QRMode.NUMBER:3791, QRMode.ALPHA_NUM:2298, QRMode.BYTE:1579, QRMode.KANJI:972},
                QRErrorCorrectLevel.H: {'bits':9776, QRMode.NUMBER:2927, QRMode.ALPHA_NUM:1774, QRMode.BYTE:1219, QRMode.KANJI:750}
            },
        40:    {QRErrorCorrectLevel.L: {'bits':23648, QRMode.NUMBER:7089, QRMode.ALPHA_NUM:4296, QRMode.BYTE:2953, QRMode.KANJI:1817},
                QRErrorCorrectLevel.M: {'bits':18672, QRMode.NUMBER:5596, QRMode.ALPHA_NUM:3391, QRMode.BYTE:2331, QRMode.KANJI:1435},
                QRErrorCorrectLevel.Q: {'bits':13328, QRMode.NUMBER:3993, QRMode.ALPHA_NUM:2420, QRMode.BYTE:1663, QRMode.KANJI:1024},
                QRErrorCorrectLevel.H: {'bits':10208, QRMode.NUMBER:3057, QRMode.ALPHA_NUM:1852, QRMode.BYTE:1273, QRMode.KANJI:784}
            }
    }


    ##
    # Calculates the capacity of a QR code in "characters" given the version, error correction
    # level and mode provided
    # @param versionNumber the version of the QR code (1 - 40)
    # @param errorCorrectLevel the error correction level (L, M, Q or H)
    # @param mode the mode of the data (NUMBER, ALPHA_NUM, BYTE, or KANJI)
    # @return the capacity of the QR code in terms of the number of characters in the given mode
    #         which can be held by the QR code, or if any of the parameters is invalid
    @staticmethod
    def capacity(versionNumber, errorCorrectLevel=QRErrorCorrectLevel.L, mode=QRMode.ALPHA_NUM):
        return QRUtil.CAPACITY_LOOKUP.get(versionNumber, {}).get(errorCorrectLevel, {}).get(mode, 0)

    ##
    # Determines the suggested QR code version to use given the amount of "characters" to store
    # with the given error correction level and character mode provided
    # @param characterCount the amount of data required to be stored
    # @param errorCorrectLevel the error correction level (L, M, Q or H)
    # @param mode the mode of the data (NUMBER, ALPHA_NUM, BYTE, or KANJI)
    # @return the suggested QR Code version number (1 - 40) to use to store the data, or -1 if
    #         there is no QR Code version which is able to hold the amount of data given
    @staticmethod
    def suggestedVersion(characterCount, errorCorrectLevel=QRErrorCorrectLevel.L, mode=QRMode.ALPHA_NUM):
        version = 0
        capacity = 0
        while True:
            version +=1
            if version > 40:
                # maximum size has been tried and it still can't hold all
                # the data - bail out!
                return -1
            capacity = QRUtil.capacity(version, errorCorrectLevel, mode)
            if capacity >= characterCount:
                # we've found one that will hold the required amount of data
                return version
        # shouldn't ever get here, but return -1 just the same
        return -1


    @staticmethod
    def getBCHTypeInfo(data):
        d = data << 10;
        while (QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G15) >= 0):
            d ^= (QRUtil.G15 << (QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G15) ) )

        return ( (data << 10) | d) ^ QRUtil.G15_MASK


    @staticmethod
    def getBCHTypeNumber(data):
        d = data << 12;
        while (QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G18) >= 0):
            d ^= (QRUtil.G18 << (QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G18) ) )
        return (data << 12) | d


    @staticmethod
    def getBCHDigit(data):
        digit = 0;
        while (data != 0):
            digit += 1
            data >>= 1
        return digit


    @staticmethod
    def getPatternPosition(versionNumber):
        return QRUtil.PATTERN_POSITION_TABLE[versionNumber - 1]


    @staticmethod
    def getMask(maskPattern, i, j):
        if maskPattern == QRMaskPattern.PATTERN000 : return (i + j) % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN001 : return i % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN010 : return j % 3 == 0
        if maskPattern == QRMaskPattern.PATTERN011 : return (i + j) % 3 == 0
        if maskPattern == QRMaskPattern.PATTERN100 : return (math.floor(i / 2) + math.floor(j / 3) ) % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN101 : return (i * j) % 2 + (i * j) % 3 == 0
        if maskPattern == QRMaskPattern.PATTERN110 : return ( (i * j) % 2 + (i * j) % 3) % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN111 : return ( (i * j) % 3 + (i + j) % 2) % 2 == 0
        raise Exception("bad maskPattern:" + maskPattern);


    @staticmethod
    def getErrorCorrectPolynomial(errorCorrectLength):
        a = QRPolynomial([1], 0);
        for i in range(errorCorrectLength):
            a = a.multiply(QRPolynomial([1, QRMath.gexp(i)], 0) )
        return a


    @staticmethod
    def getLengthInBits(mode, version):
        if 1 <= version and version < 10:
            #// 1 - 9
            if mode == QRMode.NUMBER     : return 10
            if mode == QRMode.ALPHA_NUM     : return 9
            if mode == QRMode.BYTE    : return 8
            if mode == QRMode.KANJI      : return 8
            raise Exception("mode:" + mode)
        elif (version < 27):
            #// 10 - 26
            if mode == QRMode.NUMBER     : return 12
            if mode == QRMode.ALPHA_NUM     : return 11
            if mode == QRMode.BYTE    : return 16
            if mode == QRMode.KANJI      : return 10
            raise Exception("mode:" + mode)
        elif (version < 41):
            #// 27 - 40
            if mode == QRMode.NUMBER     : return 14
            if mode == QRMode.ALPHA_NUM    : return 13
            if mode == QRMode.BYTE    : return 16
            if mode == QRMode.KANJI      : return 12
            raise Exception("mode:" + mode)
        else:
            raise Exception("version:" + version)


    @staticmethod
    def getLostPoint(qrCode):
        moduleCount = qrCode.getModuleCount();
        lostPoint = 0;
        #// LEVEL1
        for row in range(moduleCount):
            for col in range(moduleCount):
                sameCount = 0;
                dark = qrCode.isDark(row, col);
                for r in range(-1, 2):
                    if (row + r < 0 or moduleCount <= row + r):
                        continue
                    for c in range(-1, 2):
                        if (col + c < 0 or moduleCount <= col + c):
                            continue
                        if (r == 0 and c == 0):
                            continue
                        if (dark == qrCode.isDark(row + r, col + c) ):
                            sameCount+=1
                if (sameCount > 5):
                    lostPoint += (3 + sameCount - 5)
        #// LEVEL2
        for row in range(moduleCount - 1):
            for col in range(moduleCount - 1):
                count = 0;
                if (qrCode.isDark(row,     col    ) ): count+=1
                if (qrCode.isDark(row + 1, col    ) ): count+=1
                if (qrCode.isDark(row,     col + 1) ): count+=1
                if (qrCode.isDark(row + 1, col + 1) ): count+=1
                if (count == 0 or count == 4):
                    lostPoint += 3
        #// LEVEL3
        for row in range(moduleCount):
            for col in range(moduleCount - 6):
                if (qrCode.isDark(row, col)
                        and not qrCode.isDark(row, col + 1)
                        and  qrCode.isDark(row, col + 2)
                        and  qrCode.isDark(row, col + 3)
                        and  qrCode.isDark(row, col + 4)
                        and not qrCode.isDark(row, col + 5)
                        and  qrCode.isDark(row, col + 6) ):
                    lostPoint += 40
        for col in range(moduleCount):
            for row in range(moduleCount - 6):
                if (qrCode.isDark(row, col)
                        and not qrCode.isDark(row + 1, col)
                        and  qrCode.isDark(row + 2, col)
                        and  qrCode.isDark(row + 3, col)
                        and  qrCode.isDark(row + 4, col)
                        and not qrCode.isDark(row + 5, col)
                        and  qrCode.isDark(row + 6, col) ):
                    lostPoint += 40
        #// LEVEL4
        darkCount = 0;
        for col in range(moduleCount):
            for row in range(moduleCount):
                if (qrCode.isDark(row, col) ):
                    darkCount+=1
        ratio = abs(100 * darkCount / moduleCount / moduleCount - 50) / 5
        lostPoint += ratio * 10

        return lostPoint


class QRMath:

    @staticmethod
    def glog(n):
        if (n < 1):
            raise Exception("glog(" + n + ")")
        return LOG_TABLE[n];


    @staticmethod
    def gexp(n):
        while n < 0:
            n += 255
        while n >= 256:
            n -= 255
        return EXP_TABLE[n];

EXP_TABLE = [x for x in range(256)]
LOG_TABLE = [x for x in range(256)]

for i in range(8):
    EXP_TABLE[i] = 1 << i;
for i in range(8, 256):
    EXP_TABLE[i] = EXP_TABLE[i - 4] ^ EXP_TABLE[i - 5] ^ EXP_TABLE[i - 6] ^ EXP_TABLE[i - 8]
for i in range(255):
    LOG_TABLE[EXP_TABLE[i] ] = i


class QRPolynomial:

    def __init__(self, num, shift):
        if (len(num) == 0):
            raise Exception(num.length + "/" + shift)
        offset = 0
        while offset < len(num) and num[offset] == 0:
            offset += 1
        self.num = [0 for x in range(len(num)-offset+shift)]
        for i in range(len(num) - offset):
            self.num[i] = num[i + offset]

    def get(self, index):
        return self.num[index]


    def getLength(self):
        return len(self.num)


    def multiply(self, e):
        num = [0 for x in range(self.getLength() + e.getLength() - 1)];
        for i in range(self.getLength()):
            for j in range(e.getLength()):
                num[i + j] ^= QRMath.gexp(QRMath.glog(self.get(i) ) + QRMath.glog(e.get(j) ) )

        return QRPolynomial(num, 0);


    def mod(self, e):
        if (self.getLength() - e.getLength() < 0):
            return self;
        ratio = QRMath.glog(self.get(0) ) - QRMath.glog(e.get(0) )
        num = [0 for x in range(self.getLength())]
        for i in range(self.getLength()):
            num[i] = self.get(i);
        for i in range(e.getLength()):
            num[i] ^= QRMath.gexp(QRMath.glog(e.get(i) ) + ratio)
        # recursive call
        return QRPolynomial(num, 0).mod(e);


class QRRSBlock:
    RS_BLOCK_TABLE = [
        #// L
        #// M
        #// Q
        #// H
        #// 1
        [1, 26, 19],
        [1, 26, 16],
        [1, 26, 13],
        [1, 26, 9],
        #// 2
        [1, 44, 34],
        [1, 44, 28],
        [1, 44, 22],
        [1, 44, 16],
        #// 3
        [1, 70, 55],
        [1, 70, 44],
        [2, 35, 17],
        [2, 35, 13],
        #// 4
        [1, 100, 80],
        [2, 50, 32],
        [2, 50, 24],
        [4, 25, 9],
        #// 5
        [1, 134, 108],
        [2, 67, 43],
        [2, 33, 15, 2, 34, 16],
        [2, 33, 11, 2, 34, 12],
        #// 6
        [2, 86, 68],
        [4, 43, 27],
        [4, 43, 19],
        [4, 43, 15],
        #// 7
        [2, 98, 78],
        [4, 49, 31],
        [2, 32, 14, 4, 33, 15],
        [4, 39, 13, 1, 40, 14],
        #// 8
        [2, 121, 97],
        [2, 60, 38, 2, 61, 39],
        [4, 40, 18, 2, 41, 19],
        [4, 40, 14, 2, 41, 15],
        #// 9
        [2, 146, 116],
        [3, 58, 36, 2, 59, 37],
        [4, 36, 16, 4, 37, 17],
        [4, 36, 12, 4, 37, 13],
        #// 10
        [2, 86, 68, 2, 87, 69],
        [4, 69, 43, 1, 70, 44],
        [6, 43, 19, 2, 44, 20],
        [6, 43, 15, 2, 44, 16],
      # 11
      [4, 101, 81],
      [1, 80, 50, 4, 81, 51],
      [4, 50, 22, 4, 51, 23],
      [3, 36, 12, 8, 37, 13],
      # 12
      [2, 116, 92, 2, 117, 93],
      [6, 58, 36, 2, 59, 37],
      [4, 46, 20, 6, 47, 21],
      [7, 42, 14, 4, 43, 15],
      # 13
      [4, 133, 107],
      [8, 59, 37, 1, 60, 38],
      [8, 44, 20, 4, 45, 21],
      [12, 33, 11, 4, 34, 12],
      # 14
      [3, 145, 115, 1, 146, 116],
      [4, 64, 40, 5, 65, 41],
      [11, 36, 16, 5, 37, 17],
      [11, 36, 12, 5, 37, 13],
      # 15
      [5, 109, 87, 1, 110, 88],
      [5, 65, 41, 5, 66, 42],
      [5, 54, 24, 7, 55, 25],
      [11, 36, 12],
      # 16
      [5, 122, 98, 1, 123, 99],
      [7, 73, 45, 3, 74, 46],
      [15, 43, 19, 2, 44, 20],
      [3, 45, 15, 13, 46, 16],
      # 17
      [1, 135, 107, 5, 136, 108],
      [10, 74, 46, 1, 75, 47],
      [1, 50, 22, 15, 51, 23],
      [2, 42, 14, 17, 43, 15],
      # 18
      [5, 150, 120, 1, 151, 121],
      [9, 69, 43, 4, 70, 44],
      [17, 50, 22, 1, 51, 23],
      [2, 42, 14, 19, 43, 15],
      # 19
      [3, 141, 113, 4, 142, 114],
      [3, 70, 44, 11, 71, 45],
      [17, 47, 21, 4, 48, 22],
      [9, 39, 13, 16, 40, 14],
      # 20
      [3, 135, 107, 5, 136, 108],
      [3, 67, 41, 13, 68, 42],
      [15, 54, 24, 5, 55, 25],
      [15, 43, 15, 10, 44, 16],
      # 21
      [4, 144, 116, 4, 145, 117],
      [17, 68, 42],
      [17, 50, 22, 6, 51, 23],
      [19, 46, 16, 6, 47, 17],
      # 22
      [2, 139, 111, 7, 140, 112],
      [17, 74, 46],
      [7, 54, 24, 16, 55, 25],
      [34, 37, 13],
      # 23
      [4, 151, 121, 5, 152, 122],
      [4, 75, 47, 14, 76, 48],
      [11, 54, 24, 14, 55, 25],
      [16, 45, 15, 14, 46, 16],
      # 24
      [6, 147, 117, 4, 148, 118],
      [6, 73, 45, 14, 74, 46],
      [11, 54, 24, 16, 55, 25],
      [30, 46, 16, 2, 47, 17],
      # 25
      [8, 132, 106, 4, 133, 107],
      [8, 75, 47, 13, 76, 48],
      [7, 54, 24, 22, 55, 25],
      [22, 45, 15, 13, 46, 16],
      # 26
      [10, 142, 114, 2, 143, 115],
      [19, 74, 46, 4, 75, 47],
      [28, 50, 22, 6, 51, 23],
      [33, 46, 16, 4, 47, 17],
      # 27
      [8, 152, 122, 4, 153, 123],
      [22, 73, 45, 3, 74, 46],
      [8, 53, 23, 26, 54, 24],
      [12, 45, 15, 28, 46, 16],
      # 28
      [3, 147, 117, 10, 148, 118],
      [3, 73, 45, 23, 74, 46],
      [4, 54, 24, 31, 55, 25],
      [11, 45, 15, 31, 46, 16],
      # 29
      [7, 146, 116, 7, 147, 117],
      [21, 73, 45, 7, 74, 46],
      [1, 53, 23, 37, 54, 24],
      [19, 45, 15, 26, 46, 16],
      # 30
      [5, 145, 115, 10, 146, 116],
      [19, 75, 47, 10, 76, 48],
      [15, 54, 24, 25, 55, 25],
      [23, 45, 15, 25, 46, 16],
      # 31
      [13, 145, 115, 3, 146, 116],
      [2, 74, 46, 29, 75, 47],
      [42, 54, 24, 1, 55, 25],
      [23, 45, 15, 28, 46, 16],
      # 32
      [17, 145, 115],
      [10, 74, 46, 23, 75, 47],
      [10, 54, 24, 35, 55, 25],
      [19, 45, 15, 35, 46, 16],
      # 33
      [17, 145, 115, 1, 146, 116],
      [14, 74, 46, 21, 75, 47],
      [29, 54, 24, 19, 55, 25],
      [11, 45, 15, 46, 46, 16],
      # 34
      [13, 145, 115, 6, 146, 116],
      [14, 74, 46, 23, 75, 47],
      [44, 54, 24, 7, 55, 25],
      [59, 46, 16, 1, 47, 17],
      # 35
      [12, 151, 121, 7, 152, 122],
      [12, 75, 47, 26, 76, 48],
      [39, 54, 24, 14, 55, 25],
      [22, 45, 15, 41, 46, 16],
      # 36
      [6, 151, 121, 14, 152, 122],
      [6, 75, 47, 34, 76, 48],
      [46, 54, 24, 10, 55, 25],
      [2, 45, 15, 64, 46, 16],
      # 37
      [17, 152, 122, 4, 153, 123],
      [29, 74, 46, 14, 75, 47],
      [49, 54, 24, 10, 55, 25],
      [24, 45, 15, 46, 46, 16],
      # 38
      [4, 152, 122, 18, 153, 123],
      [13, 74, 46, 32, 75, 47],
      [48, 54, 24, 14, 55, 25],
      [42, 45, 15, 32, 46, 16],
      # 39
      [20, 147, 117, 4, 148, 118],
      [40, 75, 47, 7, 76, 48],
      [43, 54, 24, 22, 55, 25],
      [10, 45, 15, 67, 46, 16],
      # 40
      [19, 148, 118, 6, 149, 119],
      [18, 75, 47, 31, 76, 48],
      [34, 54, 24, 34, 55, 25],
      [20, 45, 15, 61, 46, 16]
    ]

    def __init__(self, totalCount, dataCount):
        self.totalCount = totalCount
        self.dataCount = dataCount


    @staticmethod
    def getRSBlocks(versionNumber, errorCorrectLevel):
        rsBlock = QRRSBlock.getRsBlockTable(versionNumber, errorCorrectLevel);
        if rsBlock == None:
            raise Exception("bad rs block @ versionNumber:" + versionNumber + "/errorCorrectLevel:" + errorCorrectLevel)
        length = len(rsBlock) / 3
        list = []
        for i in range(length):
            count = rsBlock[i * 3 + 0]
            totalCount = rsBlock[i * 3 + 1]
            dataCount  = rsBlock[i * 3 + 2]
            for j in range(count):
                list.append(QRRSBlock(totalCount, dataCount))

        return list;


    @staticmethod
    def getRsBlockTable(versionNumber, errorCorrectLevel):
        if errorCorrectLevel == QRErrorCorrectLevel.L:
            return QRRSBlock.RS_BLOCK_TABLE[(versionNumber - 1) * 4 + 0];
        elif errorCorrectLevel == QRErrorCorrectLevel.M:
            return QRRSBlock.RS_BLOCK_TABLE[(versionNumber - 1) * 4 + 1];
        elif errorCorrectLevel ==  QRErrorCorrectLevel.Q:
            return QRRSBlock.RS_BLOCK_TABLE[(versionNumber - 1) * 4 + 2];
        elif errorCorrectLevel ==  QRErrorCorrectLevel.H:
            return QRRSBlock.RS_BLOCK_TABLE[(versionNumber - 1) * 4 + 3];
        else:
            return None;


class QRBitBuffer:
    def __init__(self):
        self.buffer = []
        self.length = 0


    def __repr__(self):
        return ".".join([str(n) for n in self.buffer])


    def get(self, index):
        bufIndex = math.floor(index / 8)
        val = ( (self.buffer[bufIndex] >> (7 - index % 8) ) & 1) == 1
        print "get ", val
        return ( (self.buffer[bufIndex] >> (7 - index % 8) ) & 1) == 1


    def put(self, num, length):
        for i in range(length):
            self.putBit( ( (num >> (length - i - 1) ) & 1) == 1)


    def getLengthInBits(self):
        return self.length


    def putBit(self, bit):
        bufIndex = self.length // 8
        if len(self.buffer) <= bufIndex:
            self.buffer.append(0)
        if bit:
            self.buffer[bufIndex] |= (0x80 >> (self.length % 8) )
        self.length+=1