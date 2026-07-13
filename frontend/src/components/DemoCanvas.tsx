import { useEffect, useRef } from 'react'

interface DemoCanvasProps {
  type: 'spectrum' | 'waterfall'
  className?: string
}

export default function DemoCanvas({ type, className = '' }: DemoCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let frame = 0
    let animationId = 0

    const draw = () => {
      const width = canvas.width
      const height = canvas.height
      frame++

      if (type === 'spectrum') {
        ctx.fillStyle = '#050810'
        ctx.fillRect(0, 0, width, height)

        const bars = 64
        const barWidth = width / bars

        for (let i = 0; i < bars; i++) {
          const amplitude =
            0.3 +
            0.7 *
              Math.abs(
                Math.sin(i * 0.15 + frame * 0.05) * Math.cos(i * 0.08 + frame * 0.03)
              )
          const barHeight = amplitude * height * 0.8
          const x = i * barWidth

          const gradient = ctx.createLinearGradient(x, height - barHeight, x, height)
          gradient.addColorStop(0, '#00f3ff')
          gradient.addColorStop(1, '#0077ff')
          ctx.fillStyle = gradient
          ctx.fillRect(x + 1, height - barHeight, barWidth - 2, barHeight)
        }
      } else {
        const imageData = ctx.getImageData(0, 0, width, height - 1)
        ctx.putImageData(imageData, 0, 1)

        for (let x = 0; x < width; x++) {
          const intensity =
            Math.abs(Math.sin(x * 0.02 + frame * 0.08)) *
            Math.abs(Math.cos(x * 0.01 + frame * 0.05))
          const hue = intensity > 0.7 ? 180 : intensity > 0.4 ? 220 : 260
          ctx.fillStyle = `hsla(${hue}, 80%, ${30 + intensity * 50}%, 0.9)`
          ctx.fillRect(x, 0, 1, 1)
        }
      }

      animationId = requestAnimationFrame(draw)
    }

    const resize = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
    }

    resize()
    window.addEventListener('resize', resize)
    draw()

    return () => {
      window.removeEventListener('resize', resize)
      cancelAnimationFrame(animationId)
    }
  }, [type])

  return (
    <canvas
      ref={canvasRef}
      className={`w-full h-[250px] rounded-lg bg-[#050810] ${className}`}
    />
  )
}
