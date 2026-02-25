import ProjectBrowser from "./projectBrowser";
import type { ProjectsPage } from "../types/projectsPage";

export const metadata = {
  title: "Projects Damianos Zoumpos",
  description: "My Personal Projects from my Github",
};

async function fetchProjectsPage(): Promise<ProjectsPage> {
  const base = process.env.NEXT_PUBLIC_API_BASE!;
  const url = `${base}/projects?page=1&per_page=12&category=All&sort=stars`;

  const res = await fetch(url, { cache: "no-store" });

  if (!res.ok) {
    console.error("Failed to fetch Projects", res.status);
    return {
      items: [],
      page: 1,
      per_page: 12,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
    };
  }

  return res.json();
}

export default async function ProjectsPage() {
  const initialPage = await fetchProjectsPage();
  return <ProjectBrowser initialPage={initialPage} />;
}