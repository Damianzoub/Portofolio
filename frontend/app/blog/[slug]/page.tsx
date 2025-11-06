import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllPostSlugs ,getPostBySlug } from "@/app/lib/posts";
import { formatDate } from "@/app/lib/format";
type Params = {slug:string};

export async function generateStaticParam(){
    return getAllPostSlugs().map((slug)=>({slug}));
}
export function generateMetadata({params}: {params: Params}){
    const post = getPostBySlug(params.slug);
    if (!post) return {};
    return {
        title:`${post.frontmatter.title} - Blog`,
        description: post.frontmatter.excerpt ?? ""
    };
}

export default function BlogPostPage({params}: {params: Params}){
    const post = getPostBySlug(params.slug);
    if (!post) notFound();
    const {frontmatter,html} = post;

    return (
        <article className="max-w-3xl mx-auto">
            <Link href="/blog" className="text-sm text-indigo-600 hover:underline">
            Back to Blog</Link>

            <h1 className="mt-3 text-3xl font-semibold">{frontmatter.title}</h1>
            <div className="mt-1 text-xs text-slate-500">
                {formatDate(frontmatter.date)}
            </div>

            <div className="mt-6 leading-relaxed text-slate-800 space-y-4" dangerouslySetInnerHTML={{__html: html}}>

            </div>
        </article>
    )
}