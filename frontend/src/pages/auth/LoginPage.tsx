import React, { useState } from "react";
import { AuthLayout } from "@/components/auth/AuthLayout";
import { PasswordInput } from "@/components/auth/PasswordInput";
import { GoogleAuthModal } from "@/components/auth/GoogleAuthModal";
import { useAuth } from "@/context/AuthContext";
import { Mail, Loader2, Sparkles, AlertCircle, ArrowRight, UserCheck } from "lucide-react";

interface LoginPageProps {
  onNavigate: (page: string) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onNavigate }) => {
  const { login, demoLoginPrince } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [demoLoading, setDemoLoading] = useState(false);
  const [googleModalOpen, setGoogleModalOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }
    if (!password) {
      setError("Please enter your password.");
      return;
    }

    setLoading(true);
    try {
      const res = await login(email.trim(), password, rememberMe);
      if (res.onboarding_completed) {
        onNavigate("dashboard");
      } else {
        onNavigate("onboarding");
      }
    } catch (err: any) {
      setError(err?.message || "Failed to log in. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoPrinceLogin = async () => {
    setError(null);
    setDemoLoading(true);
    try {
      const res = await demoLoginPrince();
      if (res.onboarding_completed) {
        onNavigate("dashboard");
      } else {
        onNavigate("onboarding");
      }
    } catch (err: any) {
      setError(err?.message || "Demo login failed.");
    } finally {
      setDemoLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Welcome back 👋"
      subtitle="Enter your academic credentials to access your autonomous plan."
      onBackToLanding={() => onNavigate("landing")}
    >
      {/* 1-Click Fast Demo Login for Prince Singh */}
      <div className="mb-5 rounded-2xl border border-primary/30 bg-gradient-to-r from-primary/15 via-indigo-500/10 to-purple-500/15 p-3.5 backdrop-blur-xs">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-white shadow-md shadow-primary/30">
              <UserCheck className="h-4 w-4" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <p className="text-xs font-bold text-white">Prince Singh</p>
                <span className="rounded-full bg-emerald-500/20 px-1.5 py-0.2 text-[9px] font-semibold text-emerald-400">
                  Demo Student
                </span>
              </div>
              <p className="text-[10px] text-slate-400">prince.singh@university.edu</p>
            </div>
          </div>
          <button
            type="button"
            onClick={handleDemoPrinceLogin}
            disabled={demoLoading || loading}
            className="flex items-center gap-1.5 rounded-xl bg-white px-3 py-1.5 text-xs font-bold text-slate-900 hover:bg-slate-100 transition-all shadow-sm active:scale-95 cursor-pointer disabled:opacity-50"
          >
            {demoLoading ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin text-primary" />
            ) : (
              <Sparkles className="h-3.5 w-3.5 text-primary" />
            )}
            <span>Fast Login</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-center gap-2 rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-xs text-rose-300">
          <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Email */}
        <div className="space-y-1.5">
          <label htmlFor="email-input" className="text-xs font-semibold text-slate-300">
            Email
          </label>
          <div className="relative">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
              <Mail className="h-4 w-4" />
            </div>
            <input
              id="email-input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="student@university.edu"
              required
              className="w-full rounded-xl border border-white/10 bg-white/5 pl-9 pr-3.5 py-2.5 text-sm text-white placeholder:text-slate-500 shadow-xs transition-all focus:border-primary focus:bg-white/10 focus:outline-hidden focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>

        {/* Password */}
        <PasswordInput
          id="login-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••••"
          required
          className="border-white/10 bg-white/5 text-white placeholder:text-slate-500 focus:bg-white/10"
        />

        {/* Remember me & Forgot password */}
        <div className="flex items-center justify-between text-xs">
          <label className="flex items-center gap-2 text-slate-400 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="h-4 w-4 rounded-md border-white/20 bg-white/5 text-primary focus:ring-primary/30"
            />
            Remember me
          </label>
          <button
            type="button"
            onClick={() => onNavigate("forgot-password")}
            className="font-medium text-primary-light hover:underline cursor-pointer"
          >
            Forgot password?
          </button>
        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={loading || demoLoading}
          className="w-full flex items-center justify-center gap-2 rounded-xl gradient-primary py-2.5 text-sm font-bold text-white shadow-lg shadow-primary/25 transition-all hover:shadow-xl hover:shadow-primary/40 active:scale-[0.99] disabled:opacity-60 cursor-pointer"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Authenticating...</span>
            </>
          ) : (
            <>
              <span>Log In</span>
              <ArrowRight className="h-4 w-4" />
            </>
          )}
        </button>

        {/* Divider */}
        <div className="relative my-4">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-white/10" />
          </div>
          <div className="relative flex justify-center text-[11px] uppercase tracking-wider">
            <span className="bg-slate-900 px-3 text-slate-500">Or continue with</span>
          </div>
        </div>

        {/* OAuth / Google */}
        <button
          type="button"
          onClick={() => setGoogleModalOpen(true)}
          className="w-full flex items-center justify-center gap-2.5 rounded-xl border border-white/15 bg-white/5 py-2.5 text-xs font-semibold text-slate-200 hover:bg-white/10 hover:border-white/25 transition-all cursor-pointer shadow-xs"
        >
          <svg className="h-4 w-4" viewBox="0 0 24 24">
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
          <span>Continue with Google</span>
        </button>

        {/* Register link */}
        <p className="text-center text-xs text-slate-400 pt-2">
          Don't have an account?{" "}
          <button
            type="button"
            onClick={() => onNavigate("register")}
            className="font-bold text-primary-light hover:underline cursor-pointer"
          >
            Create account
          </button>
        </p>
      </form>

      {/* Google Sign-in Modal */}
      <GoogleAuthModal
        isOpen={googleModalOpen}
        onClose={() => setGoogleModalOpen(false)}
        onSuccess={(onboardingCompleted) => {
          setGoogleModalOpen(false);
          if (onboardingCompleted) {
            onNavigate("dashboard");
          } else {
            onNavigate("onboarding");
          }
        }}
      />
    </AuthLayout>
  );
};
