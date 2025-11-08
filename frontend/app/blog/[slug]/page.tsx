import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllPostSlugs ,getPostBySlug } from "@/app/lib/posts";
import { formatDate } from "@/app/lib/format";
type Params = { slug: string };

// Pre-render all posts (can stay async)
export async function generateStaticParams() {
  return getAllPostSlugs().map((slug) => ({ slug }));
}

// ⬇️ params is a Promise now — await it
export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) return {};
  return {
    title: `${post.frontmatter.title} — Blog`,
    description: post.frontmatter.excerpt ?? "",
  };
}

// ⬇️ Same here: await params
export default async function BlogPostPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) notFound();

  const { frontmatter, html } = post;

  return (
    <article className="max-w-3xl mx-auto">
      <Link href="/blog" className="text-sm text-indigo-600 hover:underline">
        ← Back to Blog
      </Link>

      <h1 className="mt-3 text-3xl font-semibold">{frontmatter.title}</h1>
      <div className="mt-1 text-xs text-slate-500">
        {formatDate(frontmatter.date)}
      </div>

      <div
        className="mt-6 leading-relaxed text-slate-800 space-y-4"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </article>
  );
}