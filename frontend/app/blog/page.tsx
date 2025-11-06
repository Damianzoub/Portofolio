import Link from "next/link";
import { getAllPosts } from "../lib/posts";
import { formatDate } from "../lib/format";
export const metadata = {
  title: "Blog — Damian Zoub",
  description: "Notes on ML, engineering, and projects.",
};

export default function BlogIndexPage() {
  const posts = getAllPosts();

  return (
    <section className="max-w-3xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-semibold">Blog</h1>
        <p className="text-slate-700 mt-2">
          Thoughts on ML, engineering, and what I’m building.
        </p>
      </header>

      <ul className="space-y-6">
        {posts.map(({ slug, frontmatter }) => (
          <li
            key={slug}
            className="bg-white rounded-2xl p-5 ring-1 ring-slate-200 hover:shadow-sm transition"
          >
            <Link href={`/blog/${slug}`} className="block">
              <h2 className="text-xl font-semibold">{frontmatter.title}</h2>
              <div className="mt-1 text-xs text-slate-500">
                {formatDate(frontmatter.date)}
              </div>
              {frontmatter.excerpt && (
                <p className="mt-3 text-slate-700">{frontmatter.excerpt}</p>
              )}
              {frontmatter.tags?.length ? (
                <div className="mt-3 flex gap-2 flex-wrap text-xs">
                  {frontmatter.tags.map((t) => (
                    <span
                      key={t}
                      className="rounded-full bg-slate-100 text-slate-700 px-2 py-0.5"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              ) : null}
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
