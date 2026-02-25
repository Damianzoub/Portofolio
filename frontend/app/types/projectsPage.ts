import type {Repo} from "./repo";

export type ProjectsPage = {
    items: Repo[];
    page:number;
    per_page:number;
    total:number;
    pages:number;
    has_next:boolean;
    has_prev:boolean;
}