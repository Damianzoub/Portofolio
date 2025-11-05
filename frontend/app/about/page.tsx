import Link from "next/link";

function Pill({children}: {children:React.ReactNode}){
    return (
        <span className="inline-flex items-center ronuded-full bg-slate-100 text-slate-700 text-xs px-2 py-0 5">
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

                    
                </div>
            </div>
        </section>
    )
}