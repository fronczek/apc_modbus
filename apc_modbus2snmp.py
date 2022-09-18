#!/usr/bin/python3
import sys
import os
import argparse
from pyModbusTCP.client import ModbusClient

#if os.getenv('USER') != 'Debian-snmp':
#    sys.stderr.write("Not running as Debian-snmp, exiting...\n")
#    sys.exit(1)

# ADD below line to your /etc/snmp/snmpd.conf
# pass    .1.3.6.1.4.1.318                     /usr/bin/python3 /opt/apc_modbus_ups.py

# test with:
# sudo -u Debian-snmp ./apc_modbus_ups.py -v;grep -E ".*" /tmp/ups*.txt --color=always

# or without sudo, first disable fs.protected_regular:
# echo 0 > /proc/sys/fs/protected_regular
# sysctl fs.protected_regular=0

parser = argparse.ArgumentParser(description='APC Modbus helper')
parser.add_argument("-o", required=False, help="APC UPS IP", default="172.16.10.4")
parser.add_argument("-p", required=False, help="APC UPS port", default=502)
parser.add_argument("-u", required=False, help="APC UPS UnitID", default=1)
parser.add_argument("-g", required=False, help="needed by pass PROG -g", default="")
parser.add_argument("-n", required=False, help="needed by pass PROG -n", default="")
parser.add_argument("-w", required=False, help="workdir writeable by snmp", default="/tmp/")
parser.add_argument("-x", required=False, help="var test name")
parser.add_argument("-v", action="count", help="verbose", default=0)
args = parser.parse_args()

ups_BasicStateOutputState = "0000000000000000000000000000000000000000000000000000000000000000"

def f_upsBasicStateOutputState(flag, value):
        global ups_BasicStateOutputState
        position = flag - 1
        ups_BasicStateOutputState = ups_BasicStateOutputState[:position] + str(value) + ups_BasicStateOutputState[position+1:]
        return ups_BasicStateOutputState

def save_var(filename, content):
    f = open(args.w + "/" + filename + ".txt", "w")
    f.write(str(content))
    f.close()
    os.chmod(args.w + "/" + filename + ".txt", 0o666)

def read_var(name):
    f = open(args.w + "/" + name + ".txt", "r")
    return f.read()

c = ModbusClient(host=args.o, port=args.p, unit_id=args.u, auto_open=True, auto_close=False, debug=False)

if c.open():

    ups_InputVoltage1 = c.read_holding_registers(151, 1)                # U6
    ups_InputVoltage1 = ups_InputVoltage1[0]/64
    save_var("ups_InputVoltage1", ups_InputVoltage1)

    ups_BattRuntimeLeft = c.read_holding_registers(128, 2)              # U0
    ups_BattRuntimeLeft = ups_BattRuntimeLeft[0]+ups_BattRuntimeLeft[1]
    save_var("ups_BattRuntimeLeft", ups_BattRuntimeLeft)

    ups_PwrConsumed = c.read_holding_registers(145, 2)                  # U0
    ups_PwrConsumed = (ups_PwrConsumed[0]+ups_PwrConsumed[1])/1000
    save_var("ups_PwrConsumed", (ups_PwrConsumed))

    ups_BattTemp = c.read_holding_registers(135, 1)                     # S7
    ups_BattTemp = ups_BattTemp[0]/128
    save_var("ups_BattTemp", ups_BattTemp)

    ups_OutFrequency = c.read_holding_registers(144, 1)                 # U7
    ups_OutFrequency = ups_OutFrequency[0]/128
    save_var("ups_OutFrequency", ups_OutFrequency)

    ups_BattChargePct = c.read_holding_registers(130, 1)                # U9
    ups_BattChargePct = ups_BattChargePct[0]/512
    save_var("ups_BattChargePct", ups_BattChargePct)

    ups_RealPowerPct = c.read_holding_registers(136, 1)                 # U8
    ups_RealPowerPct = ups_RealPowerPct[0]/256
    save_var("ups_RealPowerPct", ups_RealPowerPct)

    ups_ApparentPowerPct = c.read_holding_registers(138, 1)             # U8
    ups_ApparentPowerPct = ups_ApparentPowerPct[0]/256
    save_var("ups_ApparentPowerPct", ups_ApparentPowerPct)

    ups_OutVoltage = c.read_holding_registers(142, 1)                   # U6
    ups_OutVoltage = ups_OutVoltage[0]/64
    save_var("ups_OutVoltage", ups_OutVoltage)

    ups_OutCurrent = c.read_holding_registers(140, 1)                   # U5
    ups_OutCurrent = ups_OutCurrent[0]/32
    save_var("ups_OutCurrent", ups_OutCurrent)

    ups_OutputApparentPowerRating = c.read_holding_registers(588, 1)    # U0
    ups_OutputApparentPowerRating = ups_OutputApparentPowerRating[0]
    save_var("ups_OutApparentPowerRating", ups_OutputApparentPowerRating)

    ups_OutputRealPowerRating = c.read_holding_registers(589, 1)        # U0
    ups_OutputRealPowerRating = ups_OutputRealPowerRating[0]
    save_var("ups_OutRealPowerRating", ups_OutputRealPowerRating)

    ups_BattVoltage = c.read_holding_registers(131, 1)
    ups_BattVoltage = ups_BattVoltage[0]/32
    save_var("ups_BattVoltage", ups_BattVoltage)

    ups_StatusChangeCause = c.read_holding_registers(2, 1)
    ups_StatusChangeCause = ups_StatusChangeCause[0]
    save_var("ups_StatusChangeCause", ups_StatusChangeCause)

    ups_StatusBF = c.read_holding_registers(0, 2)
    ups_StatusBF = ups_StatusBF[0] + ups_StatusBF[1]
    save_var("ups_StatusBF", ups_StatusBF)

    ups_CalculatedLoadW = (ups_RealPowerPct/100) * (ups_OutputRealPowerRating)
    save_var("ups_CalculatedLoadW", ups_CalculatedLoadW)

    ups_BasicIdentModel = "Smart-UPS 1500"
    save_var("ups_BasicIdentModel", ups_BasicIdentModel)

    ups_BasicIdentName = "APC UPS"
    save_var("ups_BasicIdentName", ups_BasicIdentName)

    ups_AdvIdentSkuNumber = "SMT1500IC"
    save_var("ups_AdvIdentSkuNumber", ups_AdvIdentSkuNumber)

    ups_AdvIdentSerialNumber = "123456789012"
    save_var("ups_AdvIdentSerialNumber", ups_AdvIdentSerialNumber)

    save_var("ups_RUNNING_USER", os.getenv('USER'))

    BattLowLimitS = 3600
    if ups_BattRuntimeLeft >= BattLowLimitS:
        # battery normal
        save_var("ups_BasicBatteryStatus", 2)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(30, 0)
    elif ups_BattRuntimeLeft < BattLowLimitS:
        # battery low
        save_var("ups_BasicBatteryStatus", 3)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(30, 1)
    else:
        # battery unknown
        save_var("ups_BasicBatteryStatus", 1)


    # StateOnline(2)     StateOnBattery(4)     StateOutputOff(16)         Fault(32)
    # InputBad(64)       Test-Modifier(128)    PendingOutputOff(512)      HighEfficiency(8192)
    if ups_StatusBF == 8194 or ups_StatusBF == 2:
        # onLine(2)
        ups_BasicOutputStatus = 2
        save_var("ups_BasicOutputStatus", ups_BasicOutputStatus)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(4, 1)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(29, 0)
    elif ups_StatusBF == 4 or ups_StatusBF == 68 or ups_StatusBF == 580:
        # onBattery(3)
        ups_BasicOutputStatus = 3
        save_var("ups_BasicOutputStatus", ups_BasicOutputStatus)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(4, 0)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(2, 1)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(29, 0)
    elif ups_StatusBF == 132 or ups_StatusBF == 130:
        # onBatteryTest(15)
        ups_BasicOutputStatus = 15
        save_var("ups_BasicOutputStatus", ups_BasicOutputStatus)
        ups_BasicStateOutputState = f_upsBasicStateOutputState(29, 1)
    else:
        # unknown(1)
        ups_BasicOutputStatus = 1
        save_var("ups_BasicOutputStatus", ups_BasicOutputStatus)
    # onSmartBoost(4), timedSleeping(5), softwareBypass(6), off(7), rebooting(8), switchedBypass(9), 
    # hardwareFailureBypass(10), sleepingUntilPowerReturn(11), onSmartTrim(12), ecoMode(13), hotStandby(14), 

    # Flag 19: On
    ups_BasicStateOutputState = f_upsBasicStateOutputState(19, 1)
    # Flag 6: Serial Communication Established
    ups_BasicStateOutputState = f_upsBasicStateOutputState(6, 1)

    save_var("ups_BasicStateOutputState", ups_BasicStateOutputState)

    c.close()

else:
    # Flag 19: On
    ups_BasicStateOutputState = f_upsBasicStateOutputState(19, 0)
    # Flag 6: Serial Communication Established
    ups_BasicStateOutputState = f_upsBasicStateOutputState(6, 0)


if args.v == 1:
    print("TEST MODE")
    for name in dir():
        if name.startswith('ups'):
            myvalue = eval(name)
            print(name, "is", type(myvalue), "and is equal to: " + str(myvalue))
    sys.exit()

# ups_BasicIdentModel
if args.g == ".1.3.6.1.4.1.318.1.1.1.1.1.1.0":
    print(args.g)
    print("string")
    print(str(read_var(name="ups_BasicIdentModel")))

# ups_BasicIdentName
if args.g == ".1.3.6.1.4.1.318.1.1.1.1.1.2.0":
    print(args.g)
    print("string")
    print(str(read_var(name="ups_BasicIdentName")))

# ups_AdvIdentSkuNumber
if args.g == ".1.3.6.1.4.1.318.1.1.1.1.2.5.0":
    print(args.g)
    print("string")
    print(str(read_var(name="ups_AdvIdentSkuNumber")))

# ups_AdvIdentSerialNumber
if args.g == ".1.3.6.1.4.1.318.1.1.1.1.2.3.0":
    print(args.g)
    print("string")
    print(str(read_var(name="ups_AdvIdentSerialNumber")))

# ups_AdvBatteryCapacity
if args.g == ".1.3.6.1.4.1.318.1.1.1.2.2.1.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_BattChargePct"))))

# ups_BasicBatteryStatus
if args.g == ".1.3.6.1.4.1.318.1.1.1.2.1.1.0":
    print(args.g)
    print("integer")
    print(int(read_var(name="ups_BasicBatteryStatus")))

# ups_HighPrecBatteryCapacity
if args.g == ".1.3.6.1.4.1.318.1.1.1.2.3.1.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_BattChargePct"))*10))

# upsHighPrecBatteryActualVoltage
if args.g == ".1.3.6.1.4.1.318.1.1.1.2.3.4.0":
    print(args.g)
    print("integer")
    print(int(float(read_var(name="ups_BattVoltage"))*10))

#standard int
if args.g == ".1.3.6.1.4.1.318.1.1.1.2.2.2.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_BattTemp"))))

#high precision
if args.g == ".1.3.6.1.4.1.318.1.1.1.2.3.2.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_BattTemp"))*10))

if args.g == ".1.3.6.1.4.1.318.1.1.1.2.2.3.0":
    print(args.g)
    print("timeticks")
    print(int(float(read_var(name="ups_BattRuntimeLeft"))*100))

# upsAdvInputLineVoltage
if args.g == ".1.3.6.1.4.1.318.1.1.1.3.2.1.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_InputVoltage1"))))

# upsHighPrecInputLineVoltage
if args.g == ".1.3.6.1.4.1.318.1.1.1.3.3.1.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_InputVoltage1"))*10))

# upsAdvOutputVoltage
if args.g == ".1.3.6.1.4.1.318.1.1.1.4.2.1.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_OutVoltage"))))

# upsHighPrecOutputVoltage
if args.g == ".1.3.6.1.4.1.318.1.1.1.4.3.1.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_OutVoltage"))*10))

# ups_HighPrecOutputCurrent
if args.g == ".1.3.6.1.4.1.318.1.1.1.4.3.4.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_OutCurrent"))*10))

# ups_HighPrecOutputFrequency
if args.g == ".1.3.6.1.4.1.318.1.1.1.4.3.2.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_OutFrequency"))*10))

# upsHighPrecInputFrequency - fake
if args.g == ".1.3.6.1.4.1.318.1.1.1.3.3.4.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_OutFrequency"))*10))

# upsBasicOutputStatus
if args.g == ".1.3.6.1.4.1.318.1.1.1.4.1.1.0":
    print(args.g)
    print("integer")
    print(int(read_var(name="ups_BasicOutputStatus")))

# upsBasicStateOutputState
if args.g == ".1.3.6.1.4.1.318.1.1.1.11.1.1.0":
    print(args.g)
    print("string")
    print(int(read_var(name="ups_BasicStateOutputState")))

if args.g == ".1.3.6.1.4.1.318.1.1.1.4.3.3.0":
    print(args.g)
    print("gauge")
    print(int(float(read_var(name="ups_ApparentPowerPct"))*10))
