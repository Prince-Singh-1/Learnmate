import React, { useState } from "react";
import { AuthLayout } from "@/components/auth/AuthLayout";
import { PasswordInput } from "@/components/auth/PasswordInput";
import { api } from "@/lib/api";
import { Mail, KeyRound, CheckCircle2, ArrowLeft, ArrowRight, Loader2, AlertCircle } from "lucide-react";

interface ForgotPasswordPageProps {
  onNavigate: (page: string) => void;
}

export const ForgotPasswordPage: React.FC<ForgotPasswordPageProps> = ({ onNavigate }) => {
  const [step, setStep] = useState<"request" | "reset">("request");
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [devTokenNotice, setDevTokenNotice] = useState<string | null>(null);

  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setDevTokenNotice(null);

    if (!email.trim()) {
      setError("Please provide your registered email.");
      return;
    }

    setLoading(true);
    try {
      const res = await api.forgotPassword<any>({ email: email.trim() });
      if (res.dev_token) {
        setToken(res.dev_token);
        setDevTokenNotice(res.dev_token);
      }
      setStep("reset");
      setSuccessMsg("Password reset code generated. Enter your new password below.");
    } catch (err: any) {
      setError(err?.message || "Could not generate reset code for this email.");
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!token.trim()) {
      setError("Please provide the reset code.");
      return;
    }
    if (newPassword.length < 8) {
      setError("New password must be at least 8 characters long.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      await api.resetPassword({
        token: token.trim(),
        new_password: newPassword,
        confirm_password: confirmPassword,
      });
      setSuccessMsg("Your password has been successfully updated! You can now log in.");
      setTimeout(() => {
        onNavigate("login");
      }, 1500);
    } catch (err: any) {
      setError(err?.message || "Failed to reset password. Please verify the code.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      title={step === "request" ? "Reset Password 🔑" : "Create New Password"}
      subtitle={
        step === "request"
          ? "Enter your academic email to receive a password reset token."
          : "Choose a strong new password for your LearnMate account."
      }
      onBackToLanding={() => onNavigate("landing")}
    >
      {error && (
        <div className="mb-4 flex items-center gap-2 rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-xs text-rose-300">
          <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {successMsg && (
        <div className="mb-4 flex items-center gap-2 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3 text-xs text-emerald-300">
          <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
          <span>{successMsg}</span>
        </div>
      )}

      {step === "request" ? (
        <form onSubmit={handleRequestReset} className="space-y-4">
          <div className="space-y-1.5">
            <label htmlFor="reset-email" className="text-xs font-semibold text-slate-300">
              Account Email
            </label>
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                <Mail className="h-4 w-4" />
              </div>
              <input
                id="reset-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="prince.singh@university.edu"
                required
                className="w-full rounded-xl border border-white/10 bg-white/5 pl-9 pr-3.5 py-2.5 text-sm text-white placeholder:text-slate-500 shadow-xs transition-all focus:border-primary focus:bg-white/10 focus:outline-hidden focus:ring-2 focus:ring-primary/20"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 rounded-xl gradient-primary py-2.5 text-sm font-bold text-white shadow-lg shadow-primary/25 transition-all hover:shadow-xl hover:shadow-primary/40 active:scale-[0.99] disabled:opacity-60 cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Sending Reset Request...</span>
              </>
            ) : (
              <>
                <span>Request Password Reset</span>
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>

          <div className="pt-2 text-center">
            <button
              type="button"
              onClick={() => onNavigate("login")}
              className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-white transition-colors cursor-pointer"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Return to login
            </button>
          </div>
        </form>
      ) : (
        <form onSubmit={handleResetPassword} className="space-y-4">
          {devTokenNotice && (
            <div className="rounded-xl border border-primary/30 bg-primary/10 p-3 text-[11px] text-slate-300">
              <span className="font-semibold text-primary-light">Development Reset Code:</span>{" "}
              <code className="rounded bg-black/40 px-1.5 py-0.5 font-mono text-white">{devTokenNotice}</code>
              <p className="mt-1 text-[10px] text-slate-400">
                (Auto-populated below for seamless prototype demonstration)
              </p>
            </div>
          )}

          <div className="space-y-1.5">
            <label htmlFor="reset-token" className="text-xs font-semibold text-slate-300">
              Reset Token / Code
            </label>
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                <KeyRound className="h-4 w-4" />
              </div>
              <input
                id="reset-token"
                type="text"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Paste your reset token"
                required
                className="w-full rounded-xl border border-white/10 bg-white/5 pl-9 pr-3.5 py-2.5 text-sm text-white placeholder:text-slate-500 shadow-xs transition-all focus:border-primary focus:bg-white/10"
              />
            </div>
          </div>

          <PasswordInput
            id="new-pass"
            label="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            placeholder="At least 8 characters"
            required
            className="border-white/10 bg-white/5 text-white placeholder:text-slate-500 focus:bg-white/10"
          />

          <PasswordInput
            id="confirm-new-pass"
            label="Confirm New Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Re-enter new password"
            required
            className="border-white/10 bg-white/5 text-white placeholder:text-slate-500 focus:bg-white/10"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 rounded-xl gradient-primary py-2.5 text-sm font-bold text-white shadow-lg shadow-primary/25 transition-all hover:shadow-xl hover:shadow-primary/40 active:scale-[0.99] disabled:opacity-60 cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Updating Password...</span>
              </>
            ) : (
              <>
                <span>Set New Password & Log In</span>
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>

          <div className="pt-2 text-center">
            <button
              type="button"
              onClick={() => onNavigate("login")}
              className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-white transition-colors cursor-pointer"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Return to login
            </button>
          </div>
        </form>
      )}
    </AuthLayout>
  );
};
