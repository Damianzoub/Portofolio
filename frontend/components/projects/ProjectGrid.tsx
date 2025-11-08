import type { Repo } from "@/app/types/repo";
import ProjectCard from "./ProjectCard";

export default function ProjectGrid({
    items,OnDetails,
}:{items:Repo[]; OnDetails?:(repo:Repo)=>void;}){
    if (!items.length){
        return <div className="text-slate-500 text-sm">
            No projects match your filters
        </div>
    }
    return (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {items.map((repo)=>(
                <ProjectCard key={repo.id} repo={repo} onDetails={OnDetails}/>
            ))}
        </div>
    )
}

export function ProjectGridChildren({children}:{
    children:React.ReactNode
}){
    return <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">{children}</div>
}