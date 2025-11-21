"use client";
import {useState} from "react";

type Role = "user" | "assistant";
interface ChatMessage{
    role: Role;
    content: string;
}

export default function AssistantPage(){
    const [messages,setMessages] = useState<ChatMessage[]>([
        {role:"assistant",content:"Hello! I'm your AI assistant. How can I help you today?"}
    ]);
    const [input,setInput] = useState("");
    const [loading,setLoading] = useState(false);

    async function handleSubmit(e:React.FormEvent){
        e.preventDefault();
        const trimmed = input.trim();
        if (!trimmed || loading) return;
        const newMessages:ChatMessage[] = [...messages,{role:"user",content:trimmed}];
        setMessages(newMessages);
        setInput("");
        setLoading(true);
        try{
            const base = process.env.NEXT_PUBLIC_API_BASE!;
            const res = await fetch(`${base}/api/assistant`,{
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({messages:newMessages})
            })
            if (!res.ok){
                throw new Error(`Error: ${res.status} ${res.statusText}`);
            }
            const data:{reply:string} = await res.json();
            setMessages([...newMessages,{role:"assistant",content:data.reply}]);
        }catch(err){
            setMessages([...newMessages,{role:"assistant",content:"Sorry, something went wrong. Please try again later."}]);
        }finally{
            setLoading(false);
        }
    }

    return (
        <section className="max-w-3xl mx-auto space-y-6">
            <header>
                <h1 className="text-3xl font-semibold">Assistant</h1>
                <p className="text-slate-600 mt-2">
                A small chatbot that knows about this portfolio, stack, and upcoming features.
                </p>
            </header>
            <div className="bg-white rounded-2xl p-4 ring-1 ring-slate-200 flex flex-col h-[400px]">
                <div className="flex-1 overflow-y-auto space-y-3 pr-1">
                    {messages.map((msg,idx)=>(
                        <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                            <div className={`max-w-[70%] p-3 rounded-lg ${msg.role === "user" ? "bg-indigo-600 text-white" : "bg-slate-100 text-slate-900"}`}>
                                {msg.content}
                            </div>
                        </div>
                    ))}
                    {loading &&(
                        <div className="mr-auto max-w-[80%] rounded-2xl px-3 py-2 text-sm bg-slate-100 text-slate-500">
                            Thinking...
                        </div>
                    )}
                </div>
                <form onSubmit={handleSubmit} className="mt-3 flex gap-2">
                    <input type="text" value={input} onChange={(e)=>setInput(e.target.value)} className="flex-1 rounded-2xl border px-3 py-2 text-sm" placeholder="Ask about projects,stack or CV plans..." />
                    <button type="submit" disabled={loading} className="rounded-2xl bg-slate-900 text-white px-4 py-2 text-sm disabled:opacity-60">Send</button>
                </form>
            </div>
        </section>
    )
}