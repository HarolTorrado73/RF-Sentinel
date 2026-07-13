interface ProgressBarProps {
  percent: number
  label?: string
}

export default function ProgressBar({ percent, label }: ProgressBarProps) {
  const clamped = Math.min(100, Math.max(0, percent))

  return (
    <div className="space-y-1">
      {label && (
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">{label}</span>
          <span className="text-cyber-blue font-medium">{clamped}%</span>
        </div>
      )}
      <div className="h-2 bg-cyber-dark rounded-full overflow-hidden border border-border">
        <div
          className="h-full bg-gradient-to-r from-cyber-blue to-cyber-accent transition-all duration-500"
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  )
}
