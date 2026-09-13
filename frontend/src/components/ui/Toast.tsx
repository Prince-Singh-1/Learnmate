/**
 * Toast Notification System — Animated, non-intrusive floating alerts for autonomous actions.
 */

import React, { createContext, useContext, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, AlertTriangle, Info, XCircle, X } from "lucide-react";

export type ToastType = "success" | "warning" | "info" | "error";

export interface ToastItem {
  id: string;
  type: ToastType;
  title: string;
  message?: string;
  duration?: number;
}

interface ToastContextType {
  toast: (options: { type?: ToastType; title: string; message?: string; duration?: number }) => void;
  removeToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

const toastIcons = {
  success: CheckCircle2,
  warning: AlertTriangle,
  info: Info,
  error: XCircle,
};

const toastStyles = {
  success: "border-emerald-200 bg-white/95 text-emerald-950 shadow-emerald-500/10",
  warning: "border-amber-200 bg-white/95 text-amber-950 shadow-amber-500/10",
  info: "border-indigo-200 bg-white/95 text-indigo-950 shadow-indigo-500/10",
  error: "border-rose-200 bg-white/95 text-rose-950 shadow-rose-500/10",
};

const iconColors = {
  success: "text-emerald-500",
  warning: "text-amber-500",
  info: "text-indigo-500",
  error: "text-rose-500",
};

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = useCallback(
    ({
      type = "info",
      title,
      message,
      duration = 4000,
    }: {
      type?: ToastType;
      title: string;
      message?: string;
      duration?: number;
    }) => {
      const id = "t-" + Math.random().toString(36).substring(2, 9);
      const newToast: ToastItem = { id, type, title, message, duration };

      setToasts((prev) => [...prev.slice(-3), newToast]); // max 4 toasts

      if (duration > 0) {
        setTimeout(() => {
          removeToast(id);
        }, duration);
      }
    },
    [removeToast]
  );

  return (
    <ToastContext.Provider value={{ toast, removeToast }}>
      {children}
      {/* Toast container floating bottom right */}
      <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-2.5 max-w-sm pointer-events-none">
        <AnimatePresence>
          {toasts.map((t) => {
            const Icon = toastIcons[t.type];
            return (
              <motion.div
                key={t.id}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9, y: 10, transition: { duration: 0.15 } }}
                className={`pointer-events-auto flex items-start gap-3 rounded-2xl border p-3.5 backdrop-blur-xl shadow-xl transition-all ${toastStyles[t.type]}`}
              >
                <div className="flex-shrink-0 mt-0.5">
                  <Icon className={`h-5 w-5 ${iconColors[t.type]}`} />
                </div>
                <div className="flex-1 min-w-0 pr-1">
                  <h5 className="text-xs font-bold leading-tight">{t.title}</h5>
                  {t.message && <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">{t.message}</p>}
                </div>
                <button
                  onClick={() => removeToast(t.id)}
                  className="flex-shrink-0 p-1 text-slate-400 hover:text-slate-600 rounded-md transition-colors"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
};
