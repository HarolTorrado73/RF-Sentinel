export interface User {
  id: number
  email: string
  username: string
  role: "admin" | "analyst" | "viewer"
  is_active: boolean
}

export interface Target {
  id: number
  name: string
  target_type: "ip" | "domain" | "cidr"
  value: string
  status: string
  description?: string
  owner_id?: number
}

export interface Scan {
  id: number
  target_id: number
  scan_type: string
  status: string
  results?: Record<string, any>
  error_message?: string
  created_at?: string
  completed_at?: string | null
}

export interface Report {
  id: number
  scan_id: number
  title: string
  report_type: "pdf" | "csv" | "json"
  file_path?: string
  created_at?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface CreateScanDTO {
  target_id: number
  scan_type: string
}

export interface CreateReportDTO {
  scan_id: number
  title: string
  report_type: string
}
