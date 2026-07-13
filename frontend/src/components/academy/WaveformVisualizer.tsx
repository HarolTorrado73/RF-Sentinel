import { useEffect, useRef } from 'react'

interface WaveformVisualizerProps {
  data: {
    carrier_hz?: number
    modulation?: string
    modulation_index?: number
  }
}

export default function WaveformVisualizer({ data }: WaveformVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const width = canvas.width
    const height = canvas.height
    const modulation = data.modulation ?? 'fm'
    const modIndex = data.modulation_index ?? 0.5

    ctx.clearRect(0, 0, width, height)
    ctx.fillStyle = '#151932'
    ctx.fillRect(0, 0, width, height)

    ctx.strokeStyle = '#00d4ff'
    ctx.lineWidth = 2
    ctx.beginPath()

    for (let x = 0; x < width; x++) {
      const t = x / width
      const carrier = Math.sin(2 * Math.PI * 8 * t)
      let signal = carrier

      if (modulation === 'am') {
        const envelope = 0.5 + modIndex * Math.sin(2 * Math.PI * 1.5 * t)
        signal = carrier * envelope
      } else {
        const phase = modIndex * Math.sin(2 * Math.PI * 1.5 * t)
        signal = Math.sin(2 * Math.PI * 8 * t + phase)
      }

      const y = height / 2 - signal * (height / 4)
      if (x === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }

    ctx.stroke()
  }, [data])

  return (
    <div className="cyber-card">
      <h4 className="text-sm font-bold text-cyber-blue mb-3">
        Forma de onda simulada ({data.modulation?.toUpperCase() ?? 'RF'})
      </h4>
      <canvas ref={canvasRef} width={500} height={160} className="w-full rounded" />
    </div>
  )
}
