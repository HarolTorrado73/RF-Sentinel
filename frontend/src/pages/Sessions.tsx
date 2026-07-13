import { useEffect, useState } from 'react'
import { apiClient, endpoints } from '../lib/apiClient'

interface Session {
  id: number
  user_id: number
  machine_id: number | null
  status: string
  start_time: string
  end_time: string | null
  created_at: string
}

export default function Sessions() {
  const [sessions, setSessions] = useState<Session[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    apiClient.get(endpoints.sessions.list).then((res) => setSessions(res.data))
  }, [])

  const closeSession = async (id: number) => {
    setLoading(true)
    await apiClient.put(endpoints.sessions.update(id), { status: 'closed' })
    setSessions(sessions.map((s) => (s.id === id ? { ...s, status: 'closed' } : s)))
    setLoading(false)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold cyber-text-gradient">Sessions</h1>

      <div className="cyber-card">
        <h2 className="text-xl font-bold mb-4">Session List</h2>
        {sessions.length === 0 ? (
          <p className="text-muted-foreground">No sessions found</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left pb-2">ID</th>
                  <th className="text-left pb-2">User ID</th>
                  <th className="text-left pb-2">Machine ID</th>
                  <th className="text-left pb-2">Status</th>
                  <th className="text-left pb-2">Action</th>
                </tr>
              </thead>
              <tbody>
                {sessions.map((s) => (
                  <tr key={s.id} className="border-b border-border/50">
                    <td className="py-2">{s.id}</td>
                    <td className="py-2">{s.user_id}</td>
                    <td className="py-2">{s.machine_id || '-'}</td>
                    <td className="py-2">{s.status}</td>
                    <td className="py-2">
                      <button
                        className="cyber-button text-xs"
                        onClick={() => closeSession(s.id)}
                        disabled={loading || s.status === 'closed'}
                      >
                        Close
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}