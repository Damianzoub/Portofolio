"use client";

export default function Pagination({
  page,
  pages,
  total,
  hasPrev,
  hasNext,
  onPrev,
  onNext,
}: {
  page: number;
  pages: number;
  total: number;
  hasPrev: boolean;
  hasNext: boolean;
  onPrev: () => void;
  onNext: () => void;
}) {
  if (pages <= 1) return null;

  return (
    <div className="mt-6 flex items-center justify-between">
      <button
        disabled={!hasPrev}
        onClick={onPrev}
        className="px-3 py-2 rounded-lg border text-sm disabled:opacity-50"
      >
        Previous
      </button>

      <div className="text-sm text-slate-600">
        Page <span className="font-medium">{page}</span> / {pages} · {total} total
      </div>

      <button
        disabled={!hasNext}
        onClick={onNext}
        className="px-3 py-2 rounded-lg border text-sm disabled:opacity-50"
      >
        Next
      </button>
    </div>
  );
}