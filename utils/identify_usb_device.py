import libusb_package

first = []
second = []

for dev in libusb_package.find(find_all=True):
    first.append(dev)

input("unplug the device and press enter")
for dev in libusb_package.find(find_all=True):
    second.append(dev)

unplugged = list(set(first) - set(second))
for dev in unplugged:
    print(unplugged)

