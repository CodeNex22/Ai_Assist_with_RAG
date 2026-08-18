import { useMemo, useState } from 'react';
import { useHealth, useModels } from './hooks/useChat';
import { ChatWindow } from './components/ChatWindow';
import { UploadPanel } from './components/UploadPanel';
import { ChatMessage } from './types';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const health = useHealth();
  const models = useModels();

  const statusLabel = useMemo(() => {
    if (health.isError) return 'Backend unavailable';
    if (health.isLoading) return 'Checking backend...';
    return 'Backend ready';
  }, [health.isError, health.isLoading]);

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-8 text-slate-100 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <header className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Local RAG Assistant</p>
              <h1 className="mt-2 text-3xl font-semibold">AI Customer Support Assistant</h1>
              <p className="mt-3 max-w-2xl text-sm text-slate-400">
                A modular, local-first support experience backed by Ollama, Qdrant, and your own uploaded documents.
              </p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-slate-300">
              <p>{statusLabel}</p>
              <p className="mt-1 text-xs text-slate-500">Model: {models.data?.models?.[0] ?? 'qwen3:8b'}</p>
            </div>
          </div>
        </header>

        <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <ChatWindow messages={messages} onMessagesChange={setMessages} />
          <div className="space-y-6">
            <UploadPanel />
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl">
              <h3 className="text-lg font-semibold text-slate-100">Architecture Highlights</h3>
              <ul className="mt-4 space-y-2 text-sm text-slate-400">
                <li>• Ollama-powered generation</li>
                <li>• Qdrant-backed retrieval</li>
                <li>• Document upload and chunking</li>
                <li>• WhatsApp-ready adapter boundary</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
