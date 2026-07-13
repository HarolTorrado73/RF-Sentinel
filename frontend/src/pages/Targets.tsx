import { useEffect, useState } from 'react'
import { apiClient, endpoints } from '../lib/apiClient'
import { useScanStore } from '../stores/scanStore'

export default function Targets() {
  const [name, setName] = useState('')
  const [value, setValue] = useState('')
  const [targetType, setTargetType] = useState<'ip' | 'domain' | 'cidr'>('ip')
  const [loading, setLoading] = useState(false)
  const { targets, setTargets, addTarget } = useScanStore()

  useEffect(() => {
    apiClient.get(endpoints.targets.list).then((res) => setTargets(res.data))
  }, [setTargets])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await apiClient.post(endpoints.targets.create, {
        name,
        value,
        target_type: targetType,
      })
      addTarget(res.data)
      setName('')
      setValue('')
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold cyber-text-gradient">Targets</h1>

      <div className="cyber-card">
        <h2 className="text-xl font-bold mb-4">Add New Target</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              type="text"
              className="cyber-input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Target name"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Value</label>
            <input
              type="text"
              className="cyber-input"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder="IP, Domain, or CIDR"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Type</label>
            <select
              className="cyber-input"
              value={targetType}
              onChange={(e) => setTargetType(e.target.value as any)}
            >
              <option value="ip">IP</option>
              <option value="domain">Domain</option>
              <option value="cidr">CIDR</option>
            </select>
          </div>
          <button type="submit" className="cyber-button" disabled={loading}>
            {loading ? 'Adding...' : 'Add Target'}
          </button>
        </form>
      </div>

      <div className="cyber-card">
        <h2 className="text-xl font-bold mb-4">Target List</h2>
        {targets.length === 0 ? (
          <p className="text-muted-foreground">No targets configured</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left pb-2">Name</th>
                  <th className="text-left pb-2">Value</th>
                  <th className="text-left pb-2">Type</th>
                  <th className="text-left pb-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {targets.map((t) => (
                  <tr key={t.id} className="border-b border-border/50">
                    <td className="py-2">{t.name}</td>
                    <td className="py-2">{t.value}</td>
                    <td className="py-2">{t.target_type}</td>
                    <td className="py-2">{t.status}</td>
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