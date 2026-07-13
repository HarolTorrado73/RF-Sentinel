import { useEffect, useState } from 'react'
import { apiClient, endpoints } from '../lib/apiClient'
import { useScanStore } from '../stores/scanStore'

export default function Scans() {
  const [targetId, setTargetId] = useState('')
  const [scanType, setScanType] = useState('nmap')
  const [loading, setLoading] = useState(false)
  const { scans, setScans, addScan, targets } = useScanStore()

  useEffect(() => {
    apiClient.get(endpoints.scans.list).then((res) => setScans(res.data))
  }, [setScans])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await apiClient.post(endpoints.scans.create, {
        target_id: Number(targetId),
        scan_type: scanType,
      })
      addScan(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold cyber-text-gradient">Scans</h1>

      <div className="cyber-card">
        <h2 className="text-xl font-bold mb-4">Create New Scan</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Target</label>
            <select
              className="cyber-input"
              value={targetId}
              onChange={(e) => setTargetId(e.target.value)}
              required
            >
              <option value="">Select target</option>
              {targets.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} ({t.value})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Scan Type</label>
            <select
              className="cyber-input"
              value={scanType}
              onChange={(e) => setScanType(e.target.value)}
            >
              <option value="nmap">Nmap</option>
              <option value="portscan">Port Scan</option>
            </select>
          </div>
          <button type="submit" className="cyber-button" disabled={loading}>
            {loading ? 'Creating...' : 'Create Scan'}
          </button>
        </form>
      </div>

      <div className="cyber-card">
        <h2 className="text-xl font-bold mb-4">Scan History</h2>
        {scans.length === 0 ? (
          <p className="text-muted-foreground">No scans found</p>
        ) : (
          <div className="space-y-2">
            {scans.map((s) => (
              <div key={s.id} className="border border-border rounded p-3">
                <p className="font-medium">Scan #{s.id}</p>
                <p className="text-sm text-muted-foreground">
                  Type: {s.scan_type} | Status: {s.status}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}