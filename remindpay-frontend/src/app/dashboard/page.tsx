"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api, { Stats } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";

export default function DashboardPage() {
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/login";
      return;
    }
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get("/api/invoices/stats");
      setStats(res.data);
    } catch {
      router.push("/login");
    }
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar />
        <main className="p-6">
          <h2 className="text-2xl font-bold mb-6">Dashboard Overview</h2>

          {stats && (
            <div className="grid grid-cols-4 gap-4 mb-8">
              <div className="bg-white p-6 rounded-xl shadow-sm border">
                <p className="text-sm text-gray-500">Total Invoices</p>
                <p className="text-3xl font-bold">{stats.total_invoices}</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border">
                <p className="text-sm text-gray-500">Paid</p>
                <p className="text-3xl font-bold text-green-600">{stats.paid}</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border">
                <p className="text-sm text-gray-500">Pending</p>
                <p className="text-3xl font-bold text-yellow-600">{stats.pending}</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border">
                <p className="text-sm text-gray-500">Overdue</p>
                <p className="text-3xl font-bold text-red-600">{stats.overdue}</p>
              </div>
            </div>
          )}

          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <p className="text-sm text-gray-500 mb-1">Total Revenue</p>
            <p className="text-4xl font-bold text-primary-600">
              NGN {(stats?.total_revenue || 0).toLocaleString()}
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}
