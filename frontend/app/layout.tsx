import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: { default: "SKEC Digital Campus", template: "%s | SKEC" }, description: "Digital campus for Sri Krishna Engineering College", robots: { index: true, follow: true } };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="en"><body>{children}</body></html>; }
