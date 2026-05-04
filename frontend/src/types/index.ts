// ─── Board & Task ─────────────────────────────────────────────────────────────

export interface ChecklistItem {
  label: string
  done: boolean
}

export interface ActivityComment {
  title: string
  body: string
}

export interface ActivityItem {
  author: string
  initial: string
  color: string
  action: string
  date: string
  comment?: ActivityComment
}

export interface Member {
  name: string
  initial: string
  color: string
}

export interface Task {
  id: string
  column_id: string  
  title: string
  time: string
  status: string
  completed: boolean
  description: string
  dueDate: string
  members: Member[]
  checklist: ChecklistItem[]
  activity: ActivityItem[]
}

export interface Board {
  title: string
  tasks: Task[]
}

// ─── Project ──────────────────────────────────────────────────────────────────

export interface Project {
  id: number
  name: string
  client: string
  tracked: string
  progress: string
  access: string
  starred: boolean
  color: string
}

// ─── Team ─────────────────────────────────────────────────────────────────────

export interface TeamMember {
  id: number
  name: string
  email: string
  role: string
  group: string
}

export interface TeamGroup {
  id: number
  name: string
  members: number
}

// ─── Reports ──────────────────────────────────────────────────────────────────

export interface TimeEntry {
  project: string
  color: string
  desc: string
  date: string
  daySec: number
  durationSec: number
}

export interface ChartSegment {
  name: string
  color: string
  hours: number
}

export interface ChartDay {
  label: string
  segments: ChartSegment[]
  total: number
}

export interface ReportGroup {
  title: string
  color: string
  totalSec: number
  entries: { desc: string; date: string; durationSec: number }[]
}

export interface DonutSegment {
  d: string
  color: string
}

// ─── Sidebar ──────────────────────────────────────────────────────────────────

export interface MenuItem {
  name: string
  path: string
  icon: string
}

// ─── Time Tracker ─────────────────────────────────────────────────────────────

export interface TrackerEntry {
  title: string
  project: string
  time: string
  duration: string
}

export interface TrackerGroup {
  date: string
  total: string
  items: TrackerEntry[]
}