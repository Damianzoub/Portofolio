"use client";
import Link from "next/link";
import { usePathname} from "next/navigation";

const nav= [
    {href:'/',label:"Home"},
    {href:'/projects',label:"Projects"},
    {href:'/blog',label:"Blog"},
    {href:'/about',label:"About"},
    {href:'/contact',label:"Contact"}
]

export default function Header(){
    const pathname = usePathname();

    return (
        <header className="sticky top-0 bg-white/70 backdrop-blur-md border-b border-gray-200 z-50">
            <div className="max-w-6xl mx-auto px-6 md:px-10 h-16 flex items-center justify-between">
                <Link href='/' className="font-semibold tracking-tight hover:underline underline-offset-4">
                    Damianos Zoumpos
                </Link>
                <nav className="flex gap-4">
                    {nav.map((item)=>{
                        const isActive = pathname === item.href; 
                        return (
                            <Link 
                                key={item.href} 
                                href={item.href} 
                                className={`hover:underline underline-offset-4 ${isActive ? 'font-semibold' : 'font-normal text-gray-600'}`}
                            >
                                {item.label}
                            </Link>
                        )
                    })}
                </nav>
            </div>
        </header>
    )
}