import canlib

def setUpChannel(channel=0,
                 openFlags=canlib.canOPEN_ACCEPT_VIRTUAL,
                 bitrate=canlib.canBITRATE_500K,
                 bitrateFlags=canlib.canDRIVER_NORMAL):
    cl = canlib.canlib()
    ch = cl.openChannel(channel, openFlags)
    print("Using channel: %s, EAN: %s" % (ch.getChannelData_Name(),
                                          ch.getChannelData_EAN()))
    ch.setBusOutputControl(bitrateFlags)
    ch.setBusParams(bitrate)
    ch.busOn()
    return ch


def tearDownChannel(ch):
    ch.busOff()
    ch.close()

cl = canlib.canlib()
print("canlib version: %s" % cl.getVersion())


channel_0 = 0
channel_1 = 1
ch0 = setUpChannel(channel=0)
ch1 = setUpChannel(channel=1)


msgId = 100
msg = [1, 2, 3, 4]
flg = canlib.canMSG_EXT
#ch1.write(msgId, msg, flg)
print('#################################')
while True:
    try:
        (msgId, msg, dlc, flg, time) = ch0.read()
        data = ''.join(format(x, '02x') for x in msg)
        print("time:%9d id:%9d  flag:0x%02x  dlc:%d  data:%s" %
              (time, msgId, flg, dlc, data))
        #break
    except (canlib.canNoMsg) as ex:
        None
    except (canlib.canError) as ex:
        print(ex)

tearDownChannel(ch0)
tearDownChannel(ch1)

