import React from "react";
import SensorStateless, { SensorStatus } from "../telemetry/Sensor";

function Main() {
  return (
    <div className="m-10 flex justify-between">
      <SensorStateless name="Power Usage" value={4.1} units="kW" />
      <SensorStateless name="Solar Output" value={5.2} units="kW" />
      <SensorStateless name="Difference" value={"+1.1"} units="kW" status={SensorStatus.WARNING}/>
      <SensorStateless name="Battery Voltage" value={52.3} units="Volts" />
      <SensorStateless name="Inverter Current" value={6.1} units="Amps" />
    </div>
  );
}

export default Main;
