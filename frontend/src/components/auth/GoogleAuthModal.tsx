import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Loader2, UserPlus, CheckCircle2 } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

interface GoogleAuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (onboardingCompleted: boolean) => void;
}

export const GoogleAuthModal: React.FC<GoogleAuthModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const { googleLogin } = useAuth();
  const [loadingEmail, setLoadingEmail] = useState<string | null>(null);
  const [customMode, setCustomMode] = useState(false);
  const [customName, setCustomName] = useState("");
  const [customEmail, setCustomEmail] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSelectAccount = async (account: {
    email: string;
    name: string;
    avatar: string;
  }) => {
    setError(null);
    setLoadingEmail(account.email);
    try {
      const res = await googleLogin({
        email: account.email,
        full_name: account.name,
        avatar_url: account.avatar,
      });
      onSuccess(res.onboarding_completed);
    } catch (err: any) {
      setError(err?.message || "Google sign-in failed. Please try again.");
      setLoadingEmail(null);
    }
  };

  const handleCustomSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customEmail.trim() || !customEmail.includes("@")) {
      setError("Please enter a valid Google email address.");
      return;
    }
    handleSelectAccount({
      email: customEmail.trim(),
      name: customName.trim() || customEmail.split("@")[0],
      avatar: "/prince-avatar.jpg",
    });
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/65 backdrop-blur-xs"
          />

          {/* Modal Container */}
          <motion.div
            initial={{ scale: 0.95, opacity: 0, y: 15 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.95, opacity: 0, y: 15 }}
            className="relative z-10 w-full max-w-md overflow-hidden rounded-3xl border border-slate-200 bg-white p-6 sm:p-7 shadow-2xl font-sans"
          >
            {/* Close Button */}
            <button
              onClick={onClose}
              className="absolute right-4 top-4 rounded-full p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors cursor-pointer"
            >
              <X className="h-4 w-4" />
            </button>

            {/* Google Header */}
            <div className="text-center space-y-1.5 pb-5 border-b border-slate-100">
              <div className="mx-auto flex h-10 w-10 items-center justify-center">
                <svg className="h-7 w-7" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.16 0 9.98 0 12s.45 3.84 1.25 5.42l4.03-3.15z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-slate-900">Sign in with Google</h3>
              <p className="text-xs text-slate-500">to continue to <strong className="text-slate-800">LearnMate</strong></p>
            </div>

            {error && (
              <div className="mt-4 rounded-xl bg-rose-50 border border-rose-200 p-2.5 text-xs text-rose-700">
                {error}
              </div>
            )}

            {!customMode ? (
              <div className="mt-5 space-y-2.5">
                <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                  Select Google account
                </p>

                {/* Profile 1: Prince Singh */}
                <button
                  type="button"
                  onClick={() =>
                    handleSelectAccount({
                      name: "Prince Singh",
                      email: "prince.singh@university.edu",
                      avatar: "/prince-avatar.jpg",
                    })
                  }
                  disabled={Boolean(loadingEmail)}
                  className="w-full flex items-center justify-between rounded-2xl border border-slate-200 p-3 hover:bg-slate-50 hover:border-slate-300 transition-all text-left cursor-pointer disabled:opacity-50 group"
                >
                  <div className="flex items-center gap-3">
                    <img
                      src="/prince-avatar.jpg"
                      alt="Prince Singh"
                      className="h-10 w-10 rounded-full object-cover border border-slate-200"
                    />
                    <div>
                      <div className="flex items-center gap-1.5">
                        <p className="text-xs font-bold text-slate-900 group-hover:text-primary transition-colors">
                          Prince Singh
                        </p>
                        <span className="rounded bg-indigo-50 border border-indigo-100 px-1.5 py-0.2 text-[9px] font-semibold text-primary">
                          Verified
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500">prince.singh@university.edu</p>
                    </div>
                  </div>

                  {loadingEmail === "prince.singh@university.edu" ? (
                    <Loader2 className="h-4 w-4 animate-spin text-primary" />
                  ) : (
                    <CheckCircle2 className="h-4 w-4 text-slate-300 group-hover:text-primary transition-colors" />
                  )}
                </button>

                {/* Profile 2: Demo University Scholar */}
                <button
                  type="button"
                  onClick={() =>
                    handleSelectAccount({
                      name: "Maya Lin",
                      email: "maya.lin@gmail.com",
                      avatar: "/prince-avatar.jpg",
                    })
                  }
                  disabled={Boolean(loadingEmail)}
                  className="w-full flex items-center justify-between rounded-2xl border border-slate-200 p-3 hover:bg-slate-50 hover:border-slate-300 transition-all text-left cursor-pointer disabled:opacity-50 group"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100 font-bold text-purple-700 text-xs">
                      ML
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-900 group-hover:text-primary transition-colors">
                        Maya Lin
                      </p>
                      <p className="text-[11px] text-slate-500">maya.lin@gmail.com</p>
                    </div>
                  </div>

                  {loadingEmail === "maya.lin@gmail.com" ? (
                    <Loader2 className="h-4 w-4 animate-spin text-primary" />
                  ) : (
                    <CheckCircle2 className="h-4 w-4 text-slate-300 group-hover:text-primary transition-colors" />
                  )}
                </button>

                {/* Custom Google Account Toggle */}
                <button
                  type="button"
                  onClick={() => setCustomMode(true)}
                  disabled={Boolean(loadingEmail)}
                  className="w-full flex items-center gap-3 rounded-2xl border border-dashed border-slate-300 p-3 hover:bg-slate-50 hover:border-slate-400 transition-all text-left cursor-pointer text-slate-600"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 text-slate-500">
                    <UserPlus className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-slate-800">Use another Google account</p>
                    <p className="text-[11px] text-slate-400">Sign in with any university or Google email</p>
                  </div>
                </button>
              </div>
            ) : (
              <form onSubmit={handleCustomSubmit} className="mt-5 space-y-3">
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-700">Full Name</label>
                  <input
                    type="text"
                    value={customName}
                    onChange={(e) => setCustomName(e.target.value)}
                    placeholder="e.g. Jordan Lee"
                    className="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs text-slate-900 focus:border-primary focus:outline-hidden"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-700">Google Email</label>
                  <input
                    type="email"
                    required
                    value={customEmail}
                    onChange={(e) => setCustomEmail(e.target.value)}
                    placeholder="jordan.lee@gmail.com"
                    className="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs text-slate-900 focus:border-primary focus:outline-hidden"
                  />
                </div>

                <div className="flex items-center gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setCustomMode(false)}
                    className="flex-1 rounded-xl border border-slate-200 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    disabled={Boolean(loadingEmail)}
                    className="flex-1 rounded-xl gradient-primary py-2 text-xs font-bold text-white shadow-xs hover:shadow-md cursor-pointer disabled:opacity-50"
                  >
                    {loadingEmail ? "Signing in..." : "Continue"}
                  </button>
                </div>
              </form>
            )}

            <div className="mt-6 pt-4 border-t border-slate-100 text-center">
              <p className="text-[11px] text-slate-400">
                To continue, Google will share your name, email address, and profile picture with LearnMate.
              </p>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
