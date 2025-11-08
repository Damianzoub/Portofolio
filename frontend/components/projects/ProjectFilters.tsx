"use client";

type Category = "All" | "ML" | "Math" | "Automation" | "Website";
type SortKey = "stars" | "name";

export default function ProjectFilter({
    categories = ["All","ML","Math","Automation","Website"],
    selectedCategory,
    onSelectCategory,
    searchValue,
    onSearchChange,
    sortValue,
    onSortChange
}:{
    categories?: Category[];
    selectedCategory: Category;
    onSelectCategory: (c:Category)=>void;
    searchValue:string;
    onSearchChange: (v:string)=>void;
    sortValue:SortKey;
    onSortChange: (v:SortKey)=>void;
}){

    return (
        <div className="mb-6 flex flex-col gap-3 md:flex-row md:-items-center md:justify-between">
            <div className="flex gap-2 flex-wrap">
                {categories.map((c)=>(
                    <button key={c} onClick={()=>onSelectCategory(c)} className={`px-3 py-1.5 rounded-lg text-sm transition ${selectedCategory === c ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"}`}>{c}</button>
                ))}
            </div>

            <div className="flex gap-2">
                <input placeholder="Search Projects" value={searchValue} onChange={(e)=> onSearchChange(e.target.value)}  className="rounded-lg border px-3 py-2 text-sm w-56" />
                <select name="sort" value={sortValue} onChange={(e)=>onSortChange(e.target.value as SortKey)} className="rounded-lg border px-3 py-2 text-sm" id="sort">
                    <option value="stars">Sort: Stars</option>
                    <option value="name">Sort: Name</option>
                </select>
            </div>
        </div>
    )

}