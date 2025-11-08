import {
    Github,Linkedin,Instagram,Mail,Send
} from "lucide-react";
import NewsletterForm from "./NewsletterForm";
export default function Footer(){
    const year = new Date().getUTCFullYear();
    return (
        <footer className="w-full border-t text-slate-500 mt-10">
            <div className="flex flex-col-reverse justify-between text-slate-500 px-6 py-10 space-y-8 md:flex-row md:space-y-0 w-full">
                {/**Left Element */}
                <div className="flex flex-col space-y-6 text-left md:w-1/2">
                   <div className="pt-6">
                        <p>  Machine Learning Engineer • Building data driven applications and sharing what I learn along the way</p>
                   </div>
                   <div className="space-y-3">
                        <h4 className="text-sm font-medium text-slate-800 uppercase tracking-wide">
                            Newsletter
                        </h4>
                        <NewsletterForm/>
                   </div>
                </div>
                <div className="flex justify-between md:px-4  space-x-6 md:w-1/2">
                    <div className="space-y-3 md:justify-self-end">
                        <h4 className="text-sm font-medium text-slate-800 uppercase tracking-wide">
                            Connect
                        </h4>
                        <div className="flex gap-4 text-slate-500">
                            <a href="https://github.com/Damianxoub" target="_blank" className="hover:text-slate-900">
                                <Github size={20}/>
                            </a>
                            <a href="https://www.linkedin.com/in/damianos-zoumpos-980476269/" target="_blank" className="hover:text-slate-900">
                                <Linkedin size={20}/>
                            </a>
                            <a target="_blank" href="https://www.instagram.com/damian_zoub/" className="hover:text-slate-900">
                                <Instagram size={20}/>
                            </a>
                            <a href="mailto:d.zoumpos04@gmail.com" className="hover:text-slate-900">
                                <Mail size={20}/>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <div className="border-t text-center py-6 text-sm text-slate-500">
                &copy; {year} Damian Zoub • All rights reserved.
            </div>
        </footer>
    )
}