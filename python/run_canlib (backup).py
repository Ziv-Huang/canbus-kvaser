#!/usr/bin/env python
import ctypes as ct
import sys
import struct
import logging
import inspect
import csv
import os
import time
import cv2
import numpy as np
from Tkinter import *  



##### record csv
##################################################
m_timestamp = time.time()

filepath = './record/'+str(m_timestamp)+'/'
if not os.path.exists(filepath):
		os.makedirs(filepath)


fs = open(filepath+str(m_timestamp)+'.csv','w')
cvs_writer = csv.writer(fs)
cvs_writer.writerow(('time','id','data','dlc'))

##################################################

# -------------------
# Canlib constants
# -------------------

canOK = 0
canERR_PARAM = -1
canERR_NOMSG = -2
canERR_NOTFOUND = -3
canERR_NOCHANNELS = -5
canERR_TIMEOUT = -7
canERR_INVHANDLE = -10
canERR_TXBUFOFL = -13
canERR_NOCARD = -26
canERR_SCRIPT_FAIL = -39
canERR_NOT_IMPLEMENTED = -32

canOPEN_EXCLUSIVE = 0x0008
canOPEN_REQUIRE_EXTENDED = 0x0010
canOPEN_ACCEPT_VIRTUAL = 0x0020
canOPEN_OVERRIDE_EXCLUSIVE = 0x0040
canOPEN_REQUIRE_INIT_ACCESS = 0x0080
canOPEN_NO_INIT_ACCESS = 0x0100
canOPEN_ACCEPT_LARGE_DLC = 0x0200
canOPEN_CAN_FD = 0x0400
canOPEN_CAN_FD_NONISO = 0x0800

canBITRATE_1M = -1
canBITRATE_500K = -2
canBITRATE_250K = -3
canBITRATE_125K = -4
canBITRATE_100K = -5
canBITRATE_62K = -6
canBITRATE_50K = -7
canBITRATE_83K = -8
canBITRATE_10K = -9

canFD_BITRATE_500K_80P = -1000
canFD_BITRATE_1M_80P = -1001
canFD_BITRATE_2M_80P = -1002
canFD_BITRATE_4M_80P = -1003
canFD_BITRATE_8M_60P = -1004

canIOCTL_PREFER_EXT = 1
canIOCTL_PREFER_STD = 2
canIOCTL_CLEAR_ERROR_COUNTERS = 5
canIOCTL_SET_TIMER_SCALE = 6
canIOCTL_SET_TXACK = 7
canIOCTL_GET_RX_BUFFER_LEVEL = 8
canIOCTL_GET_TX_BUFFER_LEVEL = 9
canIOCTL_FLUSH_RX_BUFFER = 10
canIOCTL_FLUSH_TX_BUFFER = 11
canIOCTL_GET_TIMER_SCALE = 12
canIOCTL_SET_TXRQ = 13
canIOCTL_GET_EVENTHANDLE = 14
canIOCTL_SET_BYPASS_MODE = 15
canIOCTL_SET_WAKEUP = 16
canIOCTL_MAP_RXQUEUE = 18
canIOCTL_GET_WAKEUP = 19
canIOCTL_SET_REPORT_ACCESS_ERRORS = 20
canIOCTL_GET_REPORT_ACCESS_ERRORS = 21
canIOCTL_CONNECT_TO_VIRTUAL_BUS = 22
canIOCTL_DISCONNECT_FROM_VIRTUAL_BUS = 23
canIOCTL_SET_USER_IOPORT = 24
canIOCTL_GET_USER_IOPORT = 25
canIOCTL_SET_BUFFER_WRAPAROUND_MODE = 26
canIOCTL_SET_RX_QUEUE_SIZE = 27
canIOCTL_SET_USB_THROTTLE = 28
canIOCTL_GET_USB_THROTTLE = 29
canIOCTL_SET_BUSON_TIME_AUTO_RESET = 30
canIOCTL_GET_TXACK = 31
canIOCTL_SET_LOCAL_TXECHO = 32
canIOCTL_SET_ERROR_FRAMES_REPORTING = 33
canIOCTL_GET_CHANNEL_QUALITY = 34
canIOCTL_GET_ROUNDTRIP_TIME = 35
canIOCTL_GET_BUS_TYPE = 36
canIOCTL_GET_DEVNAME_ASCII = 37
canIOCTL_GET_TIME_SINCE_LAST_SEEN = 38
canIOCTL_GET_TREF_LIST = 39

canCHANNELDATA_CHANNEL_CAP = 1
canCHANNELDATA_TRANS_CAP = 2
canCHANNELDATA_CHANNEL_FLAGS = 3
canCHANNELDATA_CARD_TYPE = 4
canCHANNELDATA_CARD_NUMBER = 5
canCHANNELDATA_CHAN_NO_ON_CARD = 6
canCHANNELDATA_CARD_SERIAL_NO = 7
canCHANNELDATA_TRANS_SERIAL_NO = 8
canCHANNELDATA_CARD_FIRMWARE_REV = 9
canCHANNELDATA_CARD_HARDWARE_REV = 10
canCHANNELDATA_CARD_UPC_NO = 11
canCHANNELDATA_TRANS_UPC_NO = 12
canCHANNELDATA_CHANNEL_NAME = 13
canCHANNELDATA_DLL_FILE_VERSION = 14
canCHANNELDATA_DLL_PRODUCT_VERSION = 15
canCHANNELDATA_DLL_FILETYPE = 16
canCHANNELDATA_TRANS_TYPE = 17
canCHANNELDATA_DEVICE_PHYSICAL_POSITION = 18
canCHANNELDATA_UI_NUMBER = 19
canCHANNELDATA_TIMESYNC_ENABLED = 20
canCHANNELDATA_DRIVER_FILE_VERSION = 21
canCHANNELDATA_DRIVER_PRODUCT_VERSION = 22
canCHANNELDATA_MFGNAME_UNICODE = 23
canCHANNELDATA_MFGNAME_ASCII = 24
canCHANNELDATA_DEVDESCR_UNICODE = 25
canCHANNELDATA_DEVDESCR_ASCII = 26
canCHANNELDATA_DRIVER_NAME = 27
canCHANNELDATA_CHANNEL_QUALITY = 28
canCHANNELDATA_ROUNDTRIP_TIME = 29
canCHANNELDATA_BUS_TYPE = 30
canCHANNELDATA_DEVNAME_ASCII = 31
canCHANNELDATA_TIME_SINCE_LAST_SEEN = 32
canCHANNELDATA_REMOTE_OPERATIONAL_MODE = 33
canCHANNELDATA_REMOTE_PROFILE_NAME = 34

canMSG_MASK = 0x00ff
canMSG_RTR = 0x0001
canMSG_STD = 0x0002
canMSG_EXT = 0x0004
canMSG_WAKEUP = 0x0008
canMSG_NERR = 0x0010
canMSG_ERROR_FRAME = 0x0020
canMSG_TXACK = 0x0040
canMSG_TXRQ = 0x0080
canFDMSG_MASK = 0xff0000
canFDMSG_FDF = 0x010000
canFDMSG_BRS = 0x020000
canFDMSG_ESI = 0x040000
canMSGERR_MASK = 0xff00
canMSGERR_HW_OVERRUN = 0x0200
canMSGERR_SW_OVERRUN = 0x0400
canMSGERR_STUFF = 0x0800
canMSGERR_FORM = 0x1000
canMSGERR_CRC = 0x2000
canMSGERR_BIT0 = 0x4000
canMSGERR_BIT1 = 0x8000
canMSGERR_OVERRUN = 0x0600
canMSGERR_BIT = 0xC000
canMSGERR_BUSERR = 0xF800

canDRIVER_NORMAL = 4
canDRIVER_SILENT = 1
canDRIVER_SELFRECEPTION = 8
canDRIVER_OFF = 0

kvEVENT_TYPE_KEY = 1

kvSCRIPT_STOP_NORMAL = 0
kvSCRIPT_STOP_FORCED = -9

kvDEVICE_MODE_INTERFACE = 0
kvDEVICE_MODE_LOGGER = 1

ENVVAR_MAX_SIZE = 4096

kvENVVAR_TYPE_INT = 1
kvENVVAR_TYPE_FLOAT = 2
kvENVVAR_TYPE_STRING = 3


class canError(Exception):
    """Base class for exceptions raised by the canlib class

    Looks up the error text in the canlib dll and presents it together with the
    error code and the wrapper function that triggered the exception.

    """
    def __init__(self, canlib, canERR):
        self.canlib = canlib
        self.canERR = canERR
        self.fn = canlib.fn

    def __canGetErrorText(self):
        msg = ct.create_string_buffer(80)
        self.canlib.dll.canGetErrorText(self.canERR, msg, ct.sizeof(msg))
        return msg.value

    def __str__(self):
        """
        Looks up the error text in the canlib dll and presents it together
        with the error code and the wrapper function that triggered the
        exception.
        """
        return "[canError] %s: %s (%d)" % (self.fn,
                                           self.__canGetErrorText(),
                                           self.canERR)


class canNoMsg(canError):
    """Raised when no matching message was available

    """
    def __init__(self, canlib, canERR):
        self.canlib = canlib
        self.canERR = canERR

    def __str__(self):
        return "No messages available"


class canScriptFail(canError):
    """Raised when a script call failed.

    This exception represents several different failures, for example:
    - Trying to load a corrupt file or not a .txe file
    - Trying to start a t script that has not been loaded
    - Trying to load a t script compiled with the wrong version of the t
      compiler
    - Trying to unload a t script that has not been stopped
    - Trying to use an envvar that does not exist
    """
    def __init__(self, canlib, canERR):
        self.canlib = canlib
        self.canERR = canERR

    def __str__(self):
        return "Script error"


class EnvvarException(Exception):
    """Base class for exceptions related to environment variables.

    """
    pass


class EnvvarValueError(EnvvarException):
    """
    Raised when the type of the value does not match the type of the
    environment variable.

    """
    def __init__(self, envvar, type_, value):
        msg = ("invalid literal for envvar ({envvar}) with"
               " type {type_}: {value}")
        msg.format(envvar=envvar, type_=type_, value=value)
        super(EnvvarValueError, self).__init__(msg)


class EnvvarNameError(EnvvarException):
    """
    Raised when the name of the environment variable is illegal.

    """
    def __init__(self, envvar):
        msg = "envvar names must not start with an underscore: {envvar}"
        msg.format(envvar=envvar)
        super(EnvvarValueError, self).__init__(msg)


class canVersion(ct.Structure):
    """
    Class that holds CANlib version number.

    """
    _fields_ = [
        ("minor", ct.c_uint8),
        ("major", ct.c_uint8),
        ]

    def __str__(self):
        """
        Presents the version number as 'major.minor'.
        """
        return "%d.%d" % (self.major, self.minor)


class bitrateSetting(object):
    """
    Class that holds bitrate setting.

    Attributes:
        freq: Bitrate in bit/s.
        tseg1: Number of quanta from (but not including) the Sync Segment to
            the sampling point.
        tseg2: Number of quanta from the sampling point to the end of the bit.
        sjw: The Synchronization Jump Width, can be 1,2,3, or 4.
        nosamp: The number of sampling points, only 1 is supported.
        syncMode: Unsupported and ignored.

    """
    def __init__(self, freq=1000000, tseg1=4, tseg2=3, sjw=1, nosamp=1,
                 syncMode=0):
        self.freq = freq
        self.tseg1 = tseg1
        self.tseg2 = tseg2
        self.sjw = sjw
        self.nosamp = nosamp
        self.syncMode = syncMode

    def __str__(self):
        txt = "freq    : %8d\n" % self.freq
        txt += "tseg1   : %8d\n" % self.tseg1
        txt += "tseg2   : %8d\n" % self.tseg2
        txt += "sjw     : %8d\n" % self.sjw
        txt += "nosamp  : %8d\n" % self.nosamp
        txt += "syncMode: %8d\n" % self.syncMode
        return txt


# -------------------
# Canlib class
# -------------------

class canlib(object):
    """Wrapper class for the Kvaser CANlib.

    This class wraps the Kvaser CANlib dll. For more info, see the CANlib help
    files which are availible in the CANlib SDK.
    http://www.kvaser.com/developer/canlib-sdk/

    """
    def __init__(self, debug=None):
        fmt = '[%(levelname)s] %(funcName)s: %(message)s'
        if debug:
            logging.basicConfig(stream=sys.stderr,
                                level=logging.DEBUG,
                                format=fmt)
        else:
            logging.basicConfig(stream=sys.stderr,
                                level=logging.ERROR,
                                format=fmt)

        if sys.platform.startswith('win'):
            self.dll = ct.WinDLL('canlib32')
            self.dll.canInitializeLibrary()
        else:
            #self.dll = ct.CDLL('libcanlib.so')
	    self.dll = ct.CDLL('libcanlib.so.1.2.0')
        # prototypes
        self.dll.canGetVersion.argtypes = []
        self.dll.canGetVersion.restype  = ct.c_short
        self.dll.canGetVersion.errcheck = self._canErrorCheck

        self.dll.canGetNumberOfChannels.argtypes = [ct.POINTER(ct.c_int)]
        self.dll.canGetNumberOfChannels.errcheck = self._canErrorCheck

        self.dll.canGetChannelData.argtypes = [ct.c_int, ct.c_int,
                                               ct.c_void_p, ct.c_size_t]
        self.dll.canGetChannelData.errcheck = self._canErrorCheck

        self.dll.canOpenChannel.argtypes = [ct.c_int, ct.c_int]
        self.dll.canOpenChannel.errcheck = self._canErrorCheck

        self.dll.canClose.argtypes = [ct.c_int]
        self.dll.canClose.errcheck = self._canErrorCheck

        self.dll.canSetBusParams.argtypes = [ct.c_int, ct.c_long, ct.c_uint,
                                             ct.c_uint, ct.c_uint, ct.c_uint,
                                             ct.c_uint]
        self.dll.canSetBusParams.errcheck = self._canErrorCheck

        self.dll.canGetBusParams.argtypes = [ct.c_int, ct.POINTER(ct.c_long),
                                             ct.POINTER(ct.c_uint),
                                             ct.POINTER(ct.c_uint),
                                             ct.POINTER(ct.c_uint),
                                             ct.POINTER(ct.c_uint),
                                             ct.POINTER(ct.c_uint)]
        self.dll.canGetBusParams.errcheck = self._canErrorCheck

        self.dll.canSetBusParamsFd.argtypes = [ct.c_int, ct.c_long, ct.c_uint,
                                               ct.c_uint, ct.c_uint]
        self.dll.canSetBusParamsFd.errcheck = self._canErrorCheck

        self.dll.canGetBusParamsFd.argtypes = [ct.c_int, ct.POINTER(ct.c_long),
                                               ct.POINTER(ct.c_uint),
                                               ct.POINTER(ct.c_uint),
                                               ct.POINTER(ct.c_uint)]
        self.dll.canGetBusParamsFd.errcheck = self._canErrorCheck

        self.dll.canBusOn.argtypes = [ct.c_int]
        self.dll.canBusOn.errcheck = self._canErrorCheck

        self.dll.canBusOff.argtypes = [ct.c_int]
        self.dll.canBusOff.errcheck = self._canErrorCheck

        self.dll.canTranslateBaud.atgtypes = [ct.POINTER(ct.c_long),
                                              ct.POINTER(ct.c_uint),
                                              ct.POINTER(ct.c_uint),
                                              ct.POINTER(ct.c_uint),
                                              ct.POINTER(ct.c_uint),
                                              ct.POINTER(ct.c_uint)]
        self.dll.canTranslateBaud.errcheck = self._canErrorCheck

        self.dll.canWrite.argtypes = [ct.c_int, ct.c_long, ct.c_void_p,
                                      ct.c_uint, ct.c_uint]
        self.dll.canWrite.errcheck = self._canErrorCheck

        self.dll.canWriteWait.argtypes = [ct.c_int, ct.c_long,
                                          ct.c_void_p, ct.c_uint,
                                          ct.c_uint, ct.c_ulong]
        self.dll.canWriteWait.errcheck = self._canErrorCheck

        self.dll.canReadWait.argtypes = [ct.c_int, ct.POINTER(ct.c_long),
                                         ct.c_void_p,
                                         ct.POINTER(ct.c_uint),
                                         ct.POINTER(ct.c_uint),
                                         ct.POINTER(ct.c_ulong), ct.c_ulong]
        self.dll.canReadWait.errcheck = self._canErrorCheck

        try:
            self.dll.canReadSpecificSkip.argtypes = [ct.c_int, ct.c_long,
                                                     ct.c_void_p,
                                                     ct.POINTER(ct.c_uint),
                                                     ct.POINTER(ct.c_uint),
                                                     ct.POINTER(ct.c_ulong)]
            self.dll.canReadSpecificSkip.errcheck = self._canErrorCheck
        except Exception as e:
            logging.debug(str(e) + ' (Not implemented in Linux)')

        try:
            self.dll.canReadSyncSpecific.argtypes = [ct.c_int, ct.c_long,
                                                     ct.c_ulong]
            self.dll.canReadSyncSpecific.errcheck = self._canErrorCheck
        except Exception as e:
            logging.debug(str(e) + ' (Not implemented in Linux)')

        self.dll.canSetBusOutputControl.argtypes = [ct.c_int, ct.c_ulong]
        self.dll.canSetBusOutputControl.errcheck = self._canErrorCheck

        self.dll.canIoCtl.argtypes = [ct.c_int, ct.c_uint, ct.c_void_p,
                                      ct.c_uint]
        self.dll.canIoCtl.errcheck = self._canErrorCheck

        try:
            self.dll.kvReadDeviceCustomerData.argtypes = [ct.c_int, ct.c_int,
                                                          ct.c_int,
                                                          ct.c_void_p,
                                                          ct.c_size_t]
            self.dll.kvReadDeviceCustomerData.errcheck = self._canErrorCheck

            self.dll.kvFileGetCount.argtypes = [ct.c_int, ct.POINTER(ct.c_int)]
            self.dll.kvFileGetCount.errcheck = self._canErrorCheck

            self.dll.kvFileGetName.argtypes = [ct.c_int, ct.c_int, ct.c_char_p,
                                               ct.c_int]
            self.dll.kvFileGetName.errcheck = self._canErrorCheck

            self.dll.kvFileCopyFromDevice.argtypes = [ct.c_int, ct.c_char_p,
                                                      ct.c_char_p]
            self.dll.kvFileCopyFromDevice.errcheck = self._canErrorCheck

            self.dll.kvScriptSendEvent.argtypes = [ct.c_int, ct.c_int,
                                                   ct.c_int, ct.c_int,
                                                   ct.c_uint]
            self.dll.kvScriptSendEvent.errcheck = self._canErrorCheck

            self.dll.kvScriptStart.argtypes = [ct.c_int, ct.c_int]
            self.dll.kvScriptStart.errcheck = self._canErrorCheck

            self.dll.kvScriptStop.argtypes = [ct.c_int, ct.c_int, ct.c_int]
            self.dll.kvScriptStop.errcheck = self._canErrorCheck

            self.dll.kvScriptUnload.argtypes = [ct.c_int, ct.c_int]
            self.dll.kvScriptUnload.errcheck = self._canErrorCheck

            self.dll.kvScriptEnvvarOpen.argtypes = [ct.c_int, ct.c_char_p,
                                                    ct.POINTER(ct.c_int),
                                                    ct.POINTER(ct.c_int)]
            self.dll.kvScriptEnvvarOpen.restype = ct.c_int64
            self.dll.kvScriptEnvvarOpen.errcheck = self._canErrorCheck

            self.dll.kvScriptEnvvarClose.argtypes = [ct.c_int64]
            self.dll.kvScriptEnvvarClose.errcheck = self._canErrorCheck

            self.dll.kvScriptEnvvarSetInt.argtypes = [ct.c_int64, ct.c_int]
            self.dll.kvScriptEnvvarSetInt.errcheck = self._canErrorCheck

            self.dll.kvScriptEnvvarGetInt.argtypes = [ct.c_int64,
                                                      ct.POINTER(ct.c_int)]
            self.dll.kvScriptEnvvarGetInt.errcheck = self._canErrorCheck

            self.dll.kvScriptEnvvarSetFloat.argtypes = [ct.c_int64, ct.c_float]
            self.dll.kvScriptEnvvarSetFloat.errcheck = self._canErrorCheck

            self.dll.kvScriptEnvvarGetFloat.argtypes = [ct.c_int64,
                                                        ct.POINTER(ct.c_float)]
            self.dll.kvScriptEnvvarGetFloat.errcheck = self._canErrorCheck

            self.dll.kvScriptEnvvarSetData.argtypes = [ct.c_int64, ct.c_void_p,
                                                       ct.c_int, ct.c_int]
            self.dll.kvScriptEnvvarSetData.errcheck = self._canErrorCheck
            self.dll.kvScriptEnvvarGetData.argtypes = [ct.c_int64, ct.c_void_p,
                                                       ct.c_int, ct.c_int]
            self.dll.kvScriptEnvvarGetData.errcheck = self._canErrorCheck

            self.dll.kvScriptLoadFileOnDevice.argtypes = [ct.c_int, ct.c_int,
                                                          ct.c_char_p]
            self.dll.kvScriptLoadFileOnDevice.errcheck = self._canErrorCheck

            self.dll.kvScriptLoadFile.argtypes = [ct.c_int, ct.c_int,
                                                  ct.c_char_p]
            self.dll.kvScriptLoadFile.errcheck = self._canErrorCheck

            self.dll.kvDeviceSetMode.argtypes = [ct.c_int, ct.c_int]
            self.dll.kvDeviceSetMode.errcheck = self._canErrorCheck

            self.dll.kvDeviceGetMode.argtypes = [ct.c_int,
                                                 ct.POINTER(ct.c_int)]
            self.dll.kvDeviceGetMode.errcheck = self._canErrorCheck

        except Exception as e:
            logging.debug(str(e) + ' (Not implemented in Linux)')

    def __del__(self):
        self.dll.canUnloadLibrary()

    def _canErrorCheck(self, result, func, arguments):
        """Error function used in ctype calls for canlib DLL.

        """
        if result == canERR_NOMSG:
            raise canNoMsg(self, result)
        elif result == canERR_SCRIPT_FAIL:
            raise canScriptFail(self, result)
        elif result < 0:
            raise canError(self, result)
        return result

    def getVersion(self):
        """Get the CANlib version number.

        Returns the CANlib version number from the CANlib DLL currently in use.

        Args:
            None

        Returns:
            version (canVersion): Major and minor version number

        """
        self.fn = inspect.currentframe().f_code.co_name
        v = self.dll.canGetVersion()
        version = canVersion(v & 0xff, v >> 8)
        return version

    def getNumberOfChannels(self):
        """Get number of available CAN channels.

        Returns the number of available CAN channels in the computer. The
        virtual channels are included in this number.

        Args:
            None

        Returns:
            chanCount (int): Number of available CAN channels

        """
        self.fn = inspect.currentframe().f_code.co_name
        chanCount = ct.c_int()
        self.dll.canGetNumberOfChannels(chanCount)
        return chanCount.value

    def getChannelData_Name(self, channel):
        """Get the product name.

        Retrieves the product name of the device connected to channel. The name
        is returned as an ASCII string.

        Args:
            channel (int): The channel you are interested in

        Returns:
            name (string): The product name

        """
        self.fn = inspect.currentframe().f_code.co_name
        name = ct.create_string_buffer(80)
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_DEVDESCR_ASCII,
                                   ct.byref(name), ct.sizeof(name))
        buf_type = ct.c_uint * 1
        buf = buf_type()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CHAN_NO_ON_CARD,
                                   ct.byref(buf), ct.sizeof(buf))
        return "%s (channel %d)" % (name.value, buf[0])

    def getChannelData_Chan_No_On_Card(self, channel):
        """Get the channel number on the card.

        Retrieves the channel number, as numbered locally on the card, device
        connected to channel.

        Args:
            channel (int): The channel you are interested in

        Returns:
            number (int): The local channel number

        """
        self.fn = inspect.currentframe().f_code.co_name
        number = ct.c_ulong()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CHAN_NO_ON_CARD,
                                   ct.byref(number), ct.sizeof(number))
        buf_type = ct.c_uint * 1
        buf = buf_type()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CHAN_NO_ON_CARD,
                                   ct.byref(buf), ct.sizeof(buf))
        return number.value

    def getChannelData_CardNumber(self, channel):
        """Get the card number

        Retrieves the card's number in the computer. Each card type is numbered
        separately. For example, the first PCIEcan card in a machine will have
        number 0, the second PCIEcan number 1, etc.

        Args:
            channel (int): The channel you are interested in

        Returns:
            card_number (int): The device's card number

        """
        self.fn = inspect.currentframe().f_code.co_name
        buf_type = ct.c_ulong
        buf = buf_type()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CARD_NUMBER,
                                   ct.byref(buf), ct.sizeof(buf))
        return buf.value

    def getChannelData_EAN(self, channel):
        """Get EAN code

        Retrieves the EAN number for the device connected to channel. If there
        is no EAN number, "00-00000-00000-0" will be returned.

        Args:
            channel (int): The channel you are interested in

        Returns:
            ean (str): The device's EAN number

        """
        self.fn = inspect.currentframe().f_code.co_name
        buf_type = ct.c_ulong * 2
        buf = buf_type()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CARD_UPC_NO,
                                   ct.byref(buf), ct.sizeof(buf))
        (ean_lo, ean_hi) = struct.unpack('LL', buf)

        return "%02x-%05x-%05x-%x" % (ean_hi >> 12,
                                      ((ean_hi & 0xfff) << 8) | (ean_lo >> 24),
                                      (ean_lo >> 4) & 0xfffff, ean_lo & 0xf)

    def getChannelData_EAN_short(self, channel):
        """Get short EAN code

        Retrieves the short EAN number, aka product number, for the device
        connected to channel. If there is no EAN number, "00000-0" will be
        returned.

        Args:
            channel (int): The channel you are interested in

        Returns:
            ean (str): The device's shortened EAN number

        """
        self.fn = inspect.currentframe().f_code.co_name
        buf_type = ct.c_ulong * 2
        buf = buf_type()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CARD_UPC_NO,
                                   ct.byref(buf), ct.sizeof(buf))
        (ean_lo, ean_hi) = struct.unpack('LL', buf)
        return "%04x-%x" % ((ean_lo >> 4) & 0xffff, ean_lo & 0xf)

    def getChannelData_Serial(self, channel):
        """Get device serial number

        Retrieves the serial number for the device connected to channel. If the
        device does not have a serial number, 0 is returned.

        Args:
            channel (int): The channel you are interested in

        Returns:
            serial (int): The device serial number

        """
        self.fn = inspect.currentframe().f_code.co_name
        buf_type = ct.c_ulong * 2
        buf = buf_type()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CARD_SERIAL_NO,
                                   ct.byref(buf), ct.sizeof(buf))
        (serial_lo, serial_hi) = struct.unpack('LL', buf)
        # serial_hi is always 0
        return serial_lo

    def getChannelData_DriverName(self, channel):
        """Get device driver name

        Retrieves the name of the device driver (e.g. "kcany") for the device
        connected to channel. The device driver names have no special meanings
        and may change from a release to another.

        Args:
            channel (int): The channel you are interested in

        Returns:
            name (str): The device driver name

        """
        self.fn = inspect.currentframe().f_code.co_name
        name = ct.create_string_buffer(80)
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_DRIVER_NAME,
                                   ct.byref(name), ct.sizeof(name))
        return name.value

    def getChannelData_Firmware(self, channel):
        """Get device firmware version

        Retrieves the firmvare version numbers for the device connected to
        channel.

        Args:
            channel (int): The channel you are interested in

        Returns:
            major (int): The major version number
            minor (int): The minor version number
            build (int): The build number

        """
        self.fn = inspect.currentframe().f_code.co_name
        buf_type = ct.c_ushort * 4
        buf = buf_type()
        self.dll.canGetChannelData(channel,
                                   canCHANNELDATA_CARD_FIRMWARE_REV,
                                   ct.byref(buf), ct.sizeof(buf))
        (build, release, minor, major) = struct.unpack('HHHH', buf)
        return (major, minor, build)

    def openChannel(self, channel, flags=0):
        """Open CAN channel

        Retrieves a canChannel object for the given CANlib channel number using
        the supplied flags.

        Args:
            channel (int): CANlib channel number
            flags (int): Flags, a combination of the canOPEN_xxx flag values.
                Default is zero, i.e. no flags.

        Returns:
            A canChannel object created with channel and flags

        """
        self.fn = inspect.currentframe().f_code.co_name
        return canChannel(self, channel, flags)

    def translateBaud(self, freq):
        """Translate bitrate constant

        This function translates the canBITRATE_xxx constants to their
        corresponding bus parameter values.

        Args:
            freq: Any of the predefined constants canBITRATE_xxx

        Returns:
            A bitrateSetting object containing the actual values of
                frequency, tseg1, tseg2 etc.

        """
        self.fn = inspect.currentframe().f_code.co_name
        freq_p = ct.c_long(freq)
        tseg1_p = ct.c_int()
        tseg2_p = ct.c_int()
        sjw_p = ct.c_int()
        nosamp_p = ct.c_int()
        syncMode_p = ct.c_int()
        self.dll.canTranslateBaud(ct.byref(freq_p),
                                  ct.byref(tseg1_p),
                                  ct.byref(tseg2_p),
                                  ct.byref(sjw_p),
                                  ct.byref(nosamp_p),
                                  ct.byref(syncMode_p))
        rateSetting = bitrateSetting(freq=freq_p.value, tseg1=tseg1_p.value,
                                     tseg2=tseg2_p.value, sjw=sjw_p.value,
                                     nosamp=nosamp_p.value,
                                     syncMode=syncMode_p.value)
        return rateSetting

    def unloadLibrary(self):
        """Unload CANlib

        Unload canlib and relase all handles. Normally not used, but is needed
        under some circumstances to find new devices.

        Note that this will invalidate all current handles.

        """
        self.fn = inspect.currentframe().f_code.co_name
        self.dll.canUnloadLibrary()

    def initializeLibrary(self):
        """Initialize CANlib library

        This initializes the driver and must be called before any other
        function in the CANlib DLL is used. This is handled in most cases by
        the Python wrapper but if you want to trigger a re-enumeration of
        connected devices, call this function.

        Any errors encountered during library initialization will be "silent"
        and an appropriate error code will be returned later on when an API
        call that requires initialization is called.

        """
        self.fn = inspect.currentframe().f_code.co_name
        self.dll.canInitializeLibrary()

    def reinitializeLibrary(self):
        """Reinitializes the CANlib driver.

        Convenience function that calls `unloadLibrary` and `initializeLibrary`
        in succession.

        """
        self.fn = inspect.currentframe().f_code.co_name
        self.unloadLibrary()
        self.dll.canInitializeLibrary()


class canChannel(object):
    """Helper class that represents a CANlib channel.

    This class wraps the canlib class and tries to implement a more Pythonic
    interface to CANlib.

    """

    def __init__(self, canlib, channel, flags=0):
        self.canlib = canlib
        self.dll = canlib.dll
        self.index = channel
        self.canlib.fn = 'openChannel'
        self.handle = self.dll.canOpenChannel(channel, flags)
        self.envvar = envvar(self)

    def close(self):
        """Close CANlib channel

        Closes the channel associated with the handle. If no other threads are
        using the CAN circuit, it is taken off bus.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.canClose(self.handle)
        self.handle = -1

    def setBusParams(self, freq, tseg1=0, tseg2=0, sjw=0, noSamp=0,
                     syncmode=0):
        """Set bus timing parameters for classic CAN

        This function sets the bus timing parameters for the specified CAN
        controller.

        The library provides default values for tseg1, tseg2, sjw and noSamp
        when freq is specified to one of the pre-defined constants,
        canBITRATE_xxx.

        If freq is any other value, no default values are supplied by the
        library.

        If you are using multiple handles to the same physical channel, for
        example if you are writing a threaded application, you must call
        busOff() once for each handle. The same applies to busOn() - the
        physical channel will not go off bus until the last handle to the
        channel goes off bus.

        Args:
            freq: Bitrate in bit/s.
            tseg1: Number of quanta from (but not including) the Sync Segment to
                the sampling point.
            tseg2: Number of quanta from the sampling point to the end of the bit.
            sjw: The Synchronization Jump Width, can be 1,2,3, or 4.
            nosamp: The number of sampling points, only 1 is supported.
            syncMode: Unsupported and ignored.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.canSetBusParams(self.handle, freq, tseg1, tseg2, sjw,
                                 noSamp, syncmode)

    def getBusParams(self):
        """Get bus timing parameters for classic CAN

        This function retrieves the current bus parameters for the specified
        channel.

        Returns: A tuple containing:
            freq: Bitrate in bit/s.
            tseg1: Number of quanta from (but not including) the Sync Segment
                to the sampling point.
            tseg2: Number of quanta from the sampling point to the end of the
                bit.
            sjw: The Synchronization Jump Width, can be 1,2,3, or 4.
            noSamp: The number of sampling points, only 1 is supported.
            syncmode: Unsupported, always read as zero.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        freq = ct.c_long()
        tseg1 = ct.c_uint()
        tseg2 = ct.c_uint()
        sjw = ct.c_uint()
        noSamp = ct.c_uint()
        syncmode = ct.c_uint()
        self.dll.canGetBusParams(self.handle, ct.byref(freq), ct.byref(tseg1),
                                 ct.byref(tseg2), ct.byref(sjw),
                                 ct.byref(noSamp), ct.byref(syncmode))
        return (freq.value, tseg1.value, tseg2.value, sjw.value, noSamp.value,
                syncmode.value)

    def setBusParamsFd(self, freq_brs, tseg1_brs=0, tseg2_brs=0, sjw_brs=0):
        """Set bus timing parameters for BRS in CAN FD

        This function sets the bus timing parameters used in BRS (Bit rate
        switch) mode for the current CANlib channel.

        The library provides default values for tseg1_brs, tseg2_brs and
        sjw_brs when freq is specified to one of the pre-defined constants,
        canFD_BITRATE_xxx.

        If freq is any other value, no default values are supplied by the
        library.

        Args:
            freq_brs: Bitrate in bit/s.
            tseg1_brs: Number of quanta from (but not including) the Sync Segment to
                the sampling point.
            tseg2_brs: Number of quanta from the sampling point to the end of the bit.
            sjw_brs: The Synchronization Jump Width.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.canSetBusParamsFd(self.handle, freq_brs, tseg1_brs, tseg2_brs, sjw_brs)

    def getBusParamsFd(self):
        """Get bus timing parameters for BRS in CAN FD

        This function retrieves the bus current timing parameters used in BRS
        (Bit rate switch) mode for the current CANlib channel.

        The library provides default values for tseg1_brs, tseg2_brs and
        sjw_brs when freq is specified to one of the pre-defined constants,
        canFD_BITRATE_xxx.

        If freq is any other value, no default values are supplied by the
        library.

        Returns: A tuple containing:
            freq_brs: Bitrate in bit/s.
            tseg1_brs: Number of quanta from (but not including) the Sync Segment to
                the sampling point.
            tseg2_brs: Number of quanta from the sampling point to the end of the bit.
            sjw_brs: The Synchronization Jump Width.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        freq_brs = ct.c_long()
        tseg1_brs = ct.c_uint()
        tseg2_brs = ct.c_uint()
        sjw_brs = ct.c_uint()
        self.dll.canGetBusParamsFd(self.handle, ct.byref(freq_brs),
                                   ct.byref(tseg1_brs), ct.byref(tseg2_brs),
                                   ct.byref(sjw_brs))
        return (freq_brs.value, tseg1_brs.value, tseg2_brs.value,
                sjw_brs.value)

    def busOn(self):
        """Takes the specified channel on-bus.

        If you are using multiple handles to the same physical channel, for
        example if you are writing a threaded application, you must call
        busOn() once for each handle.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.canBusOn(self.handle)

    def busOff(self):
        """Takes the specified channel off-bus.

        Closes the channel associated with the handle. If no other threads are
        using the CAN circuit, it is taken off bus. The handle can not be used
        for further references to the channel.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.canBusOff(self.handle)

    # The variable name id (as used by canlib) is a built-in function in
    # Python, so we use the name id_ instead
    def write(self, id_, msg, flag=0, dlc=None):
        """Send a CAN message.

        This function sends a CAN message. Note that the message has been
        queued for transmission when this calls return. It has not necessarily
        been sent.

        If you are using the same channel via multiple handles, note that the
        default behaviour is that the different handles will "hear" each other
        just as if each handle referred to a channel of its own. If you open,
        say, channel 0 from thread A and thread B and then send a message from
        thread A, it will be "received" by thread B. This behaviour can be
        changed using canIOCTL_SET_LOCAL_TXECHO.

        The variable name id (as used by canlib) is a built-in function in
        Python, so the name id_ is used instead.

        Args:
            id_: The identifier of the CAN message to send.
            msg: An array or bytearray of the message data
            flag: A combination of message flags, canMSG_xxx. Use this
                parameter e.g. to send extended (29-bit) frames.
            dlc: The length of the message in bytes. For Classic CAN dlc can
                be at most 8, unless canOPEN_ACCEPT_LARGE_DLC is used. For
                CAN FD dlc can be one of the following 0-8, 12, 16, 20, 24,
                32, 48, 64. Optional, if omitted, dlc is calculated from the
                msg array.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        if not isinstance(msg, (bytes, str)):
            if not isinstance(msg, bytearray):
                msg = bytearray(msg)
            msg = bytes(msg)
        if dlc is None:
            dlc = len(msg)
        return self.dll.canWrite(self.handle, id_, msg, dlc, flag)

    def writeWait(self, id_, msg, flag=0, dlc=0, timeout=0):
        """Sends a CAN message and waits for it to be sent.

        This function sends a CAN message. It returns when the message is sent,
        or the timeout expires. This is a convenience function that combines
        write() and writeSync().

        Args:
            id_: The identifier of the CAN message to send.
            msg: An array or bytearray of the message data
            flag: A combination of message flags, canMSG_xxx. Use this
                parameter e.g. to send extended (29-bit) frames.
            dlc: The length of the message in bytes. For Classic CAN dlc can
                be at most 8, unless canOPEN_ACCEPT_LARGE_DLC is used. For
                CAN FD dlc can be one of the following 0-8, 12, 16, 20, 24,
                32, 48, 64. Optional, if omitted, dlc is calculated from the
                msg array.
            timeout: The timeout, in milliseconds. 0xFFFFFFFF gives an infinite
                timeout.

        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        if not isinstance(msg, (bytes, str)):
            if not isinstance(msg, bytearray):
                msg = bytearray(msg)
            msg = bytes(msg)
            
        if (dlc == 0):
            dlc = len(msg)

        self.dll.canWriteWait(self.handle, id_, msg, dlc, flag, timeout)
    def read_test(self):

	print("test")
	flag = ct.c_ulong()
	txErr = ct.c_uint()
	rxErr = ct.c_uint()
	voErr = ct.c_uint()

	_MAX_SIZE = 64
        msg = ct.create_string_buffer(_MAX_SIZE)
        id_ = ct.c_long()
        dlc = ct.c_uint()
        flag = ct.c_uint()
        time = ct.c_ulong()
	
	#self.kvDeviceSetMode(1)
	#self.kvDeviceGetMode()
	
	#self.readDeviceCustomerData()
	#print self.readSpecificSkip(0)
	#print self.dll.canReadSync(self.handle,flag)
	#print self.dll.canReadErrorCounters(self.handle,txErr,rxErr,voErr)
	#print self.dll.canReadStatus(self.handle,flag)
	#print self.getBusParams()

	
    def read(self, timeout=0):
        """Read a CAN message and metadata.

        Reads a message from the receive buffer. If no message is available,
        the function waits until a message arrives or a timeout occurs.

        Args:
            timeout (int): Timeout in milliseconds, -1 gives an infinite
                           timeout.

        Returns:
            id_ (int):    CAN identifier
            msg (bytes):  CAN data - max length 8
            dlc (int):    Data Length Code
            flag (int):   Flags, a combination of the canMSG_xxx and
                          canMSGERR_xxx values
            time (float): Timestamp from hardware
        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        # msg will be replaced by class when CAN FD is supported
        _MAX_SIZE = 64
        msg = ct.create_string_buffer(_MAX_SIZE)
        id_ = ct.c_long()
        dlc = ct.c_uint()
        flag = ct.c_uint()
        time = ct.c_ulong(0)
	

	self.dll.canReadWait(self.handle, id_, msg, dlc, flag, time, timeout)

        length = min(_MAX_SIZE, dlc.value)
        return(id_.value, bytearray(msg.raw[:length]), dlc.value, flag.value,
               time.value)

    def readDeviceCustomerData(self, userNumber=100, itemNumber=0):
        self.fn = inspect.currentframe().f_code.co_name
        buf = ct.create_string_buffer(8)
        user = ct.c_int(userNumber)
        item = ct.c_int(itemNumber)
        self.dll.kvReadDeviceCustomerData(self.handle, user, item, buf,
                                          ct.sizeof(buf))
        return struct.unpack('!Q', buf)[0]

    def readSpecificSkip(self, id_):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        # msg will be replaced by class when CAN FD is supported
        _MAX_SIZE = 64
        msg = ct.create_string_buffer(_MAX_SIZE)
        id_ = ct.c_long(id_)
        dlc = ct.c_uint()
        flag = ct.c_uint()
        time = ct.c_ulong()
        self.dll.canReadSpecificSkip(self.handle, id_, msg, dlc, flag, time)
        length = min(_MAX_SIZE, dlc.value)
        return(id_.value, bytearray(msg.raw[:length]), dlc.value, flag.value,
               time.value)

    def readSyncSpecific(self, id_, timeout=0):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        id_ = ct.c_long(id_)
        self.dll.canReadSyncSpecific(self.handle, id_, timeout)

    def scriptSendEvent(self, slotNo=0, eventType=kvEVENT_TYPE_KEY,
                        eventNo=ord('a'), data=0):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvScriptSendEvent(self.handle, ct.c_int(slotNo),
                                   ct.c_int(eventType), ct.c_int(eventNo),
                                   ct.c_uint(data))

    def setBusOutputControl(self, drivertype=canDRIVER_NORMAL):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.canSetBusOutputControl(self.handle, drivertype)

    def ioCtl_flush_rx_buffer(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.canIoCtl(self.handle, canIOCTL_FLUSH_RX_BUFFER, None, 0)

    def ioCtl_set_timer_scale(self, scale):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        scale = ct.c_long(scale)
        self.dll.canIoCtl(self.handle, canIOCTL_SET_TIMER_SCALE,
                          ct.byref(scale), ct.sizeof(scale))

    def getChannelData_Name(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_Name(self.index)

    def getChannelData_Chan_No_On_Card(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_Chan_No_On_Card(self.index)

    def getChannelData_CardNumber(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_CardNumber(self.index)

    def getChannelData_EAN(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_EAN(self.index)

    def getChannelData_EAN_short(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_EAN_short(self.index)

    def getChannelData_Serial(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_Serial(self.index)

    def getChannelData_DriverName(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_DriverName(self.index)

    def getChannelData_Firmware(self):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        return self.canlib.getChannelData_Firmware(self.index)

    def scriptStart(self, slot):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvScriptStart(self.handle, slot)

    def scriptStop(self, slot, mode=kvSCRIPT_STOP_NORMAL):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvScriptStop(self.handle, slot, mode)

    def scriptUnload(self, slot):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvScriptUnload(self.handle, slot)

    def scriptLoadFileOnDevice(self, slot, localFile):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvScriptLoadFileOnDevice(self.handle, slot,
                                          ct.c_char_p(localFile))

    def scriptLoadFile(self, slot, filePathOnPC):
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvScriptLoadFile(self.handle, slot, ct.c_char_p(filePathOnPC))

    def scriptEnvvarOpen(self, name):
        envvarType = ct.c_int()
        envvarSize = ct.c_int()
        envHandle = self.dll.kvScriptEnvvarOpen(self.handle, ct.c_char_p(name),
                                                ct.byref(envvarType),
                                                ct.byref(envvarSize))
        return envHandle, envvarType.value, envvarSize.value

    def scriptEnvvarClose(self, envHandle):
        self.dll.kvScriptEnvvarClose(ct.c_int64(envHandle))

    def scriptEnvvarSetInt(self, envHandle, value):
        value = int(value)
        self.dll.kvScriptEnvvarSetInt(ct.c_int64(envHandle), ct.c_int(value))

    def scriptEnvvarGetInt(self, envHandle):
        envvarValue = ct.c_int()
        self.dll.kvScriptEnvvarGetInt(ct.c_int64(envHandle),
                                      ct.byref(envvarValue))
        return envvarValue.value

    def scriptEnvvarSetFloat(self, envHandle, value):
        value = float(value)
        self.dll.kvScriptEnvvarSetFloat(ct.c_int64(envHandle),
                                        ct.c_float(value))

    def scriptEnvvarGetFloat(self, envHandle):
        envvarValue = ct.c_float()
        self.dll.kvScriptEnvvarGetFloat(ct.c_int64(envHandle),
                                        ct.byref(envvarValue))
        return envvarValue.value

    def scriptEnvvarSetData(self, envHandle, value, envSize):
        self.dll.kvScriptEnvvarSetData(ct.c_int64(envHandle),
                                       ct.c_char_p(value), 0,
                                       ct.c_int(envSize))

    def scriptEnvvarGetData(self, envHandle, envSize):
        envvarValue = ct.create_string_buffer(envSize)
        self.dll.kvScriptEnvvarGetData(ct.c_int64(envHandle),
                                       ct.byref(envvarValue), 0,
                                       ct.c_int(envSize))
        return envvarValue.value

    def fileGetCount(self):
        """Get the number of files on the device.

        Returns:
            count (int): The number of files.
        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        count = ct.c_int()
        self.dll.kvFileGetCount(self.handle, ct.byref(count))
        return count.value

    def fileGetName(self, fileNo):
        """Get the name of the file with the supplied number.

        Args:
            fileNo (int): The number of the file.

        Returns:
            fileName (string): The name of the file.
        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        fileName = ct.create_string_buffer(50)
        self.dll.kvFileGetName(self.handle, ct.c_int(fileNo), fileName,
                               ct.sizeof(fileName))
        return fileName.value

    def fileCopyToDevice(self, hostFileName, deviceFileName):
        """Copy an arbitrary file from the host to the device.

        Args:
            hostFileName (string):   The target host file name.
            deviceFileName (string): The device file name.
        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvFileCopyToDevice(self.handle, hostFileName,
                                    deviceFileName)

    def fileCopyFromDevice(self, deviceFileName, hostFileName):
        """Copy an arbitrary file from the device to the host.

        Args:
            deviceFileName (string): The device file name.
            hostFileName (string):   The target host file name.
        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvFileCopyFromDevice(self.handle, deviceFileName,
                                      hostFileName)

    def kvDeviceSetMode(self, mode):
        """Set the current device's mode.

        Note: The mode is device specific, which means that not all modes are
        implemented in all products.

        Args:
            mode (int): One of the kvDEVICE_MODE_xxx constants, defining which
                        mode to use.
        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        self.dll.kvDeviceSetMode(self.handle, ct.c_int(mode))

    def kvDeviceGetMode(self):
        """Read the current device's mode.

        Note: The mode is device specific, which means that not all modes are
        implemented in all products.

        Returns:
            mode (int): One of the kvDEVICE_MODE_xxx constants, indicating
                        which mode is in use.
        """
        self.canlib.fn = inspect.currentframe().f_code.co_name
        mode = ct.c_int()
        self.dll.kvDeviceGetMode(self.handle, ct.byref(mode))
        return mode.value


class envvar(object):
    class Attrib(object):
        def __init__(self, handle=None, type_=None, size=None):
            self.handle = handle
            self.type_ = type_
            self.size = size

    def __init__(self, channel):
        self.__dict__['_channel'] = channel
        self.__dict__['_attrib'] = {}

    def _ensure_open(self, name):
        assert not name.startswith('_'), ("envvar names must not start"
                                          " with an underscore: %s" % name)
        # We just check the handle here
        if name not in self.__dict__['_attrib']:
            self._attrib[name] = envvar.Attrib(*self._channel.scriptEnvvarOpen(name))

    def __getattr__(self, name):
        self._ensure_open(name)
        handle = self._attrib[name].handle
        if self._attrib[name].type_ == kvENVVAR_TYPE_INT:
            value = self._channel.scriptEnvvarGetInt(handle)
        elif self._attrib[name].type_ == kvENVVAR_TYPE_FLOAT:
            value = self._channel.scriptEnvvarGetFloat(handle)
        elif self._attrib[name].type_ == kvENVVAR_TYPE_STRING:
            size = self._attrib[name].size
            value = self._channel.scriptEnvvarGetData(handle, size)
        else:
            msg = "getting is not implemented for type {type_}"
            msg = msg.format(type_=self._attrib[name].type_)
            raise TypeError(msg)
        return value

    def __setattr__(self, name, value):
        self._ensure_open(name)
        handle = self._attrib[name].handle
        if self._attrib[name].type_ == kvENVVAR_TYPE_INT:
            value = self._channel.scriptEnvvarSetInt(handle, value)
        elif self._attrib[name].type_ == kvENVVAR_TYPE_FLOAT:
            value = self._channel.scriptEnvvarSetFloat(handle, value)
        elif self._attrib[name].type_ == kvENVVAR_TYPE_STRING:
            value = str(value)
            size = self._attrib[name].size
            value = self._channel.scriptEnvvarSetData(handle, value, size)
        else:
            msg = "setting is not implemented for type {type_}"
            msg = msg.format(type_=self._attrib[name].type_)
            raise TypeError(msg)


############################################################################################

########################
#                      #
#                      #
#                      #
########################

def mode_selection():
	print "receive info : 1"
	print "control car : 2"
	mode = input("mode : ")

	if(mode == 1):
		recv_canlib()
	elif(mode == 2):
		command_cv()
		#command = UI_command()
		#command.run_loop()
	else:
		print "\n###error###\n"
		print "please enter 1 or 2 to choose mode"
		mode_selection()


######################### command opencv 

def convert_2complement_hex(data,size):
	# + -
	# input:10 -> 2 -> 2's -> 16
	
	if data>=0:
		return hex(data)
	else:
		data=data*-1
		buf = bin(data)[2:].zfill(size)

	
		tmp=str()
		tmp=tmp+'0b'
		for i in range(size):
			if(buf[i]=='0'):tmp = tmp+'1'
			elif(buf[i]=='1'):tmp = tmp+'0'
		#print tmp
		#print hex(int(tmp,2))
		return hex(int(tmp,2))


def command_cv():

	"""
	########################
	#open kvaser
	
	cl = canlib()
	channels = cl.getNumberOfChannels()
	
	#Firmware : 4,3,239
	#print "Firmware : ",cl.getChannelData_Firmware(0)
	#cl.initializeLibrary()

    	print("canlib version: %s" % cl.getVersion())
	print("have %d channels" % channels) 

    	if len(sys.argv) != 2:
        	print("Please enter channel, example: %s 3\n" % sys.argv[0])
        	for ch in range(0, channels):
        	    try:
        	        print("%d. %s (%s / %s)" % (ch, cl.getChannelData_Name(ch),
        	                                    cl.getChannelData_EAN(ch),
        	                                    cl.getChannelData_Serial(ch)))
        	    except (canError) as ex:
        	        print(ex)
        	sys.exit()

    	ch = int(sys.argv[1])
    	if ch >= channels:
        	print("Invalid channel number")
        	sys.exit()

    	try:
        	#ch1 = cl.openChannel(ch, canOPEN_ACCEPT_VIRTUAL)
		ch1 = cl.openChannel(ch, canOPEN_CAN_FD)
        	print("Using channel: %s, EAN: %s" % (ch1.getChannelData_Name(),
                                              ch1.getChannelData_EAN()))

        	ch1.setBusOutputControl(canDRIVER_NORMAL)	

        	ch1.setBusParams(canBITRATE_500K)
        	ch1.busOn()
    	except (canError) as ex:
        	print(ex)

	#open kvaser
	########################
	"""
	






	#show
	#ret,frame = cap.read()
	
	#save
	#ret,ori = cap.read()
	
	#info
	infoimg = np.zeros((400,500),np.uint8)
	cv2.namedWindow('info')


	#print data on image
	#sp=frame.shape
	sp=infoimg.shape
	height = sp[0]
	width = sp[1]
	font_point = height-10
	_color = (255,255,255)
	


	



	#key_event	
	key_w = 1048695
	key_s = 1048691
	key_a = 1048673
	key_d = 1048676

	key_space = 1048608
	key_esc = 1048603
	key_up = 1113938
	key_down = 1113940

	key_0 = 1114032
	key_1 = 1114033
	key_2 = 1114034

	key_o = 1048687
	key_p = 1048688
	

	accelerator=0
	brake=0
	s_angle=0
	shift=0
	light='0b00000000'
	light_l='off'
	light_r='off'

	msgId=None
	msg=None

	font2 = cv2.FONT_HERSHEY_SIMPLEX
	
	
	#show video
	#cv2.imshow('frame',frame)
	#cv2.imshow('ori',ori)
	#cv2.imwrite(filepath+str(m_timestamp)+'.png',ori)


	key_event=None


	#brake 0x0A 1 byte (0~255)
	#steering angle 0x0B 2 bytes (+-700)
	#accelerator 0x0C 1 byte (0~255)
	#shift 0x0D 1 byte (0:N 1:R 2:F)
	#light 0x0E 1 byte (off/on  bit[1]:left, bit[2]:right)




	#########################################################

	########error!!! when you brake, need to ch1.write() accelerator's value=0
	########error!!! initial needs to ch1.write() all id's value = 0
	while True:

		msg = None
		msgId = None

		infoimg = np.zeros((400,500),np.uint8)
		time_ = time.time()
		st = time.localtime(time_)
		cv2.putText(infoimg,time.strftime('%Y-%m-%d %H:%M:%S',st)
			,(10,20),font2,0.5,_color,1,16)
		

		cv2.putText(infoimg,'accelerator: '+str(accelerator)
			,(10,font_point-15*5),font2,0.5,_color,1,16)
	
		cv2.putText(infoimg,'brake: '+str(brake)
			,(10,font_point-15*4),font2,0.5,_color,1,16)
	
		cv2.putText(infoimg,'steering angle: '+str(s_angle)
			,(10,font_point-15*3),font2,0.5,_color,1,16)
	
		cv2.putText(infoimg,'shift: '+str(shift)
			,(10,font_point-15*2),font2,0.5,_color,1,16)
		cv2.putText(infoimg,'light left/right: '+str(light_l)+'/'+str(light_r)
			,(10,font_point-15),font2,0.5,_color,1,16)


		
		
		cv2.imshow('info',infoimg)
		key_event = cv2.waitKey(1)


		
		#if key_event!=-1:
		#	print key_event
		
		
		#accelerator
		if key_event==key_w:
			accelerator=accelerator+1
			########safe
			if accelerator>10:
				accelerator=10
			msgId = 0x0C
			msg = hex(accelerator)
		elif key_event==key_s:
			accelerator=accelerator-1
			if accelerator<0:
				accelerator=0
			msgId = 0x0C
			msg = hex(accelerator)

		#angle
		elif key_event==key_a:
			s_angle=s_angle+1
			########safe
			if s_angle>=50: s_angle=50
			#if s_angle>=700: s_angle=700
			msgId = 0x0B
			#msg = hex(s_angle)
			msg = convert_2complement_hex(s_angle,16)
			#print '##########'
			#print s_angle
			#print msg
		elif key_event==key_d:
			s_angle=s_angle-1
			########safe
			if s_angle<=-50: s_angle=-50
			#if s_angle<=-700: s_angle=-700
			msgId = 0x0B
			#msg = hex(s_angle)			
			msg = convert_2complement_hex(s_angle,16)
			#print '##########'
			#print s_angle
			#print msg
			

		#brake
		elif key_event==key_up:
			brake=brake+1
			########safe
			if brake>100: brake=100
			#if brake>255: brake=255
			accelerator=0
			msgId = 0x0A
			msg = hex(brake)
		elif key_event==key_down:
			brake=brake-1
			if brake<0: brake=0
			msgId = 0x0A
			msg = hex(brake)

		#shift
		elif key_event==key_0:
			shift = 0
			msgId = 0x0D
			msg = hex(shift)
		elif key_event==key_1:
			shift = 1
			msgId = 0x0D
			msg = hex(shift)
		elif key_event==key_2:
			shift = 2
			msgId = 0x0D
			msg = hex(shift)

		#light
		### what is the input value about light??? 
		elif key_event==key_o:
			tmp = str()
			for i in range(len(light)):
				# bit 1 for left light  0b0'0'000000
				if i == 3:
					if light_l == 'off':
						light_l='on'
						tmp = tmp+'1'
					elif light_l == 'on':	
						light_l='off'
						tmp = tmp+'0'
				else: tmp = tmp+light[i]
	
			light = tmp
			msgId = 0x0E
			msg = hex(int(light,2))
		elif key_event==key_p:
			tmp = str()
			for i in range(len(light)):
				# bit 2 for left light  0b00'0'00000
				if i == 4:
					if light_r == 'off':
						light_r='on'
						tmp = tmp+'1'
					elif light_r == 'on':	
						light_r='off'
						tmp = tmp+'0'
				else: tmp = tmp+light[i]
	
			light = tmp
			msgId = 0x0E
			msg = hex(int(light,2))
	
		#initial
		elif key_event==key_esc:
			accelerator=0
			brake=0
			s_angle=0
			shift=0
			light='0b00000000'
			light_l='off'
			light_r='off'
		
		
		if msgId!=None:print msgId,':',msg
		##########################################
		#send message
		#ex: msg[2:]='0101' msg='0x0101'
		"""
		if msgId!=None: 
			state = ch1.write(msgId, msg[2:], canMSG_EXT)	
			if state!=canOK: print "send error!!!"	
		"""
		##########################################

	#########################################################

	#if(cap.isOpened()==False):
	#	print("video is not found")



"""
class UI_command(object):
  

	def __init__(self):
        	self.enter = None
		self.cl = canlib()
		self.channels = self.cl.getNumberOfChannels()
		
		self.accelerator=0
		self.brake=0
		self.s_angle=0
		self.shift=0
		self.light=0
	
		
    		print("canlib version: %s" % self.cl.getVersion())
		print("have %d channels" % self.channels) 

	    	if len(sys.argv) != 2:
			print("Please enter channel, example: %s 3\n" % sys.argv[0])
			for ch in range(0, self.channels):
			    try:
			        print("%d. %s (%s / %s)" % (self.ch, self.cl.getChannelData_Name(self.ch),
			                                    self.cl.getChannelData_EAN(self.ch),
			                                   self.cl.getChannelData_Serial(self.ch)))
			    except (canError) as ex:
			        print(ex)
			sys.exit()

	    	self.ch = int(sys.argv[1])
	    	if self.ch >= self.channels:
			print("Invalid channel number")
			sys.exit()

	    	try:
			#ch1 = cl.openChannel(ch, canOPEN_ACCEPT_VIRTUAL)
			self.ch1 = self.cl.openChannel(self.ch, canOPEN_CAN_FD)
			print("Using channel: %s, EAN: %s" % (self.ch1.getChannelData_Name(),
		                                      self.ch1.getChannelData_EAN()))

			self.ch1.setBusOutputControl(canDRIVER_NORMAL)	

			self.ch1.setBusParams(canBITRATE_500K)
			self.ch1.busOn()
	    	except (canError) as ex:
			print(ex)

		

	def key(self,event):
		#print "pressed", repr(event.keycode)
		self.enter = event.keycode
		self.command()
	def callback(self,event):
		self.frame.focus_set()
		#print "clicked at", event.x, event.y  


	###################################################3
	##### not finishing command
	def command(self):

		#up = 111
		#left = 113
		#down = 116
		#right = 114
		#space = 65

		#w = 25
		#a = 38
		#s = 39
		#d = 40

		#nine
		#0 = 90 for N
		#1 = 87 for R
		#2 = 88 for F

		#esc = 9


		#brake 0x0A 1 byte (0~255)
		#steering angle 0x0B 2 bytes (+-)
		#accelerator 0x0C 1 byte (0~255)
		#shift 0x0D 1 byte (0:N 1:R 2:F)
		#light 0x0E 1 byte (off/on  bit[1]:left, bit[2]:right)

		#self.ch1.write(in_msgId, in_msg, in_flg)

		#self.accelerator=0
		#self.brake=0
		#self.s_angle=0
		#self.shift=0
		#self.light=0

		msgId=None
		msg=None

		if(self.enter == 25):
			if(self.accelerator<=255):
				self.accelerator=self.accelerator+1


			if(self.accelerator>5):
				print "too fast!!!!!!"
				self.accelerator = 5

			self.brake=0
			msgId = 0x0C
			msg = hex(self.accelerator)
			print "accelerator:",int(msg,16)

		elif(self.enter == 39):
			if(self.accelerator>0):
				self.accelerator=self.accelerator-1
			msgId = 0x0C
			msg = hex(self.accelerator)
			print "accelerator:",int(msg,16)

		elif(self.enter == 38):
			if(self.s_angle<=700):
				self.s_angle=self.s_angle+1
			msgId = 0x0B
			msg = hex(self.s_angle)
			print "angle:",int(msg,16)
	
		elif(self.enter == 40):
			if(self.s_angle>=-700):
				self.s_angle=self.s_angle-1
			msgId = 0x0B
			msg = hex(self.s_angle)
			print "angle:",int(msg,16)

		elif(self.enter == 65):
			if(self.accelerator<=255):
				self.brake = self.brake+1
			self.accelerator = 0
			msgId = 0x0A
			msg = hex(self.brake)
			self.ch1.write(0x0C, 0, canMSG_EXT)
			print "brake:",int(msg,16)

		elif(self.enter == 90):
			self.shift=0
			msgId = 0x0D
			msg = hex(self.shift)
			print "shift:",int(msg,16)

		elif(self.enter == 87):
			self.shift=1
			msgId = 0x0D
			msg = hex(self.shift)
			print "shift:",int(msg,16)

		elif(self.enter == 88):
			self.shift=2
			msgId = 0x0D
			msg = hex(self.shift)
			print "shift:",int(msg,16)




		

		self.label5.pack(side='bottom')
		self.label4.pack(side='bottom')
		self.label3.pack(side='bottom')
		self.label2.pack(side='bottom')
		self.label1.pack(side='bottom')

		#elif(self.enter == 9):
		#	return
		
		

		###initialization
		self.ch1.write(0x0A, 0, canMSG_EXT)
		self.ch1.write(0x0B, 0, canMSG_EXT)
		self.ch1.write(0x0C, 0, canMSG_EXT)
	
	def run_loop(self):

	  	print("control car...")
		root = Tk()  
		  
	

		  
		self.frame = Frame(root, width=500, height=500)  
		self.frame.bind("<Key>", self.key)  
		self.frame.bind("<Button-1>", self.callback)  
		self.frame.pack_propagate(False)		
		self.frame.pack()  
		

		
		self.label1=Label(self.frame,text='accelerator:'+str(self.accelerator))				  
		self.label2=Label(self.frame,text='brake:'+str(self.brake))
		self.label3=Label(self.frame,text='steering angle:'+str(self.s_angle))
		self.label4=Label(self.frame,text='shift:'+str(self.shift))
		self.label5=Label(self.frame,text='light:'+str(self.light))

		

		root.mainloop()  
"""

		


######################### receive

def convert_2complement_dec(data,size):
	# + -
	# input:10 -> 2 -> 2's -> 10
	
	buf = bin(data)[2:].zfill(size)

	if(buf[0]=='0'):
		return int(buf[1:],2)
	elif(buf[0]=='1'):
		tmp=str()
		for i in range(size):
			if(buf[i]=='0'):tmp = tmp+'1'
			elif(buf[i]=='1'):tmp = tmp+'0'
		return (int(tmp[1:],2)+1)*-1
	



	
def write_csv(m_timestamp,msgId,tmp,dlc):
	
	cvs_writer.writerow((m_timestamp,msgId,tmp,dlc))			
		

def recv_mapping(msgId,msg,dlc):

	#CAN table.xlsx

	# 16 -> 10 -> 2.zfill()	
	m_timestamp = time.time()
	tmp = None
	for i in range(dlc):
		msg[i] = (msg[i]) % 256
		tmp = ( ''.join('{:02x}'.format(x) for x in msg))
	
	if msgId == 0x14:
		#Driver's operation info
		print "info : ",tmp
	elif msgId == 0x15:
		#Brake depth 8 bits
		#tmp0 = int(tmp[:2],16)
		#tmp1 = int(tmp[2:],16)
		print "Brake : ",tmp
	
	elif msgId == 0x16:
		#Steering angle 16 bits in front of 32 bits
		# +:left   -:right
		#tmp = 2 complement's
		tmp1 = tmp[0:4]
		tmp1 = int(tmp1,16)
		tmp1 = convert_2complement_dec(tmp1,16)

		
		print "Steering angle : ",tmp1
	
	elif msgId == 0x17:
		#Speed 16 bits
		# value*10
		tmp = int(tmp[:2],16)*10
		print "Speed : ",tmp
	
	elif msgId == 0x18:
		#control mode 8 bits
		# 0:hand 1:auto 2:VCU mode
		print "control mode : ",tmp
	
	elif msgId == 0x19:
		#Accelerator depression 8 bits
		tmp = int(tmp,16)
		print "Accelerator depression : ",tmp
	
	elif msgId == 0x1A:
		#Shift position 8 bits
		# 0:N 1:R 2:F
		print "Shift position : ",tmp
	
	
	#elif msgId == 0x???: 
		#for Hydraulic brake

	#else : print "##nothing##"
	

	
	write_csv(m_timestamp,msgId,tmp,dlc)
		


def recv_canlib():
	cl = canlib()
	channels = cl.getNumberOfChannels()
	
	#Firmware : 4,3,239
	#print "Firmware : ",cl.getChannelData_Firmware(0)
	#cl.initializeLibrary()

    	print("canlib version: %s" % cl.getVersion())
	print("have %d channels" % channels) 

    	if len(sys.argv) != 2:
        	print("Please enter channel, example: %s 3\n" % sys.argv[0])
        	for ch in range(0, channels):
        	    try:
        	        print("%d. %s (%s / %s)" % (ch, cl.getChannelData_Name(ch),
        	                                    cl.getChannelData_EAN(ch),
        	                                    cl.getChannelData_Serial(ch)))
        	    except (canError) as ex:
        	        print(ex)
        	sys.exit()

    	ch = int(sys.argv[1])
    	if ch >= channels:
        	print("Invalid channel number")
        	sys.exit()

    	try:
        	#ch1 = cl.openChannel(ch, canOPEN_ACCEPT_VIRTUAL)
		ch1 = cl.openChannel(ch, canOPEN_CAN_FD)
        	print("Using channel: %s, EAN: %s" % (ch1.getChannelData_Name(),
                                              ch1.getChannelData_EAN()))

        	ch1.setBusOutputControl(canDRIVER_NORMAL)	

        	ch1.setBusParams(canBITRATE_500K)
        	ch1.busOn()
    	except (canError) as ex:
        	print(ex)

	


	
	"""
	in_msgId = 0x0D
	in_msg = 0x01
	in_flg = canMSG_EXT
	ch1.write(in_msgId, in_msg, in_flg)
	"""

	
	############################################
	###read and write
	print("#############################################################")
    	switch = 1
	if switch == 1:
		while True:
			try:

				
			    msgId, msg, dlc, flg, time = ch1.read()
			    #msgId, msg, dlc, flg, time =  ch1.readSpecificSkip(0)
			    #ch1.read_test()
			    flag = 1
			    if flag == 1:

				    recv_mapping(msgId,msg,dlc)
				    #ch1.write(in_msgId, in_msg, in_flg)
				    
				    
				    #print("id:%9d  time:%9d  flg:0x%02x  dlc:%d  msg:%s" % (msgId, time, flg, dlc, msg))
				    
				    #for i in range(dlc):
				    #	msg[i] = (msg[i]+1) % 256
				    #	print(msg, ''.join('{:02x}'.format(x) for x in msg))
				    
			except (canNoMsg) as ex:
			    None
			except (canError) as ex:
			    print(ex)


	###read and write
	############################################
	
	


    	ch1.busOff()
    	ch1.close()

if __name__ == '__main__':
	mode_selection()

	

    
