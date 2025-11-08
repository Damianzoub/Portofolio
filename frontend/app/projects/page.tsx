import type { Repo } from "../types/repo";
import ProjectFilter from "@/components/projects/ProjectFilters";
import ProjectGrid from "@/components/projects/ProjectGrid";
import { useMemo,useState } from "react";

export const dynamic ='force-static';

const sample: Repo[] = [
    { id: 1, name: "Iris Classifier", description: "End-to-end ML pipeline with FastAPI inference.", html_url: "https://github.com/Damianzoub/ml-project-iris", language: "Python", stargazers_count: 0, category: "ML" },
    { id: 2, name: "Mall Customers Clustering", description: "KMeans + EDA", html_url: "https://github.com/Damianzoub/Mall_Customers_Clustering", language: "Python", stargazers_count: 0, category: "ML" },
    { id: 3, name: "Time Series Forecast", description: "Classical forecasting", html_url: "https://github.com/Damianzoub/time-series-project", language: "Python", stargazers_count: 0, category: "ML" },
    { id: 4, name: "NewsScrapingAPI", description: "Scrape + sentiment", html_url: "https://github.com/Damianzoub/news-scraping-api", language: "Python", stargazers_count: 0, category: "Automation" },
    { id: 5, name: "Math Utils", description: "Numeric helpers", html_url: "https://github.com/Damianzoub/math-utils", language: "JavaScript", stargazers_count: 0, category: "Math" },
];

//CONTINUE THE PAGE OF PROJECTS BELOW