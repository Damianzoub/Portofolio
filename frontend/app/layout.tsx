import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../styles/globals.css";
import Header from "@/components/ui/Header";
import Footer from "@/components/ui/Footer";
import { describe } from "node:test";

export const metadata = {
  title: "Damianos Zoumpos - Portofolio",
  description: "Projects and blog posts by Damianos Zoumpos"
};

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const year = new Date().getUTCFullYear();

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-dvh flex flex-col">
          <Header/>
          <main className="flex-1 px-6 md:px-10 py-10 max-w-6xl mx-auto w-full">
            {children}
          </main>
          
          <Footer/>
      </body>
    </html>
  );
}
