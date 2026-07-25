# RemindPay Frontend

## Prerequisites
- Node.js 18+
- npm or yarn

## Quick Start

### 1. Install dependencies
```bash
cd remindpay-frontend
npm install
```

### 2. Configure environment
Edit `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. Start development server
```bash
npm run dev
```
Frontend at: http://localhost:3000

## Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/login` | Login / Register |
| `/dashboard` | Overview (paid/pending/overdue stats) |
| `/dashboard/invoices` | Create & manage invoices |
| `/dashboard/settings` | API keys & WhatsApp config |

## Project Structure

```
src/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Landing page
│   ├── globals.css             # Tailwind imports
│   ├── login/page.tsx          # Auth page
│   └── dashboard/
│       ├── page.tsx            # Stats overview
│       ├── invoices/page.tsx   # Invoice CRUD
│       └── settings/page.tsx   # User settings
├── components/
│   ├── Sidebar.tsx             # Navigation sidebar
│   ├── Navbar.tsx              # Top bar + logout
│   ├── InvoiceTable.tsx        # Invoice data table
│   └── StatusBadge.tsx         # Status pill component
└── lib/
    └── api.ts                  # Axios client + TypeScript interfaces
```

## Build for Production
```bash
npm run build
npm start
```
