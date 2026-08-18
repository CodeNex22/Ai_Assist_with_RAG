const API_URL =
  import.meta.env.VITE_API_URL ||
  (typeof window !== 'undefined' ? `http://${window.location.hostname}:8000` : 'http://localhost:8000');

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function sendChatMessage(message: string, chatId?: string) {
  return request<any>('/chat', {
    method: 'POST',
    body: JSON.stringify({ message, chat_id: chatId }),
  });
}

export async function uploadDocuments(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await fetch(`${API_URL}/documents/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    throw new Error('Upload failed');
  }
  return response.json();
}

export async function getHealth() {
  return request<any>('/health');
}

export async function getModels() {
  return request<any>('/models');
}
