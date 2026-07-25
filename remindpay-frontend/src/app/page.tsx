import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <nav className="flex justify-between items-center px-8 py-4 border-b">
        <h1 className="text-2xl font-bold text-primary-600">RemindPay</h1>
        <div className="space-x-4">
          <Link href="/login" className="text-gray-600 hover:text-gray-900">
            Login
          </Link>
          <Link
            href="/login"
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
          >
            Get Started
          </Link>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-8 py-20 text-center">
        <h2 className="text-5xl font-bold text-gray-900 mb-6">
          Never Lose Revenue to
          <br />
          <span className="text-primary-600">Forgotten Invoices</span>
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          RemindPay automatically sends WhatsApp payment reminders to your customers
          before, on, and after due dates. Integrates with Paystack and Flutterwave.
        </p>
        <div className="space-x-4">
          <Link
            href="/login"
            className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg hover:bg-primary-700 inline-block"
          >
            Start Free
          </Link>
        </div>

        <div className="mt-20 grid grid-cols-3 gap-8 text-left">
          <div className="p-6 bg-gray-50 rounded-xl">
            <div className="text-3xl mb-3">📱</div>
            <h3 className="font-semibold mb-2">WhatsApp Reminders</h3>
            <p className="text-sm text-gray-600">
              3-stage automated reminder sequence via WhatsApp Cloud API
            </p>
          </div>
          <div className="p-6 bg-gray-50 rounded-xl">
            <div className="text-3xl mb-3">💳</div>
            <h3 className="font-semibold mb-2">Payment Gateways</h3>
            <p className="text-sm text-gray-600">
              Paystack & Flutterwave integration with real-time webhook updates
            </p>
          </div>
          <div className="p-6 bg-gray-50 rounded-xl">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="font-semibold mb-2">Auto-Cancel</h3>
            <p className="text-sm text-gray-600">
              Reminders auto-cancel the moment a customer pays
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
