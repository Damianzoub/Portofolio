"use client";
import { useState } from "react";
import { Send } from "lucide-react";

export default function NewsletterForm(){
    const [email,setEmail] = useState("");

    const onSubmit = (e: React.FormEvent<HTMLFormElement>) =>{
        e.preventDefault();
        setEmail("");
    }

    return (
        <form onSubmit={onSubmit} className="flex gap-2">
            <input type="email" value='email' onChange={(e)=> setEmail(e.target.value)} placeholder="youremail@example.com" required className="flex-1 rounded-xl border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            <button type="submit" className="rounded-xl bg-indigo-600 px-3 py-2 text-white hover:bg-indigo-700 transition">
                <Send size={16}/>
            </button>
        </form>
    )
}