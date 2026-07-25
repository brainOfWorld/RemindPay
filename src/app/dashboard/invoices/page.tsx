"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api, { Invoice } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import InvoiceTable from "@/components/InvoiceTable";

export default function InvoicesPage() {
  const router = useRouter();
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    customer_name: "",
    customer_email: "",
    customer_phone: "",
    amount: "",
    currency: "NGN",
    description: "",
    due_date: "",
    payment_gateway: "",
  });

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    try {
      const res = await api.get("/api/invoices/");
      setInvoices(res.data.invoices);
    } catch {
      router.push("/login");
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/api/invoices/", {
        ...form,
        amount: parseFloat(form.amount),
        due_date: new Date(form.due_date).toISOString(),
        payment_gateway: form.payment_gateway || null,
        customer_phone: form.customer_phone || null,
        description: form.description || null,
      });
      setShowForm(false);
      setForm({
        customer_name: "",
        customer_email: "",
        customer_phone: "",
        amount: "",
        currency: "NGN",
        description: "",
        due_date: "",
        payment_gateway: "",
      });
      fetchInvoices();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to create invoice");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this invoice?")) return;
    try {
      await api.delete(`/api/invoices/${id}`);
      fetchInvoices();
    } catch {
      alert("Failed to delete invoice");
    }
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar />
        <main className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Invoices</h2>
            <button
              onClick={() => setShowForm(!showForm)}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
            >
              {showForm ? "Cancel" : "+ New Invoice"}
            </button>
          </div>

          {showForm && (
            <form onSubmit={handleCreate} className="bg-white p-6 rounded-xl shadow-sm border mb-6">
              <div className="grid grid-cols-2 gap-4">
                <input
                  placeholder="Customer Name"
                  value={form.customer_name}
                  onChange={(e) => setForm({ ...form, customer_name: e.target.value })}
                  required
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  placeholder="Customer Email"
                  type="email"
                  value={form.customer_email}
                  onChange={(e) => setForm({ ...form, customer_email: e.target.value })}
                  required
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  placeholder="Phone (optional)"
                  value={form.customer_phone}
                  onChange={(e) => setForm({ ...form, customer_phone: e.target.value })}
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  placeholder="Amount"
                  type="number"
                  step="0.01"
                  value={form.amount}
                  onChange={(e) => setForm({ ...form, amount: e.target.value })}
                  required
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  placeholder="Due Date"
                  type="datetime-local"
                  value={form.due_date}
                  onChange={(e) => setForm({ ...form, due_date: e.target.value })}
                  required
                  className="px-4 py-2 border rounded-lg"
                />
                <select
                  value={form.payment_gateway}
                  onChange={(e) => setForm({ ...form, payment_gateway: e.target.value })}
                  className="px-4 py-2 border rounded-lg"
                >
                  <option value="">No Gateway</option>
                  <option value="paystack">Paystack</option>
                  <option value="flutterwave">Flutterwave</option>
                </select>
                <input
                  placeholder="Description (optional)"
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  className="px-4 py-2 border rounded-lg col-span-2"
                />
              </div>
              <button
                type="submit"
                className="mt-4 bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700"
              >
                Create Invoice
              </button>
            </form>
          )}

          <div className="bg-white rounded-xl shadow-sm border">
            {loading ? (
              <p className="p-6 text-gray-500">Loading...</p>
            ) : (
              <InvoiceTable
                invoices={invoices}
                onDelete={handleDelete}
                onRefresh={fetchInvoices}
              />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
