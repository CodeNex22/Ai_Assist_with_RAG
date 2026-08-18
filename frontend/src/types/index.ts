export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  chat_id: string;
  answer: string;
  sources: string[];
  used_rag: boolean;
}

export interface DocumentSummary {
  id: string;
  filename: string;
  size: number;
  uploaded_at: string;
}
