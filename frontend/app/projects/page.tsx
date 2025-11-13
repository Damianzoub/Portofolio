import ProjectBrowser from "./projectBrowser";
import type { Repo } from "../types/repo";

export const metadata ={
    title: "Projects Damianos Zoumpos",
    description: "My Personal Projects from my Github"
}

async function fetchProjects(): Promise<Repo[]>{
    const base = process.env.NEXT_PUBLIC_API_BASE!;
    const res = await fetch(`${base}/projects`,{cache:"no-store"})
        if (!res.ok){
            console.error("Failed to fetch Projects",res.status);
            return [];
        }
        return res.json();
    
}

export default async function ProjectsPage(){
    const repos = await fetchProjects();
    return <ProjectBrowser initialItems={repos}/>
}


