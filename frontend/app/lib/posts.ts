import fs from "node:fs";
import path from "node:path";
import {marked} from "marked"; 
import matter from "gray-matter";

export type PostFrontmatter = {
    title: string;
    date: string;
    tags?: string[];
    excerpt?: string;
}

export type Post = {
    slug: string; 
    frontmatter: PostFrontmatter;
    html: string;
}

const POSTS_DIR = path.join(process.cwd(),'app','content','posts');

export function getAllPostSlugs(): string[] {
    if (!fs.existsSync(POSTS_DIR)) return [];
    return fs.readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith('.md'))
    .map((f) => f.replace(/\.md$/,""));
}

export function getPostBySlug(slug: string): Post | null {
    const full = path.join(POSTS_DIR,`${slug}.md`);
    if(!fs.existsSync(full)) return null;

    const raw = fs.readFileSync(full,'utf8');
    const {data,content} = matter(raw);

    const frontmatter: PostFrontmatter= {
        title: data.title ?? slug,
        date: data.date ?? new Date().toISOString(),
        tags: Array.isArray(data.tags) ? data.tags : [],
        excerpt: data.excerpt ?? "",
    };

    const html = marked.parse(content) as string;
    return {slug,frontmatter,html};
}

export function getAllPosts(): Post[]{
    const slugs = getAllPostSlugs();
    const posts = slugs.map(getPostBySlug).filter(Boolean) as Post[];
    posts.sort(
        (a,b)=> 
            new Date(b.frontmatter.date).getTime()-
        new Date(a.frontmatter.date).getTime()
    );
    return posts;
}

