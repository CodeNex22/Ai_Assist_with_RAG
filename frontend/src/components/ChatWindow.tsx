import { FormEvent, useState } from 'react';
import { useSendMessage } from '../hooks/useChat';
import { ChatMessage } from '../types';

interface ChatWindowProps {
  messages: ChatMessage[];
  onMessagesChange: (messages: ChatMessage[]) => void;
}

export function ChatWindow({ messages, onMessagesChange }: ChatWindowProps) {
  const [draft, setDraft] = useState('');
  const sendMessage = useSendMessage();

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!draft.trim()) return;

    const userMessage: ChatMessage = { role: 'user', content: draft.trim() };
    const nextMessages = [...messages, userMessage];
    onMessagesChange(nextMessages);
    setDraft('');

    try {
      const response = await sendMessage.mutateAsync({ message: userMessage.content });
      onMessagesChange([...nextMessages, { role: 'assistant', content: response.answer }]);
    } catch (error) {
      onMessagesChange([...nextMessages, { role: 'assistant', content: 'The assistant is unavailable right now.' }]);
    }
  };

  return (
    <div className="flex h-[70vh] flex-col rounded-3xl border border-slate-800 bg-slate-900/70 shadow-2xl">
      <div className="flex items-center justify-between border-b border-slate-800 px-6 py-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Support Assistant</h2>
          <p className="text-sm text-slate-400">Grounded by your uploaded documents</p>
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto px-6 py-4">
        {messages.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-700 p-4 text-sm text-slate-400">
            Ask a question about your business documents to get started.
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={`${message.role}-${index}`} className={`rounded-2xl px-4 py-3 ${message.role === 'user' ? 'ml-auto bg-cyan-600 text-white' : 'bg-slate-800 text-slate-100'}`}>
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleSubmit} className="border-t border-slate-800 p-4">
        <div className="flex gap-3">
          <input
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            placeholder="Ask about your support policies..."
            className="flex-1 rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none"
          />
          <button type="submit" className="rounded-2xl bg-cyan-600 px-4 py-3 text-sm font-semibold text-white">
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
