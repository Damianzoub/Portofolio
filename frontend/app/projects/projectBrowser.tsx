"use client";

import { useEffect, useMemo, useState } from "react";
import ProjectFilter from "@/components/projects/ProjectFilters";
import ProjectGrid from "@/components/projects/ProjectGrid";
import type { ProjectsPage } from "../types/projectsPage";

type Category = "All" | "ML" | "Math" | "Automation" | "Website";
type SortKey = "stars" | "name";

const PER_PAGE = 12;

function buildQuery(params: {
  page: number;
  per_page: number;
  category: Category;
  search?: string;
  sort: SortKey;
}) {
  const qs = new URLSearchParams();
  qs.set("page", String(params.page));
  qs.set("per_page", String(params.per_page));
  qs.set("category", params.category);
  qs.set("sort", params.sort);
  if (params.search && params.search.trim()) qs.set("search", params.search.trim());
  return qs.toString();
}

export default function ProjectBrowser({ initialPage }: { initialPage: ProjectsPage }) {
  const API = process.env.NEXT_PUBLIC_API_BASE;

  const [query, setQuery] = useState("");
  const [cat, setCat] = useState<Category>("All");
  const [sort, setSort] = useState<SortKey>("stars");
  const [page, setPage] = useState<number>(initialPage.page ?? 1);

  const [data, setData] = useState<ProjectsPage>(initialPage);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Reset to page 1 when filters/search/sort change
  useEffect(() => {
    setPage(1);
  }, [cat, sort, query]);

  const requestUrl = useMemo(() => {
    if (!API) return null;
    const qs = buildQuery({
      page,
      per_page: PER_PAGE,
      category: cat,
      search: query,
      sort,
    });
    return `${API}/projects?${qs}`;
  }, [API, page, cat, query, sort]);

  useEffect(() => {
    let cancelled = false;

    async function run() {
      if (!requestUrl) {
        setError("NEXT_PUBLIC_API_BASE is not set.");
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const res = await fetch(requestUrl, { cache: "no-store" });
        if (!res.ok) {
          const text = await res.text();
          throw new Error(`API error ${res.status}: ${text}`);
        }
        const json = (await res.json()) as ProjectsPage;
        if (!cancelled) setData(json);
      } catch (e: any) {
        if (!cancelled) setError(e?.message ?? "Failed to load projects");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [requestUrl]);

  return (
    <section className="max-w-6xl mx-auto px-4 py-10">
      <ProjectFilter
        categories={["All", "ML", "Math", "Automation", "Website"]}
        selectedCategory={cat}
        onSelectCategory={(c: Category) => setCat(c)}
        searchValue={query}
        onSearchChange={setQuery}
        sortValue={sort}
        onSortChange={(v: SortKey) => setSort(v)}
      />

      {error && (
        <div className="mb-4 rounded-xl border p-3 text-sm text-red-700 bg-red-50">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-sm text-slate-500">Loading…</div>
      ) : (
        <ProjectGrid
          items={data.items}
          OnDetails={(repo) => {
            console.log("Details for:", repo);
          }}
        />
      )}

      {/* Pagination */}
      {data.pages > 1 && (
        <div className="mt-6 flex items-center justify-between">
          <button
            disabled={!data.has_prev}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            className="px-3 py-2 rounded-lg border text-sm disabled:opacity-50"
          >
            Previous
          </button>

          <div className="text-sm text-slate-600">
            Page <span className="font-medium">{data.page}</span> / {data.pages} · {data.total} total
          </div>

          <button
            disabled={!data.has_next}
            onClick={() => setPage((p) => p + 1)}
            className="px-3 py-2 rounded-lg border text-sm disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </section>
  );
}