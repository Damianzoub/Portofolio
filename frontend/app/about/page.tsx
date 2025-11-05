import Link from "next/link";


function Pill({children}: {children:React.ReactNode}){
    return (
        <span className="inline-flex items-center ronuded-full bg-slate-100 text-slate-700 text-xs px-2 py-0.5">
            {children}
        </span>
    )
}

export const metada = {
    title: "About - Damianos Zoumpos",
    description:"About Damianos Zoumpos - Machine Learning Engineer"
};

export default function AboutPage(){
    return (
        <section className="max-2-6xl mx-auto">
            <div className="max-w-2xl mx-auto text-center">
                <h1 className="text-3xl md:text-4xl font-semibold tracking-tight">
                    About Me 
                </h1>
                <p className="mt-4 text-slate-700">
                    I'm Damian, a Machine Learning engineer focus on turning data into usable products -
                    from collection and feature engineering to model serving and ligthweight UIs 
                </p>
                <div className="mt-6 flex items-center justify-center gap-3">
                    {/**Add my CV to the public/cv/ directory */}
                    <Link href="/cv/Damianos_ZoumposCV.pdf" target="_blank" className="px-4 py-2 rounded-xl bg-slate-900 text-white hover:bg-slate-800">Download my CV</Link>
                    <Link href="mailto:d.zoumpos04@gmail.com" className="px-4 py-2 rounded-xl border hover:bg-slate-100">Contact Me</Link>
                </div>
            </div>

            {/**LEFT CATEGORIES / RIGHT DETAILS */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-[220px_minmax(0,1fr)] gap-8">
                <aside className="md:pr-4">
                    <nav className="sticky-top-24 space-y-2">
                        <a href="#experience" className="block text-sm hover:underline">
                            Experience
                        </a>
                        <a href="#projects" className="block text-sm hover:underline">
                            Projects
                        </a>
                        <a href="#volunteer_work" className="block text-sm hover:underline">
                            Volunteer Work
                        </a>
                        <a href="#skills" className="block text-sm hover:underline">
                            Skills
                        </a>
                        <a href="#Languages" className="block text-sm hover:underline">
                            Languages
                        </a>
                        <a href="#certs" className="block text-sm hover:underline">
                            Certificates
                        </a>
                    </nav>
                </aside>

                <div className="md:border-l md:pl-8 md:border-slate-200">
                    <section className="space-y-3" id="experience">
                        <h2 className="text-xl font-semibold">Experience</h2>
                        <div className="bg-white rounded-2xl p-5 ring-1 ring-slate-200">
                            <div className="text-sm text-slate-500">Apr 2025 - Aug 2025</div>
                            <div className="mt-1 font-medium">
                                Feature Engineer - New Data Spaces for Green Mobility (research program)
                            </div>
                            <p className="mt-2 text-slate-700">
                            Manipulated raw data, engineered features, and applied machine
                learning for analysis and modeling; contributed to a cleaner,
                production-oriented workflow. 
                            </p>
                        </div>
                    </section>
                    <section id="projects" className="space-y-3">
                        <h2 className="text-xl py-2 font-semibold">Projects</h2>
                        <div className="bg-white rounded-2xl p-5 ring-1 ring-slate-200">
                                <div className="font-medium">
                                    TodoList Clone
                                </div>
                                <p className="text-slate-700 mt-1">
                                    Full-stack task manager with Flask API and React + Tailwind UI,
                                    JWT auth, CRUD tasks and labels
                                </p>
                                <div className="mt-2 flex gap-2 flex-wrap">
                                    <Pill>Flask</Pill> <Pill>React</Pill> <Pill>Tailwind</Pill> <Pill>JWT</Pill>
                                </div>
                        </div>
                        <div className="bg-white rounded-2xl p-5 ring-1 ring-slate-200">
                            <div className="font-medium">
                                Machine Learning Project IRIS 
                            </div>
                            <p className="text-slate-700 mt-1">
                                It's a machine learning project for classyfing the Iris dataset. The project is structured to support
                                development,testing and deployment using Dockers and CI/CD workflows
                            </p>
                            <div className="mt-2 flex gap-2">
                                <Pill>FastAPI</Pill> <Pill>Scikit-Learn</Pill> <Pill>Pandas</Pill> <Pill>NumPy</Pill> <Pill>Dockers</Pill> <Pill>MLFlow</Pill> 
                            </div>
                        </div>
                    </section>
                    <section id="volunteer_work" className="space-y-3">
                        <h2 className="text-xl py-2 font-semibold">Volunteer Work</h2>
                        <div className="space-y-3">
                            <div className="bg-white rounded-2xl p-5 ring-1 ring-slate-200">
                                <div className="flex items-center justify-between">
                                    <h3 className="font-medium text-lg">UniAI</h3>
                                    <span className="text-sm text-slate-500">October 2025 - Present</span>
                                </div>
                                <p className="mt-2 text-slate-700">
                                    Expertise member of the university artificial intelligence student community.
                                    Reading articles about AI and organizing different events and workshops
                                </p>
                            </div>
                        </div>
                        <div className="bg-white rounded-2xl p-5 ring-1 ring-slate-200">
                            <div className="flex items-center justify-between">
                                <h3 className="font-medium text lg">IEEE Student Branch</h3>
                                <span className="text-sm text-slate 500">July 2025 - Present</span>
                            </div>
                            <p className="mt-2 text-slate-700">
                                Active member of AI SG of the IEEE UniWA student organization, we organize events and projects related with AI
                            </p>
                        </div>
                    </section>
                    <section id="skills" className="space-y-3">
                        <h2 className="text-xl py-2 font-semibold">Skills</h2>
                        <div className="bg-white rounded-2xl p-5 ring-1 ring-slate-100">
                            <div className="font-medium mt-4">
                                Coding
                            </div>
                            <p className="text-slate-700 mt-1">
                                Python,HTML,JavaScript,SQL,XML/XSL,LaTeX
                            </p>
                            <div className="font-medium mt-4">Data Analysis & ML</div>
                            <p className="text-slate-700 mt-1">
                                Pandas,NumPy,Scikit-learn,OpenCV,PyTorch(basic),Tensorflow 
                            </p>
                            <div className="font-medium mt-4">
                                Visualization
                            </div>
                            <p className="text-slate-700 mt-1">
                                Seaborn,Matplotlib, Power BI
                            </p>
                            <div className="font-medium mt-4">Databases</div>
                            <p className="text-slate-700 mt-1">
                                MySQL,PostegreSQL
                            </p>
                            <div className="font-medium mt-4">Frameworks</div>
                            <p className="text-slate-700 mt-1">
                                Tailwind,Flask,FastAPI
                            </p>
                        </div>
                    </section>
                    <section id="languages" className="space-y-3">
                        <h2 className="text-xl py-2 font-semibold">Languages</h2>
                        <div className="bg-white rounded-2xl p-5 ring-1 ring-slate-100">
                            Greek (Native), English (C2), Spanish (B1)
                        </div>
                    </section>
                    <section id="certs" className="space-y-3">
                        <h2 className="text-xl py-2 font-semibold">Certificates</h2>
                        <div className="bg-white rounded-2xl ring-1 p-5 ring-slate-100">
                            <p className="text-slate-700">
                                Football Data Analyst - Workearly
                            </p>
                            <p className="text-slate-700">
                                Fundamentals of Deep Learning - NVIDIA 
                            </p>
                            <p className="text-slate-700">
                                Generative AI with Diffusion Models - NVIDIA
                            </p>
                        </div>
                    </section>
                </div>
            </div>
        </section>
    )
}