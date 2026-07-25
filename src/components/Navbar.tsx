"use client";

import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    router.push("/login");
  };

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center">
      <div />
      <button
        onClick={handleLogout}
        className="text-sm text-gray-600 hover:text-red-600 transition-colors"
      >
        Logout
      </button>
    </header>
  );
}
