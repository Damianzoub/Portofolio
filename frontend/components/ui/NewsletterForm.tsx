"use client";
import { useState } from "react";
import { Send } from "lucide-react";

export default function NewsletterForm(){
    const [email,setEmail] = useState("");
    const [state,setState] = useState<"idle"|"loading"|"success"|"error">('idle');
    const [errorMsg,setErrorMsg] = useState("");
    
    async function onSubmit(e: React.FormEvent<HTMLFormElement>){
        e.preventDefault();
        setErrorMsg('');
        if (!email.trim()){
            setState("error");
            setErrorMsg("Email is required")
            return;
        }

        setState("loading");

        try{
            const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"
            const res = await fetch(`${base}/newsletter`,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({email})
            })
            if(!res.ok){
                const data = await res.json().catch(()=> null);
                throw new Error(data?.message || "Failed to subscribe");
            }
            setState("success")
            setEmail("");
        }catch (err:any){
            setState("error");
            setErrorMsg(err?.message || "Something went wrong")
        }
    }

    return (
        <form onSubmit={onSubmit} className="flex gap-2">
            <input type="email" value={email} onChange={(e)=>{
                setEmail(e.target.value);
                if (state ==='error') setState('idle')
            }} placeholder="youremail@example.com" required className="flex-1 rounded-xl border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            <button type="submit" disabled={state==="loading"} className="rounded-xl bg-indigo-600 px-3 py-2 text-white hover:bg-indigo-700 transition">
                {state==="loading" ? "Subscribing..." : "Subscribe"}
                <Send size={16}/>
            </button>
            {state === "error" && (
                <p className="text-xs text-rose-600">{errorMsg || "Could not subscribe"}</p>
            )}
            {state === "success" && (
                <p className="text-xs text-emerald-600">Subscribed! You'll hear from me soon.</p>
            )}
        </form>
    )
}