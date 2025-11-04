"use client";
import React, {useEffect,useRef,useState} from "react";
import {X} from "lucide-react";
import {createPortal} from "react-dom";
import { createECDH } from "crypto";

type ModalProps ={
    open: boolean;
    onClose: ()=> void;
    title?: string;
    children: React.ReactNode;
    widthClass?:string;
};

export default function Modal({
    open,onClose,title,children,widthClass="max-w-lg"
}:ModalProps){
    const [mounted,setMounted] = useState(false);
    const dialogRef = useRef<HTMLDivElement>(null);

    useEffect(()=>setMounted(true),[]);

    //close on ESC
    useEffect(()=>{
        if(!open) return;
        const onKey= (e:KeyboardEvent)=>{
            if(e.key === "Escape"){
                onClose();
            }
        }
        window.addEventListener("keydown",onKey);
        return ()=> window.removeEventListener("keydown",onKey);
    },[open,onClose]);

    //focus trap
    useEffect(()=>{
        if (!open || !dialogRef.current ) return;
        const el = dialogRef.current;
        const focusable = el.querySelectorAll<HTMLElement>(
            'button,[href],input,textarea,select,[tabindex]:not([tabindex="-1"])'
        );
        focusable[0]?.focus();
    },[open])

    if (!mounted) return null;
    return open ? createPortal(
        <div arial-model='true' role='dialog' className="fixed inset-0 z-50 flex items-center justify-center">
            <div onClick={onClose} className="absolute inset-0 bg-black/40">
                <div ref={dialogRef}             className={`relative z-10 w-full ${widthClass} mx-4 rounded-2xl bg-white shadow-xl ring-1 ring-slate-200`}
                >
                    <div className="flex items-center justify-between px-5 py-4 border-b">
                        <h3 className="text-lg font-semibold">{title}</h3>
                        <button aria-label="Close Modal" onClick={onClose} className="p-2 rounded-lg hover:bg-slate-100">
                            <X size={15}/>
                        </button>
                    </div>
                    <div className="p-5">{children}</div>
                </div>
            </div>
        </div>,
        document.body
    ) : null;
}