
import pexpect
import time

LIGHT01 = "20:C3:8F:8D:8C:9E"
VALUE = ["00000000", "FF000000", "00FF0000", "0000FF00", "000000FF", "00000000"];


child = pexpect.spawn("gatttool -I")

child.sendline("connect {0}".format(LIGHT01))
child.expect("Connection successful", timeout=5)
print ("Connected to the light!")
while True:
	for i in range(6):
		child.sendline("char-write-req 0x0031 {0}".format(VALUE[i]))
		child.expect("Characteristic value was written successfully", timeout=5)
		time.sleep(1);

child.sendline("disconnect")

child.close()

print ("Light Turned OFF")

