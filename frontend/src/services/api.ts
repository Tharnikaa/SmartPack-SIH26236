import { AnalyzeRequest, AnalyzeResponse, MLStatusResponse } from '../types';

const API_BASE = 'http://localhost:8000/api';

export async function analyzePackaging(payload: AnalyzeRequest): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Analysis failed (${res.status}): ${errorText}`);
  }
  return res.json();
}

export async function fetchFoods(query: string = '') {
  const res = await fetch(`${API_BASE}/foods?q=${encodeURIComponent(query)}`);
  return res.json();
}

export async function fetchCategories(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/categories`);
  return res.json();
}

export async function fetchMLStatus(): Promise<MLStatusResponse> {
  const res = await fetch(`${API_BASE}/ml/status`);
  return res.json();
}

export async function triggerMLTrain(): Promise<any> {
  const res = await fetch(`${API_BASE}/ml/train`, { method: 'POST' });
  return res.json();
}

export async function fetchWeights(): Promise<Record<string, number>> {
  const res = await fetch(`${API_BASE}/config/weights`);
  return res.json();
}

export async function updateWeights(weights: Record<string, number>): Promise<any> {
  const res = await fetch(`${API_BASE}/config/weights`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(weights)
  });
  return res.json();
}

export async function fetchPackagingMaterials(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/packaging/materials`);
  return res.json();
}
