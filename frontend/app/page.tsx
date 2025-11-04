import Link from "next/link";

export default function HomePage(){
  return (
    <section id="hero">
        <div className="container flex flex-col md:flex-row items-center px-6 mx-auto mt-32 space-y-0 md:space-y-0">
            {/*Left Item*/}
            <div className="flex flex-col mb-30 space-y-6 md:w-1/2">
              <h1 className="text-4xl font-bold text-center md:text-5xl md:text-left">
                Hi, I'm <span className="text-indigo-700">Damianos Zoumpos</span>
              </h1>
              <p className="text-lg text-center md:text-left">
                A Machine Learning Engineer building data driven applications and sharing what I learn along the way.
              </p>
              <div className="flex justify-center md:justify-start space-x-4">
                <Link href="#projects" className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
                  View Projects
                </Link>
                <Link href="#contact" className="px-6 py-3 border border-indigo-600 text-indigo-600 rounded-lg hover:bg-indigo-100 transition">
                  Contact Me
                </Link>
              </div>
            </div>
            {/*Right Item*/}
            <div className="md:w-1/2">
              <img src="" alt="Damianos Zoumpos Picture" />
            </div>
        </div>
    </section>
  )
}