import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import "./global.css";

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
        {children}
      </body>
    </html>
  );
}
