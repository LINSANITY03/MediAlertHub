import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import "../global.css";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const robotoSans = Roboto({
  variable: "--font-roboto-sans",
  subsets: ["latin"],
  weight: "100"
});

export const metadata: Metadata = {
  title: "E-survillance",
  description: "Software used to collect detected diseases from different health posts across Nepal.",
  icons: {
    icon: "/logo.ico"
  }
};

/** 
 * RootLayout component wraps the entire application layout, including 
 * global metadata and font styles.
 * 
 * This layout applies the Roboto font (from Google Fonts), sets global metadata 
 * such as title, description, and icon, and renders the child components 
 * passed to it within the body of the page.
 * 
 * @param {React.ReactNode} children - The child components to be rendered inside the layout.
 * @returns {JSX.Element} The HTML layout structure with applied metadata, fonts, and children.
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${robotoSans.variable} antialiased`}
      >
        <main>
          {children}
        </main>
      <ToastContainer />
      </body>
    </html>
  );
}
