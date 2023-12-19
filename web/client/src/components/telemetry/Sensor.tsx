import React from 'react'

type SensorProps = {
  name: string,
  value: number | null | string,
  units: string,
  status?: SensorStatus
}

export enum SensorStatus {
  NORMAL,
  WARNING,
  ANOMALY
}

function SensorStateless(props: SensorProps) {
  const { name, value, units, status = SensorStatus.NORMAL } = props;

  let textStyle = "text-3xl font-bold"
  // let status = SensorStatus.NORMAL
  if (status === SensorStatus.WARNING) {
    textStyle = textStyle + " text-green-500"
  }
  if (status === SensorStatus.ANOMALY) {
    textStyle = textStyle + " text-red-500"
  }

  let valueText = (value !== null) ? `${value}` : "?";

  return (
    <div className='flex flex-col items-center text-xl'>
      <div className='whitespace-nowrap'>{name}</div>
      <div className={textStyle}>{valueText}</div>
      <div>{units}</div>
    </div>
  )
}

export default SensorStateless;