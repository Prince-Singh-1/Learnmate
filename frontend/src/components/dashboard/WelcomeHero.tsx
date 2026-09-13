/**
 * WelcomeHero — Left top hero banner with Pixar 3D student artwork,
 * motivational greeting, quote, and quick action buttons.
 */

import { motion } from "framer-motion";
import { Sparkles, ArrowRight, BookOpen, Bot } from "lucide-react";
import { useStudent } from "@/hooks/useLearnMate";

interface WelcomeHeroProps {
  onContinueLearning?: () => void;
  onViewPlan?: () => void;
  onOpenSimulation?: () => void;
}

export function WelcomeHero({ onContinueLearning, onViewPlan, onOpenSimulation }: WelcomeHeroProps) {
  const { data: student } = useStudent();
  const studentName = student?.name || "Alex";

  const scrollToAgent = () => {
    document.getElementById("autonomous-agent-panel")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="relative overflow-hidden rounded-2xl border border-white/[0.08] gradient-hero shadow-2xl p-6 lg:p-7 flex flex-col md:flex-row items-center justify-between gap-6"
    >
      {/* Background subtle glow circles */}
      <div className="absolute -left-12 -top-12 h-56 w-56 rounded-full bg-primary/20 blur-3xl pointer-events-none" />
      <div className="absolute right-10 bottom-0 h-48 w-48 rounded-full bg-purple-600/15 blur-3xl pointer-events-none" />

      {/* Left text content */}
      <div className="relative z-10 flex-1 space-y-4 max-w-xl">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.06] px-3 py-1 text-xs font-medium text-purple-200 mb-2 backdrop-blur-md">
            <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Autonomous Learning Planner Active
          </div>
          <h2 className="text-2xl lg:text-3xl font-extrabold tracking-tight text-white">
            Good Evening, {studentName}! 👋
          </h2>
          <p className="text-sm text-white/70 mt-1 font-normal">
            Small steps today, big results tomorrow.
          </p>
        </div>

        {/* Quote box */}
        <div className="rounded-xl border border-white/10 bg-white/[0.04] p-3.5 backdrop-blur-md">
          <p className="text-xs italic text-white/80 leading-relaxed">
            "The expert in anything was once a beginner."
          </p>
          <p className="text-[11px] text-white/50 mt-1 font-medium">— Helen Hayes</p>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center gap-3 pt-1">
          <motion.button
            whileHover={{ scale: 1.03, boxShadow: "0 10px 25px -5px rgba(99, 102, 241, 0.4)" }}
            whileTap={{ scale: 0.97 }}
            onClick={onContinueLearning}
            className="flex items-center gap-2 rounded-xl gradient-primary px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-primary/25 transition-all cursor-pointer"
          >
            <Sparkles className="h-4 w-4" />
            Continue Learning
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.03, backgroundColor: "rgba(168, 85, 247, 0.3)" }}
            whileTap={{ scale: 0.97 }}
            onClick={onOpenSimulation}
            className="flex items-center gap-2 rounded-xl border border-purple-400/50 bg-purple-600/25 px-4 py-2.5 text-sm font-semibold text-purple-200 backdrop-blur-md transition-all hover:bg-purple-600/40 cursor-pointer shadow-lg shadow-purple-500/20"
          >
            <Sparkles className="h-4 w-4 text-amber-300" />
            Demo Simulation Lab
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.03, backgroundColor: "rgba(99, 102, 241, 0.25)" }}
            whileTap={{ scale: 0.97 }}
            onClick={scrollToAgent}
            className="flex items-center gap-2 rounded-xl border border-indigo-400/40 bg-indigo-500/15 px-3.5 py-2.5 text-sm font-semibold text-white backdrop-blur-md transition-all hover:bg-indigo-500/25 cursor-pointer"
          >
            <Bot className="h-4 w-4 text-emerald-400" />
            Agent Reasoning
            <ArrowRight className="h-3.5 w-3.5 opacity-70" />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.03, backgroundColor: "rgba(255, 255, 255, 0.12)" }}
            whileTap={{ scale: 0.97 }}
            onClick={onViewPlan}
            className="flex items-center gap-2 rounded-xl border border-white/15 bg-white/[0.06] px-3.5 py-2.5 text-sm font-medium text-white/90 backdrop-blur-md transition-all hover:text-white cursor-pointer"
          >
            <BookOpen className="h-4 w-4 opacity-70" />
            Plan
          </motion.button>
        </div>
      </div>

      {/* Right Artwork banner with 3D depth */}
      <div className="relative z-10 w-full md:w-auto flex-shrink-0 flex justify-center">
        <motion.div
          whileHover={{ scale: 1.03, rotateY: 4, rotateX: -2 }}
          transition={{ type: "spring", stiffness: 220, damping: 20 }}
          style={{ perspective: 1000 }}
          className="relative overflow-hidden rounded-2xl border border-white/25 shadow-2xl group max-w-[360px] max-h-[210px] bg-slate-950"
        >
          <img
            src="/hero-student-3d.jpg"
            alt="3D Student learning with AI assistant"
            className="h-[200px] w-[340px] object-cover object-center transition-transform duration-500 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-transparent to-transparent pointer-events-none" />
          <div className="absolute bottom-2.5 left-3 right-3 flex items-center justify-between text-[11px] font-medium text-white/90 drop-shadow-md">
            <span className="flex items-center gap-1.5 font-semibold text-white">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              Autonomous Copilot
            </span>
            <span className="rounded-md bg-white/20 px-2 py-0.5 backdrop-blur-md text-[10px] font-bold border border-white/20">
              3D AI Engine
            </span>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
