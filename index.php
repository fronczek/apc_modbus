<?php

$command = escapeshellcmd('python3 apc_modbus2prtg.py');
$output = shell_exec($command);
file_put_contents('output.xml', $output);
echo $output;

$xmlfile = file_get_contents('output.xml');
$new = simplexml_load_string($xmlfile);
$jsonfile = json_encode($new);
$outarray = json_decode($jsonfile, true);

$nut =  "ups.mfr: APC" . PHP_EOL;
$nut .= "ups.model: APC SMT1500IC" . PHP_EOL;
$nut .= "ups.power.nominal: " . $outarray['result'][11]['value'] . PHP_EOL;
$nut .= "battery.charge: " . $outarray['result'][1]['value'] . PHP_EOL;
$nut .= "battery.runtime: " . $outarray['result'][9]['value'] . PHP_EOL;
$nut .= "battery.temperature: " . $outarray['result'][2]['value'] . PHP_EOL;
$nut .= "input.voltage: " . $outarray['result'][3]['value'] . PHP_EOL;
$nut .= "output.voltage: " . $outarray['result'][5]['value'] . PHP_EOL;
$nut .= "output.voltage.nominal: 230.0" . PHP_EOL;
$nut .= "output.current: " . $outarray['result'][4]['value'] . PHP_EOL;
$nut .= "battery.voltage: " . $outarray['result'][10]['value'] . PHP_EOL;
$nut .= "ups.load: " . $outarray['result'][0]['value'] . PHP_EOL; //apparent

file_put_contents('output.arr', $nut );

?>
