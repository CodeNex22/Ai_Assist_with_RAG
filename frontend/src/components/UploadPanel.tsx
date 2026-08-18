import { ChangeEvent, useState } from 'react';
import { useUploadDocuments } from '../hooks/useChat';

export function UploadPanel() {
  const [status, setStatus] = useState('No files uploaded yet.');
  const uploadDocuments = useUploadDocuments();

  const handleUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setStatus(`Uploading ${file.name}...`);
    try {
      const result = await uploadDocuments.mutateAsync(file);
      setStatus(`Indexed ${result.filename} successfully.`);
    } catch {
      setStatus('Upload failed. Please check the backend service.');
    }
  };

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl">
      <h3 className="text-lg font-semibold text-slate-100">Upload Documents</h3>
      <p className="mt-2 text-sm text-slate-400">PDF, DOCX, TXT, Markdown, and CSV files are supported.</p>
      <label className="mt-4 flex cursor-pointer items-center justify-center rounded-2xl border border-dashed border-cyan-600 px-4 py-8 text-sm text-cyan-400">
        <span>Drag and drop or choose a file</span>
        <input className="hidden" type="file" onChange={handleUpload} />
      </label>
      <p className="mt-3 text-sm text-slate-400">{status}</p>
    </div>
  );
}
