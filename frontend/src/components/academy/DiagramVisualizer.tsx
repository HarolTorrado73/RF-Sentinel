interface DiagramVisualizerProps {
  data: {
    title?: string
    items?: Array<{ label: string; value: string }>
  }
}

export default function DiagramVisualizer({ data }: DiagramVisualizerProps) {
  const items = data.items ?? []

  return (
    <div className="cyber-card">
      <h4 className="text-sm font-bold text-cyber-blue mb-3">{data.title ?? 'Diagrama'}</h4>
      <div className="space-y-2">
        {items.map((item) => (
          <div
            key={item.label}
            className="flex items-center justify-between border border-border rounded px-3 py-2"
          >
            <span className="font-medium text-sm">{item.label}</span>
            <span className="text-sm text-muted-foreground">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
