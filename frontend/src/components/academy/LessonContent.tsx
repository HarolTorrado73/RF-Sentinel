function renderContent(content: string) {
  return content.split('\n').map((line, index) => {
    if (line.startsWith('## ')) {
      return (
        <h3 key={index} className="text-lg font-bold mt-4 mb-2 text-cyber-blue">
          {line.replace('## ', '')}
        </h3>
      )
    }
    if (line.startsWith('### ')) {
      return (
        <h4 key={index} className="text-md font-bold mt-3 mb-1">
          {line.replace('### ', '')}
        </h4>
      )
    }
    if (line.startsWith('- ')) {
      return (
        <li key={index} className="text-sm text-muted-foreground ml-4 list-disc">
          {line.replace('- ', '').replace(/\*\*(.*?)\*\*/g, '$1')}
        </li>
      )
    }
    if (line.startsWith('```')) {
      return null
    }
    if (line.trim() === '') {
      return <br key={index} />
    }
    if (line.startsWith('|')) {
      return (
        <p key={index} className="text-xs font-mono text-muted-foreground">
          {line}
        </p>
      )
    }
    if (line.startsWith('**') && line.endsWith('**')) {
      return (
        <p key={index} className="text-sm font-bold text-cyber-accent mt-2">
          {line.replace(/\*\*/g, '')}
        </p>
      )
    }
    return (
      <p key={index} className="text-sm text-muted-foreground leading-relaxed">
        {line.replace(/\*\*(.*?)\*\*/g, '$1').replace(/`(.*?)`/g, '$1')}
      </p>
    )
  })
}

interface LessonContentProps {
  content: string
}

export default function LessonContent({ content }: LessonContentProps) {
  return <div className="prose-invert space-y-1">{renderContent(content)}</div>
}
