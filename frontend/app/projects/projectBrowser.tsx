"use client";
import ProjectCard from "@/components/projects/ProjectCard";
import type { Repo } from "../types/repo";
import ProjectFilter from "@/components/projects/ProjectFilters";
import ProjectGrid, { ProjectGridChildren } from "@/components/projects/ProjectGrid";
import { use, useMemo,useState } from "react";

export const dynamic ='force-static';



type Category = "All" | "ML" | "Math" | "Automation" | "Website";

export default function ProjectBrowser({initialItems}:{initialItems:Repo[]}){
    const [query,setQuery] = useState("");
    const [cat,setCat] = useState<Category>("All");
    const [sort,setSort] = useState<"stars"|"name">("stars")

    const filtered = useMemo(()=>{
        let list = initialItems;
        if (cat !=="All"){
            list = list.filter((i)=> i.category ===cat)
        }
        if (query.trim()){
            const q =  query.trim().toLowerCase();
            list = list.filter((i)=> 
            i.name.toLowerCase().includes(q) || (i.description ?? "").toLowerCase().includes(q) || (i.language ?? "").toLowerCase().includes(q))
        }
        if (sort ==="stars"){
            list = [...list].sort((a,b)=>(b.stargazers_count??0)- (a.stargazers_count ?? 0))
        }else{
            list = [...list].sort((a,b)=> a.name.localeCompare(b.name))
        }
        return list 
    },[initialItems,cat,query,sort])
    
    return (
        <section className="max-w-6xl mx-auto">
            <ProjectFilter
            categories={["All","ML","Math","Automation","Website"]}
            selectedCategory={cat}
            onSelectCategory={(c: Category)=> setCat(c)}
            searchValue={query}
            onSearchChange={setQuery}
            sortValue={sort}
            onSortChange={(v:"stars"|"name")=>setSort(v)}
            />

            <ProjectGrid items={filtered} OnDetails={(repo)=>{
                console.log("Details for: ",repo)
            }}>
                
            </ProjectGrid>
        </section>
    )
}