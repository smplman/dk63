import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x0C45, idProduct=0x766B)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# if dev.is_kernel_driver_active(0):
#     try:
#         dev.detach_kernel_driver(0)
#         print "kernel driver detached"
#     except usb.core.USBError as e:
#         sys.exit("Could not detach kernel driver: ")
# else:
#         print "no kernel driver attached"

# for cfg in dev:
#   for intf in cfg:
#     if dev.is_kernel_driver_active(intf.bInterfaceNumber):
#       try:
#         dev.detach_kernel_driver(intf.bInterfaceNumber)
#       except usb.core.USBError as e:
#         sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(
#             intf.bInterfaceNumber, str(e)))

dev.reset()

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# endpoint_in = dev[0][(0, 0)][0]
# endpoint_out = dev[0][(0, 0)][1]
# print ("endpoint_out",endpoint_out)
# print ("endpoint_in",endpoint_in)

# dev.ctrl_transfer(0x21, 0x09, 0x0200, 0x0000, 0x0001)
endpoint = dev[0][(0, 0)][0]
attempts = 10
data = None
# while data is None and attempts > 0:
while True:
    try:
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        print data
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            attempts -= 1
            continue

print data

# # get an endpoint instance
# cfg = dev.get_active_configuration()
# intf = cfg[(0,0)]

# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_OUT)

# assert ep is not None

# # write the data
# ep.write('test')