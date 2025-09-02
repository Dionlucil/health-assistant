import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

export function formatTime(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

export function formatSymptomName(symptom: string): string {
  return symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

export function getSeverityColor(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'severe': return 'text-danger-600 bg-danger-50'
    case 'moderate': return 'text-warning-600 bg-warning-50'
    case 'mild': return 'text-success-600 bg-success-50'
    default: return 'text-gray-600 bg-gray-50'
  }
}

export function getUrgencyColor(urgency: string): string {
  switch (urgency.toLowerCase()) {
    case 'high': return 'text-danger-600'
    case 'medium': return 'text-warning-600'
    case 'low': return 'text-success-600'
    default: return 'text-gray-600'
  }
}