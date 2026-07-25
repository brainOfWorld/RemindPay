import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;

export interface User {
  id: string;
  email: string;
  business_name: string;
  phone_number: string | null;
  is_active: boolean;
  created_at: string;
}

export interface Invoice {
  id: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string | null;
  amount: number;
  currency: string;
  description: string | null;
  reference: string | null;
  status: string;
  payment_gateway: string | null;
  payment_link: string | null;
  due_date: string;
  paid_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Reminder {
  id: string;
  stage: number;
  scheduled_at: string | null;
  sent_at: string | null;
  status: string;
  message_content: string | null;
  whatsapp_message_id: string | null;
  error_message: string | null;
  created_at: string;
}

export interface Stats {
  total_invoices: number;
  paid: number;
  pending: number;
  overdue: number;
  total_revenue: number;
}
