import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import Image from "next/image";
import "../global.css";

const robotoSans = Roboto({
  variable: "--font-roboto-sans",
  subsets: ["latin"],
  weight: "100",
});

export const metadata: Metadata = {
  title: "Verify your details",
  icons: {
    icon: "/logo.ico",
  },
};

export default function VerifyLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${robotoSans.variable} antialiased`}>
        <nav className="flex shadow-lg p-6 items-center w-full h-32 min-h-32 fixed top-0 z-10">
          {/* logo */}
          <Image
            src="/logo.png"
            width={85}
            height={79}
            alt="Picture of e-surveillance logo"
            className="ml-10"
          />
          {/* website title */}
          <h1 className="tracking-tighter text-4xl ml-8">E-survillance</h1>
        </nav>
        <main className="mt-40 z-0">{children}</main>
      </body>
    </html>
  );
}
