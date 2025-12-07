import { useEffect, useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { fetchHistory, sendPrompt, RequestItem, API_BASE } from './api';

function formatDate(value?: string) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function AnswerBlock({ answer }: { answer: string }) {
  return (
    <div className="card p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Ответ</h2>
        <button
          className="btn btn-ghost text-emerald-700"
          onClick={() => navigator.clipboard.writeText(answer)}
        >
          Копировать
        </button>
      </div>
      <pre className="bg-slate-900 text-slate-50 rounded-lg p-3 text-sm overflow-auto min-h-[120px]">
        {answer || '- Нет ответа -'}
      </pre>
    </div>
  );
}

function HistoryList({ items }: { items: RequestItem[] }) {
  if (!items?.length) {
    return <p className="text-slate-500 text-sm">Записей нет.</p>;
  }
  return (
    <ul className="space-y-3">
      {items.map((it, idx) => {
        const timestamp = it.created_at || it.ts || it.timestamp;
        const prompt = it.prompt || '';
        const response = it.response || it.answer || it.result || '';
        return (
          <li key={`${prompt}-${idx}`} className="border border-slate-100 rounded-lg p-3 bg-slate-50">
            <div className="flex items-start justify-between gap-3">
              <div className="space-y-1">
                {timestamp && <div className="badge">{formatDate(timestamp)}</div>}
                {prompt && (
                  <div>
                    <span className="font-semibold">Prompt:</span> {prompt}
                  </div>
                )}
                {response && (
                  <div>
                    <span className="font-semibold">Ответ:</span> {response}
                  </div>
                )}
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
}

export default function App() {
  const queryClient = useQueryClient();
  const [prompt, setPrompt] = useState('');

  const historyQuery = useQuery({
    queryKey: ['history'],
    queryFn: fetchHistory,
  });

  const sendMutation = useMutation({
    mutationFn: sendPrompt,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['history'] });
    },
  });

  const statusText = useMemo(() => {
    if (sendMutation.isPending) return 'Отправка...';
    if (sendMutation.isError) return 'Ошибка отправки';
    if (historyQuery.isFetching) return 'Загрузка истории...';
    if (sendMutation.isSuccess) return 'Готово';
    return 'Готов';
  }, [sendMutation.isPending, sendMutation.isError, historyQuery.isFetching, sendMutation.isSuccess]);

  const answer = useMemo(() => {
    if (sendMutation.data === undefined) return '';
    return typeof sendMutation.data === 'string'
      ? sendMutation.data
      : JSON.stringify(sendMutation.data, null, 2);
  }, [sendMutation.data]);

  useEffect(() => {
    // auto-refresh history once on mount
    historyQuery.refetch();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const value = prompt.trim();
    if (!value) return;
    sendMutation.mutate(value);
  };

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 p-6">
      <div className="max-w-4xl mx-auto space-y-5">
        <header className="flex flex-col gap-2 card p-4">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold">API Demo</h1>
            <span className="badge">React + Tailwind</span>
          </div>
          <p className="text-sm text-slate-600">
            Бэкенд: <span className="font-mono text-slate-800">{API_BASE}</span>
          </p>
          <p className="text-sm text-slate-500">
            Убедитесь, что CORS разрешает этот origin (например, http://localhost:5173).
          </p>
        </header>

        <section className="card p-5 space-y-4">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div>
              <p className="text-base font-semibold">Prompt</p>
              <p className="text-sm text-slate-500">POST /requests</p>
            </div>
            <span className="text-sm text-slate-500">{statusText}</span>
          </div>
          <form onSubmit={onSubmit} className="space-y-3">
            <textarea
              className="w-full min-h-[140px] rounded-xl border border-slate-200 bg-white p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-200"
              placeholder="Введите prompt для отправки на бэкенд"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <div className="flex flex-wrap items-center gap-3">
              <button type="submit" className="btn btn-primary" disabled={!prompt.trim() || sendMutation.isPending}>
                {sendMutation.isPending ? 'Отправка...' : 'Отправить'}
              </button>
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => setPrompt('')}
                disabled={sendMutation.isPending}
              >
                Очистить
              </button>
              {sendMutation.isError && (
                <span className="text-sm text-red-600">{String(sendMutation.error)}</span>
              )}
            </div>
          </form>
        </section>

        <AnswerBlock answer={answer} />

        <section className="card p-5 space-y-4">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div>
              <h2 className="text-lg font-semibold">История</h2>
              <p className="text-sm text-slate-500">GET /requests</p>
            </div>
            <div className="flex items-center gap-2">
              <button className="btn btn-ghost" onClick={() => historyQuery.refetch()} disabled={historyQuery.isFetching}>
                Обновить
              </button>
              {historyQuery.isFetching && <span className="text-sm text-slate-500">Загрузка...</span>}
            </div>
          </div>
          {historyQuery.isError ? (
            <p className="text-red-600 text-sm">Не удалось загрузить историю</p>
          ) : historyQuery.isLoading ? (
            <p className="text-slate-500 text-sm">Загрузка...</p>
          ) : (
            <HistoryList items={historyQuery.data || []} />
          )}
        </section>
      </div>
    </main>
  );
}
