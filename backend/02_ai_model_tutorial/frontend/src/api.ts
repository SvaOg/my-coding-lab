export const API_BASE = 'http://localhost:8000';

export type RequestItem = {
  prompt?: string;
  response?: string;
  answer?: string;
  result?: string;
  created_at?: string;
  ts?: string;
  timestamp?: string;
};

export async function sendPrompt(prompt: string) {
  const res = await fetch(`${API_BASE}/requests`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Ошибка ${res.status}`);
  }
  const data = await res.json();
  return data.answer ?? data;
}

export async function fetchHistory(): Promise<RequestItem[]> {
  const res = await fetch(`${API_BASE}/requests`);
  if (!res.ok) {
    throw new Error(`Ошибка ${res.status}`);
  }
  return res.json();
}
