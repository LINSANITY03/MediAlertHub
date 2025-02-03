import Image from "next/image";

export default function Home() {
  return (
    <div className="grid grid-rows-2:3fr 1fr h-screen">
      <div className="p-8 m-12 mb-40">
        <Image
          src="/logo.png"
          width={50}
          height={50}
          alt="Picture of e-surveillance logo"
        />
        <h1 className="text-7xl tracking-tighter">E-surveillance</h1>
      </div>
      <div className="p-8 bg-primary_green">
        <h2 className="text-3xl tracking-tighter">Services</h2>
        <ol className="underline p-4 inline-flex">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="size-6 mr-2"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3"
            />
          </svg>

          <ul>Provide the details of the diagnosed condition.</ul>
        </ol>
      </div>
    </div>
  );
}
