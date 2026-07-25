"use client";

import { Invoice } from "@/lib/api";
import StatusBadge from "./StatusBadge";

interface Props {
  invoices: Invoice[];
  onDelete: (id: string) => void;
  onRefresh: () => void;
}

export default function InvoiceTable({ invoices, onDelete, onRefresh }: Props) {
  if (invoices.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No invoices found. Create your first invoice above.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200 text-left text-gray-500">
            <th className="py-3 px-4">Customer</th>
            <th className="py-3 px-4">Amount</th>
            <th className="py-3 px-4">Status</th>
            <th className="py-3 px-4">Gateway</th>
            <th className="py-3 px-4">Due Date</th>
            <th className="py-3 px-4">Actions</th>
          </tr>
        </thead>
        <tbody>
          {invoices.map((inv) => (
            <tr key={inv.id} className="border-b border-gray-100 hover:bg-gray-50">
              <td className="py-3 px-4">
                <div>
                  <p className="font-medium">{inv.customer_name}</p>
                  <p className="text-xs text-gray-500">{inv.customer_email}</p>
                </div>
              </td>
              <td className="py-3 px-4 font-medium">
                {inv.currency} {inv.amount.toLocaleString()}
              </td>
              <td className="py-3 px-4">
                <StatusBadge status={inv.status} />
              </td>
              <td className="py-3 px-4 text-gray-500">
                {inv.payment_gateway || "-"}
              </td>
              <td className="py-3 px-4 text-gray-500">
                {new Date(inv.due_date).toLocaleDateString()}
              </td>
              <td className="py-3 px-4">
                <button
                  onClick={() => onDelete(inv.id)}
                  className="text-red-500 hover:text-red-700 text-xs"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
