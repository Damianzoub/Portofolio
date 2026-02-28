import Link from "next/link";

export default function HomePage(){
  return (
    <section id="hero" className="min-h-screen flex items-center">
      <div className="container mx-auto px-6">
        <div className="flex flex-col space-y-6 md:w-2/3">
          <h1 className="text-4xl font-bold md:text-5xl">
            Hi, I'm <span className="text-indigo-700">Damianos Zoumpos</span>
          </h1>

          <p className="text-lg">
            A Machine Learning Engineer building data driven applications and sharing what I learn along the way.
          </p>

          <div className="flex space-x-4">
            <Link href="projects" className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
              View Projects
            </Link>

            <Link href="contact" className="px-6 py-3 border border-indigo-600 text-indigo-600 rounded-lg hover:bg-indigo-100 transition">
              Contact Me
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}
