export type Repo ={
    id:number;
    name:string;
    description?:string|null;
    html_url:string;
    language?:string|null;
    stargazers_count?:number;
    category?: "ML" | "Math" | "Automation" | "Website";
}