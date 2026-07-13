import { useEffect, useRef } from 'react'

interface SpectrumVisualizerProps {
  data: {
    frequencies_mhz?: number[]
    amplitudes?: number[]
    labels?: string[]
  }
}

export default function SpectrumVisualizer({ data }: SpectrumVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const frequencies = data.frequencies_mhz ?? []
    const amplitudes = data.amplitudes ?? []
    const width = canvas.width
    const height = canvas.height

    ctx.clearRect(0, 0, width, height)

    const gradient = ctx.createLinearGradient(0, 0, 0, height)
    gradient.addColorStop(0, '#151932')
    gradient.addColorStop(1, '#0a0e27')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, width, height)

    ctx.strokeStyle = '#1e2a4a'
    ctx.lineWidth = 1
    for (let i = 0; i <= 4; i++) {
      const y = (height / 4) * i
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(width, y)
      ctx.stroke()
    }

    if (frequencies.length === 0) return

    const barWidth = width / frequencies.length - 4
    frequencies.forEach((freq, index) => {
      const amplitude = amplitudes[index] ?? 0.5
      const barHeight = amplitude * (height - 40)
      const x = index * (barWidth + 4) + 2
      const y = height - barHeight - 20

      const barGradient = ctx.createLinearGradient(x, y, x, height - 20)
      barGradient.addColorStop(0, '#00d4ff')
      barGradient.addColorStop(1, '#ff0055')
      ctx.fillStyle = barGradient
      ctx.fillRect(x, y, barWidth, barHeight)

      ctx.fillStyle = '#8892b0'
      ctx.font = '10px sans-serif'
      ctx.textAlign = 'center'
      ctx.fillText(`${freq}`, x + barWidth / 2, height - 6)
    })
  }, [data])

  return (
    <div className="cyber-card">
      <h4 className="text-sm font-bold text-cyber-blue mb-3">Espectro simulado (MHz)</h4>
      <canvas ref={canvasRef} width={500} height={200} className="w-full rounded" />
      <p className="text-xs text-muted-foreground mt-2">
        Visualización educativa con datos simulados. No representa señales reales en vivo.
      </p>
    </div>
  )
}
