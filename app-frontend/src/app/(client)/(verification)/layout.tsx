import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import Image from "next/image";
import "../global.css";
import ApolloWrapper from "@/services/ApolloProvider";
import { ToastContainer } from 'react-toastify';

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

/**
 * VerifyLayout component wraps the "Verify your details" page layout, 
 * providing global styles, metadata, and application context such as Apollo Client 
 * and toast notifications.
 *
 * This layout includes a fixed navigation bar with a logo and title, 
 * and renders its children below the navbar inside the main content area.
 *
 * @param {object} props
 * @param {React.ReactNode} props.children - The components to be rendered inside the layout.
 * @returns {JSX.Element} The layout structure including navbar, content area, and toast container.
 */
export default function VerifyLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${robotoSans.variable} antialiased`}>
        <nav className="flex shadow-lg p-6 items-center w-full h-32 min-h-32 fixed top-0 z-50 bg-white">
          <Image
            src="/logo.png"
            width={85}
            height={79}
            alt="Picture of e-surveillance logo"
            className="ml-10"
          />

          <h1 className="tracking-tighter text-4xl ml-8">E-survillance</h1>
        </nav>
        <main className="pt-40">
          <ApolloWrapper>{children}</ApolloWrapper>
        </main>
        <ToastContainer />
      </body>
    </html>
  );
}
