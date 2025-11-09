import { Repo } from "@/app/types/repo";
import { ExternalLink } from "lucide-react";

export default function ProjectCard({
    repo,onDetails
}:{repo:Repo; onDetails?:(repo:Repo)=>void}){
    return (
        <article className="bg-white rounded-2xl p-3 shadow-sm ring-1 ring-slate-200 hover:shadow-md transition">
            <h3 className="text-lg font-semibold tracking-tight">
                {repo.name}
            </h3>
            <p className="text-sm text-slate-600 mt-2 line-clamp-3">
                {repo.description ?? "No description provided"}
            </p>
            <div className="mt-4 flex items-center justify-between text-sm">
                <div className="flex items-center gap-2 text-slate-500">
                    <span className="px-2 py-0.5 rounded bg-slate-100">
                        {repo.language ?? "N/A"}
                    </span>
                    {typeof repo.stargazers_count ==="number" && (
                        <span>{repo.stargazers_count}</span>
                    )}
                    {repo.category && (
                        <span className="px-2 py-0.5 rounded bg-indigo-50 text-indigo-700">
                            {repo.category}
                        </span>
                    )}
                </div>
                <div className="flex items-center gap-2">
                    {onDetails && (
                        <button onClick={()=> onDetails(repo)} className="px-3 py-1.5 rounded-lg bg-slate-900 text-white hover:bg-slate-800">
                            Details
                        </button>
                    )}
                    <a href={repo.html_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 text-indigo-600 hover:underline ">GitHub <ExternalLink size={16}/></a>
                </div>
            </div>
        </article>
    )
}