import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  Brain,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
  Bot,
  UserCheck,
  Loader2,
  ChevronRight,
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";

interface LandingPageProps {
  onNavigate: (page: string) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate }) => {
  const { demoLoginPrince } = useAuth();
  const [fastLoginLoading, setFastLoginLoading] = useState(false);

  const handleFastDemoLogin = async () => {
    setFastLoginLoading(true);
    try {
      const res = await demoLoginPrince();
      if (res.onboarding_completed) {
        onNavigate("dashboard");
      } else {
        onNavigate("onboarding");
      }
    } catch {
      onNavigate("login");
    } finally {
      setFastLoginLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full bg-slate-950 text-white font-sans overflow-x-hidden selection:bg-primary/30">
      {/* Background Ambient Glows */}
      <div className="pointer-events-none absolute -top-48 left-1/2 -translate-x-1/2 h-[550px] w-[800px] rounded-full bg-indigo-600/20 blur-[140px]" />
      <div className="pointer-events-none absolute top-[600px] -left-48 h-96 w-96 rounded-full bg-purple-600/15 blur-[120px]" />
      <div className="pointer-events-none absolute top-[900px] -right-48 h-96 w-96 rounded-full bg-blue-600/15 blur-[120px]" />

      {/* Grid Pattern */}
      <div
        className="pointer-events-none absolute inset-0 opacity-10"
        style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255,255,255,0.2) 1px, transparent 0)`,
          backgroundSize: "32px 32px",
        }}
      />

      {/* Navigation Header */}
      <header className="relative z-20 mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl gradient-primary shadow-lg shadow-primary/30">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <div>
            <span className="text-xl font-black tracking-tight text-white">
              Learn<span className="text-primary-light">Mate</span>
            </span>
            <span className="hidden sm:inline-block ml-2 rounded-full border border-primary/30 bg-primary/10 px-2 py-0.5 text-[10px] font-bold text-primary-light uppercase tracking-wider">
              Autonomous Planner
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => onNavigate("login")}
            className="rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-xs font-semibold text-white hover:bg-white/10 transition-all cursor-pointer"
          >
            Log In
          </button>
          <button
            onClick={() => onNavigate("register")}
            className="rounded-xl gradient-primary px-4 py-2 text-xs font-bold text-white shadow-md shadow-primary/25 hover:shadow-lg hover:shadow-primary/40 transition-all cursor-pointer"
          >
            Get Started
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 mx-auto max-w-7xl px-6 pt-12 pb-24 lg:pt-16">
        <div className="text-center max-w-3xl mx-auto space-y-6">
          {/* Tag badge */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3.5 py-1.5 text-xs font-semibold text-primary-light shadow-xs"
          >
            <Sparkles className="h-3.5 w-3.5" />
            <span>Autonomous Learning Planner & Adaptive Reasoning Engine</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight"
          >
            Stop following static timetables.{" "}
            <span className="bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 bg-clip-text text-transparent">
              Learn with an autonomous pilot.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-base sm:text-lg text-slate-300 leading-relaxed"
          >
            LearnMate continuously analyzes your performance, identifies hidden knowledge gaps, and dynamically recalculates your study calendar when life happens.
          </motion.p>

          {/* Primary Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2"
          >
            <button
              onClick={() => onNavigate("register")}
              className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-2xl gradient-primary px-7 py-3.5 text-sm font-bold text-white shadow-xl shadow-primary/30 hover:shadow-2xl hover:shadow-primary/50 transition-all active:scale-95 cursor-pointer"
            >
              <span>Get Started</span>
              <ArrowRight className="h-4 w-4" />
            </button>

            <button
              onClick={() => onNavigate("login")}
              className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-2xl border border-white/20 bg-white/10 px-7 py-3.5 text-sm font-semibold text-white hover:bg-white/15 transition-all backdrop-blur-xs cursor-pointer"
            >
              <span>Log In</span>
            </button>
          </motion.div>

          {/* Fast Demo Showcase Card for Prince Singh */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
            className="mt-8 rounded-3xl border border-indigo-500/40 bg-gradient-to-r from-indigo-950/60 via-purple-950/40 to-slate-900/80 p-5 backdrop-blur-xl shadow-2xl max-w-xl mx-auto"
          >
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-3.5 text-left">
                <div className="relative flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-indigo-500 text-white shadow-lg shadow-indigo-500/30">
                  <UserCheck className="h-6 w-6" />
                  <span className="absolute -top-1 -right-1 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-emerald-500 border-2 border-slate-900">
                    <span className="h-1.5 w-1.5 rounded-full bg-white" />
                  </span>
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-bold text-white">Prince Singh</h3>
                    <span className="rounded-full bg-emerald-500/20 px-2 py-0.5 text-[10px] font-bold text-emerald-400">
                      Live Demo Account
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">
                    CS Senior • GPA 3.84 • Goal: Algorithms & AI
                  </p>
                  <p className="text-[11px] text-slate-400">
                    prince.singh@university.edu
                  </p>
                </div>
              </div>

              <button
                onClick={handleFastDemoLogin}
                disabled={fastLoginLoading}
                className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-2.5 text-xs font-bold text-slate-900 shadow-md hover:bg-slate-100 active:scale-95 transition-all cursor-pointer disabled:opacity-50 shrink-0"
              >
                {fastLoginLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin text-primary" />
                    <span>Logging In...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4 text-primary" />
                    <span>1-Click Demo Login</span>
                    <ChevronRight className="h-3.5 w-3.5 text-slate-500" />
                  </>
                )}
              </button>
            </div>
          </motion.div>
        </div>

        {/* Feature Cards Grid */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 backdrop-blur-md hover:border-white/20 transition-all group"
          >
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-indigo-500/20 text-indigo-400 mb-4 group-hover:scale-105 transition-transform">
              <Zap className="h-5 w-5" />
            </div>
            <h3 className="text-base font-bold text-white mb-2">Autonomous Replanning</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              When an assessment drops or a study block is missed, the autonomous engine recalculates study allocations without breaking your target deadline.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 backdrop-blur-md hover:border-white/20 transition-all group"
          >
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-purple-500/20 text-purple-400 mb-4 group-hover:scale-105 transition-transform">
              <Bot className="h-5 w-5" />
            </div>
            <h3 className="text-base font-bold text-white mb-2">Contextual AI Tutor</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Personalized hints, Socratic explanations, and gap analysis grounded strictly in your current syllabus and active mastery scores.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.55 }}
            className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 backdrop-blur-md hover:border-white/20 transition-all group"
          >
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-500/20 text-emerald-400 mb-4 group-hover:scale-105 transition-transform">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <h3 className="text-base font-bold text-white mb-2">Deterministic Verification</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Every plan revision is verified by deterministic constraint checkers to ensure calendar conflicts and prerequisite graphs remain satisfied.
            </p>
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 py-8 text-center text-xs text-slate-500">
        <p>© 2025 LearnMate Autonomous Learning Planner. Designed for university students.</p>
      </footer>
    </div>
  );
};
