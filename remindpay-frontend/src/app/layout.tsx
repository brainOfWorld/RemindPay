import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RemindPay - Automated Payment Reminders",
  description: "Automated WhatsApp payment reminders via Paystack & Flutterwave",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
