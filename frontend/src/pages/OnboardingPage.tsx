import React, { useState } from "react";
import { motion } from "framer-motion";
import { Brain, Target, Calendar, Clock, BookOpen, CheckCircle2, ArrowRight, Loader2, Sparkles } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

interface OnboardingPageProps {
  onNavigate: (page: string) => void;
}

const GOAL_OPTIONS = [
  {
    id: "dsa",
    title: "Master Data Structures & Algorithms",
    description: "Graph traversal, Dynamic Programming, Topological sort, Dijkstra's algorithm",
    defaultHours: 14,
    deadline: "2025-06-15",
  },
  {
    id: "ai",
    title: "Deep Learning & Neural Architectures",
    description: "Backprop, Transformers, Attention mechanisms, Convolutional networks",
    defaultHours: 12,
    deadline: "2025-07-01",
  },
  {
    id: "systems",
    title: "Distributed Systems & Cloud Computing",
    description: "Consensus algorithms, Raft, Distributed caching, Fault tolerance",
    defaultHours: 10,
    deadline: "2025-08-15",
  },
];

const TOPIC_CHIPS = [
  "Graph Algorithms",
  "Dynamic Programming",
  "Trees & Heaps",
  "Sorting & Searching",
  "Greedy Algorithms",
  "Bit Manipulation",
  "System Design",
  "Time Complexity Analysis",
];

export const OnboardingPage: React.FC<OnboardingPageProps> = ({ onNavigate }) => {
  const { user, completeOnboarding } = useAuth();

  const [selectedGoal, setSelectedGoal] = useState<string>(GOAL_OPTIONS[0].title);
  const [weeklyHours, setWeeklyHours] = useState<number>(14);
  const [targetDeadline, setTargetDeadline] = useState<string>("2025-06-15");
  const [selectedTopics, setSelectedTopics] = useState<string[]>([
    "Graph Algorithms",
    "Dynamic Programming",
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleTopic = (topic: string) => {
    if (selectedTopics.includes(topic)) {
      setSelectedTopics(selectedTopics.filter((t) => t !== topic));
    } else {
      setSelectedTopics([...selectedTopics, topic]);
    }
  };

  const handleFinishOnboarding = async () => {
    setLoading(true);
    setError(null);
    try {
      await completeOnboarding({
        current_goal: selectedGoal,
        target_deadline: targetDeadline,
        weekly_target_hours: weeklyHours,
        subjects: selectedTopics,
      });
      onNavigate("dashboard");
    } catch (err: any) {
      setError(err?.message || "Failed to save onboarding preferences.");
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full bg-slate-950 text-white font-sans flex items-center justify-center p-4 sm:p-6 overflow-hidden">
      {/* Glow */}
      <div className="pointer-events-none absolute top-1/4 left-1/2 -translate-x-1/2 h-[500px] w-[700px] rounded-full bg-primary/15 blur-[120px]" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="relative z-10 w-full max-w-3xl rounded-3xl border border-white/15 bg-slate-900/85 p-6 sm:p-10 backdrop-blur-2xl shadow-2xl space-y-8"
      >
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl gradient-primary shadow-lg shadow-primary/30">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-black text-white">
                Welcome to LearnMate, {user?.full_name?.split(" ")[0] || "Scholar"}! 👋
              </h1>
              <p className="text-xs text-slate-400">
                Let's configure your autonomous learning parameters and initial goal.
              </p>
            </div>
          </div>
          <span className="rounded-full bg-primary/20 border border-primary/30 px-3 py-1 text-xs font-semibold text-primary-light flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5" />
            Initial Setup
          </span>
        </div>

        {error && (
          <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-xs text-rose-300">
            {error}
          </div>
        )}

        {/* Section 1: Choose Primary Learning Goal */}
        <div className="space-y-3">
          <label className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-300">
            <Target className="h-4 w-4 text-primary-light" />
            1. Select Primary Target Goal
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {GOAL_OPTIONS.map((g) => {
              const isSelected = selectedGoal === g.title;
              return (
                <div
                  key={g.id}
                  onClick={() => {
                    setSelectedGoal(g.title);
                    setWeeklyHours(g.defaultHours);
                    setTargetDeadline(g.deadline);
                  }}
                  className={`cursor-pointer rounded-2xl border p-4 transition-all ${
                    isSelected
                      ? "border-primary bg-primary/15 shadow-md shadow-primary/20"
                      : "border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/10"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-xs font-bold text-white">{g.title}</h4>
                    {isSelected && <CheckCircle2 className="h-4 w-4 text-primary-light shrink-0" />}
                  </div>
                  <p className="text-[11px] text-slate-400 line-clamp-3">{g.description}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Section 2: Study Availability & Deadline */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="flex items-center justify-between text-xs font-bold text-slate-300">
              <span className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-primary-light" />
                Weekly Study Allocation
              </span>
              <span className="rounded-md bg-primary/20 px-2 py-0.5 font-mono text-xs font-bold text-primary-light">
                {weeklyHours} hrs/week
              </span>
            </label>
            <input
              type="range"
              min={5}
              max={30}
              step={1}
              value={weeklyHours}
              onChange={(e) => setWeeklyHours(Number(e.target.value))}
              className="w-full accent-primary cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500">
              <span>5 hrs (Light)</span>
              <span>15 hrs (Balanced)</span>
              <span>30 hrs (Intensive)</span>
            </div>
          </div>

          <div className="space-y-2">
            <label className="flex items-center gap-2 text-xs font-bold text-slate-300">
              <Calendar className="h-4 w-4 text-primary-light" />
              Target Mastery Deadline
            </label>
            <input
              type="date"
              value={targetDeadline}
              onChange={(e) => setTargetDeadline(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs text-white focus:border-primary focus:outline-hidden"
            />
            <p className="text-[10px] text-slate-500">
              The deterministic verifier will validate your schedule against this deadline.
            </p>
          </div>
        </div>

        {/* Section 3: Focus Topics */}
        <div className="space-y-2.5">
          <label className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-300">
            <BookOpen className="h-4 w-4 text-primary-light" />
            3. Select Focus Topics & Initial Diagnostic Focus
          </label>
          <div className="flex flex-wrap gap-2">
            {TOPIC_CHIPS.map((chip) => {
              const isSelected = selectedTopics.includes(chip);
              return (
                <button
                  type="button"
                  key={chip}
                  onClick={() => toggleTopic(chip)}
                  className={`rounded-xl px-3 py-1.5 text-xs font-medium transition-all cursor-pointer ${
                    isSelected
                      ? "bg-primary text-white border border-primary shadow-xs"
                      : "border border-white/10 bg-white/5 text-slate-300 hover:bg-white/10"
                  }`}
                >
                  {chip}
                </button>
              );
            })}
          </div>
        </div>

        {/* Complete button */}
        <div className="pt-4 border-t border-white/10 flex items-center justify-end gap-3">
          <button
            onClick={handleFinishOnboarding}
            disabled={loading}
            className="flex items-center gap-2 rounded-2xl gradient-primary px-6 py-3 text-sm font-bold text-white shadow-lg shadow-primary/30 hover:shadow-xl hover:shadow-primary/40 active:scale-95 transition-all disabled:opacity-60 cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Activating Autonomous Agent...</span>
              </>
            ) : (
              <>
                <span>Complete Setup & Launch Dashboard</span>
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>
        </div>
      </motion.div>
    </div>
  );
};
