"use client";
import { useState } from "react";
import { Mail, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

type FormState = "idle" | "submitting" | "success" | "error";

export default function ContactForm() {
  const [state, setState] = useState<FormState>("idle");
  const [errorMsg, setErrorMsg] = useState<string>("");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErrorMsg("");
    setState("submitting");

    const form = e.currentTarget;
    const formData = new FormData(form);

    if (formData.get("website")) {
      setState("success");
      form.reset();
      return;
    }

    const name = String(formData.get("name") || "").trim();
    const email = String(formData.get("email") || "").trim();
    const message = String(formData.get("message") || "").trim();

    if (!name || !email || !message) {
      setState("error");
      setErrorMsg("Please fill in all required fields");
      return;
    }
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      setState("error");
      setErrorMsg("Please enter a valid email address.");
      return;
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);

    try {
      const base = process.env.NEXT_PUBLIC_API_BASE;
      if (!base) throw new Error("Missing NEXT_PUBLIC_API_BASE on Vercel");

      const res = await fetch(`${base}/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, message }),
        signal: controller.signal,
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) throw new Error(data?.message || data?.detail || `Request failed: ${res.status}`);
      if (data?.ok === false) throw new Error(data?.message || "Something went wrong");

      setState("success");
      form.reset();
    } catch (error: any) {
      setState("error");
      setErrorMsg(error?.name === "AbortError" ? "Request timed out. Try again." : (error?.message || "Something went wrong"));
    } finally {
      clearTimeout(timer);
    }
  }

  return (
    <form onSubmit={onSubmit} className="bg-white rounded-2xl p-6 ring-1 ring-slate-200 space-y-4">
      <div>
        <label className="text-sm text-slate-600" htmlFor="name">Name</label>
        <input type="text" required placeholder="Your Name" className="mt-1 w-full rounded-xl border px-3 py-2" name="name" id="name" />
      </div>

      <div>
        <label className="text-sm text-slate-600" htmlFor="email">Email</label>
        <input type="email" id="email" name="email" required placeholder="youremail@example.com" className="mt-1 w-full rounded-xl border px-3 py-2" />
      </div>

      <div>
        <label className="text-sm text-slate-600" htmlFor="message">Message</label>
        <textarea name="message" id="message" required placeholder="Tell about project, questions or collaborations" rows={5} className="mt-1 w-full rounded-xl border px-3 py-2" />
      </div>

      <input type="text" name="website" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />

      {state === "error" && (
        <div className="flex items-center gap-2 text-rose-600 text-sm">
          <AlertCircle size={16} /> {errorMsg || "Error sending message"}
        </div>
      )}
      {state === "success" && (
        <div className="flex items-center gap-2 text-emerald-600 text-sm">
          <CheckCircle2 size={16} /> Thanks! Your message has been sent.
        </div>
      )}

      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2 text-slate-500 text-sm">
          <Mail size={16} />
          <span>I'll reply via email.</span>
        </div>

        <button type="submit" disabled={state === "submitting"} className="inline-flex items-center gap-2 px-4 py-3 rounded-xl bg-slate-900 text-white hover:bg-slate-800 disabled:opacity-60">
          {state === "submitting" ? (<><Loader2 className="animate-spin" size={16} /> Sending...</>) : "Send"}
        </button>
      </div>
    </form>
  );
}