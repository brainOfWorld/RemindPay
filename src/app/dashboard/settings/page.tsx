"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api, { User } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";

export default function SettingsPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [form, setForm] = useState({
    business_name: "",
    phone_number: "",
    paystack_secret_key: "",
    flutterwave_secret_key: "",
    whatsapp_phone_number_id: "",
    whatsapp_access_token: "",
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      const res = await api.get("/api/auth/me");
      setUser(res.data);
      setForm({
        business_name: res.data.business_name || "",
        phone_number: res.data.phone_number || "",
        paystack_secret_key: "",
        flutterwave_secret_key: "",
        whatsapp_phone_number_id: "",
        whatsapp_access_token: "",
      });
    } catch {
      router.push("/login");
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage("");

    try {
      const payload: Record<string, string> = {};
      Object.entries(form).forEach(([key, value]) => {
        if (value) payload[key] = value;
      });

      const res = await api.put("/api/auth/settings", payload);
      setUser(res.data);
      setMessage("Settings saved successfully");
      setForm((prev) => ({
        ...prev,
        paystack_secret_key: "",
        flutterwave_secret_key: "",
        whatsapp_phone_number_id: "",
        whatsapp_access_token: "",
      }));
    } catch (err: any) {
      setMessage(err.response?.data?.detail || "Failed to save settings");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar />
        <main className="p-6">
          <h2 className="text-2xl font-bold mb-6">Settings</h2>

          {message && (
            <div
              className={`p-3 rounded-lg mb-4 text-sm ${
                message.includes("success")
                  ? "bg-green-50 text-green-600"
                  : "bg-red-50 text-red-600"
              }`}
            >
              {message}
            </div>
          )}

          <form onSubmit={handleSave} className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h3 className="font-semibold mb-4">Business Info</h3>
              <div className="grid grid-cols-2 gap-4">
                <input
                  placeholder="Business Name"
                  value={form.business_name}
                  onChange={(e) => setForm({ ...form, business_name: e.target.value })}
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  placeholder="Phone Number"
                  value={form.phone_number}
                  onChange={(e) => setForm({ ...form, phone_number: e.target.value })}
                  className="px-4 py-2 border rounded-lg"
                />
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h3 className="font-semibold mb-4">Payment Gateways</h3>
              <div className="grid grid-cols-2 gap-4">
                <input
                  placeholder="Paystack Secret Key"
                  type="password"
                  value={form.paystack_secret_key}
                  onChange={(e) => setForm({ ...form, paystack_secret_key: e.target.value })}
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  placeholder="Flutterwave Secret Key"
                  type="password"
                  value={form.flutterwave_secret_key}
                  onChange={(e) => setForm({ ...form, flutterwave_secret_key: e.target.value })}
                  className="px-4 py-2 border rounded-lg"
                />
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h3 className="font-semibold mb-4">WhatsApp Cloud API</h3>
              <div className="grid grid-cols-2 gap-4">
                <input
                  placeholder="Phone Number ID"
                  value={form.whatsapp_phone_number_id}
                  onChange={(e) =>
                    setForm({ ...form, whatsapp_phone_number_id: e.target.value })
                  }
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  placeholder="Access Token"
                  type="password"
                  value={form.whatsapp_access_token}
                  onChange={(e) =>
                    setForm({ ...form, whatsapp_access_token: e.target.value })
                  }
                  className="px-4 py-2 border rounded-lg"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={saving}
              className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              {saving ? "Saving..." : "Save Settings"}
            </button>
          </form>
        </main>
      </div>
    </div>
  );
}
