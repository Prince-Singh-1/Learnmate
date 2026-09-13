import React from "react";
import { motion } from "framer-motion";
import { Brain, Sparkles, ShieldCheck, Zap, ArrowLeft } from "lucide-react";

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  onBackToLanding?: () => void;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({
  children,
  title,
  subtitle,
  onBackToLanding,
}) => {
  return (
    <div className="relative min-h-screen w-full flex items-center justify-center bg-slate-950 px-4 py-8 overflow-hidden font-sans">
      {/* Dynamic Background Glow Elements */}
      <div className="pointer-events-none absolute -top-40 -left-40 h-96 w-96 rounded-full bg-indigo-500/20 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-40 -right-40 h-96 w-96 rounded-full bg-purple-500/20 blur-3xl" />
      <div className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[600px] w-[600px] rounded-full bg-primary/10 blur-[120px]" />

      {/* Grid Pattern Overlay */}
      <div
        className="pointer-events-none absolute inset-0 opacity-15"
        style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0)`,
          backgroundSize: "28px 28px",
        }}
      />

      <div className="relative z-10 w-full max-w-5xl">
        {/* Top bar return to landing button */}
        {onBackToLanding && (
          <div className="mb-6">
            <button
              onClick={onBackToLanding}
              className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-white/10 hover:text-white transition-all cursor-pointer backdrop-blur-xs"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Back to Overview
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* Left Hero Pitch (Desktop) */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4 }}
            className="hidden lg:flex lg:col-span-5 flex-col justify-center space-y-6 pr-4"
          >
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl gradient-primary shadow-lg shadow-primary/30">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <span className="text-xl font-black tracking-tight text-white">Learn<span className="text-primary-light">Mate</span></span>
                <span className="block text-[10px] font-semibold uppercase tracking-wider text-primary-light">Autonomous Learning Planner</span>
              </div>
            </div>

            <div className="space-y-2">
              <h1 className="text-3xl font-extrabold text-white tracking-tight leading-tight">
                Self-driving study plans powered by AI.
              </h1>
              <p className="text-sm text-slate-400 leading-relaxed">
                Continuous performance analysis, automated calendar replanning, and targeted knowledge gap remediation.
              </p>
            </div>

            {/* Micro Feature highlights */}
            <div className="space-y-3 pt-2">
              <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 p-3 backdrop-blur-xs">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/20 text-emerald-400">
                  <Zap className="h-4 w-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">Autonomous Replanning</h4>
                  <p className="text-[11px] text-slate-400">Recalculates schedules when you miss a session</p>
                </div>
              </div>

              <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 p-3 backdrop-blur-xs">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/20 text-indigo-400">
                  <Sparkles className="h-4 w-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">Knowledge Gap Detection</h4>
                  <p className="text-[11px] text-slate-400">Identifies weak topics before exams</p>
                </div>
              </div>

              <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 p-3 backdrop-blur-xs">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-purple-500/20 text-purple-400">
                  <ShieldCheck className="h-4 w-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">Deterministic Verification</h4>
                  <p className="text-[11px] text-slate-400">Ensures revised plan satisfies goal deadlines</p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Right Card (Form container) */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
            className="lg:col-span-7 w-full max-w-md mx-auto lg:max-w-none"
          >
            <div className="rounded-3xl border border-white/15 bg-slate-900/80 p-6 sm:p-8 backdrop-blur-xl shadow-2xl shadow-black/50">
              {/* Mobile Logo View */}
              <div className="flex lg:hidden items-center gap-2.5 mb-6">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl gradient-primary">
                  <Brain className="h-5 w-5 text-white" />
                </div>
                <div>
                  <span className="text-lg font-black text-white">Learn<span className="text-primary-light">Mate</span></span>
                  <span className="block text-[9px] font-semibold uppercase tracking-wider text-slate-400">Autonomous Planner</span>
                </div>
              </div>

              <div className="mb-6">
                <h2 className="text-xl font-bold text-white tracking-tight">{title}</h2>
                {subtitle && <p className="mt-1 text-xs text-slate-400">{subtitle}</p>}
              </div>

              {children}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
