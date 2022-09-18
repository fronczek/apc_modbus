#!/usr/bin/python3

from pyModbusTCP.client import ModbusClient

c = ModbusClient(host="172.16.10.4", port=502, unit_id=1,
                 auto_open=True, auto_close=False, debug=False)

if c.open():
    ups_InputVoltage = c.read_holding_registers(151, 1)               # U6
    ups_RuntimeLeft = c.read_holding_registers(128, 2)                # U0
    ups_PwrConsumed = c.read_holding_registers(145, 2)                # U0
    ups_BattTemp = c.read_holding_registers(135, 1)                   # S7
    ups_BattVoltage = c.read_holding_registers(131, 1)                # S5
    ups_ChargePct = c.read_holding_registers(130, 1)                  # U9
    ups_RealPowerPct = c.read_holding_registers(136, 1)               # U8
    ups_ApparentPowerPct = c.read_holding_registers(138, 1)           # U8
    ups_OutVoltage = c.read_holding_registers(142, 1)                 # U6
    ups_OutFrequency = c.read_holding_registers(144,1)                # U7
    ups_OutCurrent = c.read_holding_registers(140, 1)                 # U5
    ups_OutputApparentPowerRating = c.read_holding_registers(588, 1)  # U0
    ups_OutputRealPowerRating = c.read_holding_registers(589, 1)      # U0
    ups_StatusChangeCause = c.read_holding_registers(2,1)             # ENUM
    ups_StatusBF = c.read_holding_registers(0, 2)                     # BF

    print('<?xml version="1.0" encoding="UTF-8" ?>')
    print("<prtg>")
    print("<result><channel>ups_ApparentLoadPct</channel><value>" + str(ups_ApparentPowerPct[0]/256) + "</value><unit>Percent</unit><float>1</float></result>")
    print("<result><channel>ups_BatteryChargedPct</channel><value>" + str(ups_ChargePct[0]/512) + "</value><unit>Percent</unit><float>1</float></result>")
    print("<result><channel>ups_BatteryTemperature</channel><value>" + str(ups_BattTemp[0]/128) + "</value><unit>Temperature</unit><float>1</float></result>")
    print("<result><channel>ups_InputVoltage</channel><value>" + str(ups_InputVoltage[0]/64) + "</value><unit>Custom</unit><customunit>V</customunit><float>1</float></result>")
    print("<result><channel>ups_OutputCurrent</channel><value>" + str(ups_OutCurrent[0]/32) + "</value><unit>Custom</unit><customunit>A</customunit><float>1</float></result>")
    print("<result><channel>ups_OutputVoltage</channel><value>" + str(ups_OutVoltage[0]/64) + "</value><unit>Custom</unit><customunit>V</customunit><float>1</float></result>")
    print("<result><channel>ups_RealLoadPct</channel><value>" + str(ups_RealPowerPct[0]/256) + "</value><unit>Percent</unit><float>1</float></result>")
    print("<result><channel>ups_RealLoadW</channel><value>" + str((((ups_RealPowerPct[0]/256)/100) * (ups_OutputRealPowerRating[0]))) + "</value><unit>Custom</unit><customunit>W</customunit><float>1</float></result>")
    print("<result><channel>ups_RealPowerConsumed</channel><value>" + str((ups_PwrConsumed[0]+ups_PwrConsumed[1])/1000) + "</value><unit>Custom</unit><customunit>kWh</customunit><float>1</float></result>")
    print("<result><channel>ups_RuntimeLeft</channel><value>" + str(ups_RuntimeLeft[0]+ups_RuntimeLeft[1]) + "</value><unit>TimeSeconds</unit><float>0</float></result>") #idx9
    print("<result><channel>ups_BatteryVoltage</channel><value>" + str(ups_BattVoltage[0]/32) + "</value><unit>Custom</unit><customunit>VDC</customunit><float>1</float></result>")
    print("<result><channel>ups_ApparentPwrRating</channel><value>" + str(ups_OutputApparentPowerRating[0]) + "</value><unit>Custom</unit><customunit>VA</customunit><float>0</float></result>") #11
    print("<result><channel>ups_StatusChangeCause</channel><value>" + str(ups_StatusChangeCause[0]) + "</value><ValueLookup>xml.apc.modbus.UPSStatusChangeCause</ValueLookup></result>") #12
    print("<result><channel>ups_StatusBF</channel><value>" + str(ups_StatusBF[0] + ups_StatusBF[1]) + "</value><ValueLookup>xml.apc.modbus.UPSStatus_BF</ValueLookup></result>") #13
    print("<result><channel>ups_OutputFrequency</channel><value>" + str(ups_OutFrequency[0]/128) + "</value><unit>Custom</unit><customunit>Hz</customunit><float>1</float></result>") #14
    print("</prtg>")
    c.close()

else:
    print('<?xml version="1.0" encoding="UTF-8" ?>')
    print("<prtg>")
    print("<error>3</error>")
    print("<text>Modbus connection error</text>")
    print("</prtg>")
