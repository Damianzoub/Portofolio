import ContactForm from "@/components/forms/ContactForm"


export const metadata ={
    title: "Contact- Damianos Zoumpos",
    description: "Get in touch for collaboration, roles or questions"
};

export default function ContactPage(){
    return (
        <section className="max-w-xl mx-auto space-y-6">
            <h1 className="text-3xl font-semibold">
                Contact Me 
            </h1>
            <p className="text-slate-700">
                Reach out for collaborations, roles or questions. I usually respond within 2 days
            </p>
            <ContactForm/>
        </section>
    )
}