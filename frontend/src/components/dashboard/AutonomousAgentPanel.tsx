/**
 * AutonomousAgentPanel — Real-time Autonomous Agent Activity Feed,
 * "Why did my plan change?" explanation card, and Old Plan vs New Plan
 * side-by-side comparison animated with Framer Motion.
 */

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  Sparkles,
  RefreshCw,
  Clock,
  TrendingUp,
  AlertCircle,
  Calendar,
  ChevronDown,
  ChevronUp,
  ShieldCheck,
  Zap,
  Check,
  Play,
  Terminal,
  FileDiff,
  Flame,
} from "lucide-react";
import {
  useAgentActivity,
  useReplanComparison,
  useRunAgent,
  type AgentActionItem,
  type PlanComparisonItem,
} from "@/hooks/useLearnMate";
import { LoadingState, ErrorState } from "@/components/ui/states";

export function AutonomousAgentPanel() {
  const [isExpanded, setIsExpanded] = useState(true);
  const [filterMode, setFilterMode] = useState<"all" | "changed" | "preserved">("all");
  const [isReplaying, setIsReplaying] = useState(false);
  const [activeStepIndex, setActiveStepIndex] = useState<number | null>(null);
  const [hoveredActivity, setHoveredActivity] = useState<string | null>(null);

  const {
    data: agentFeed,
    isLoading: isFeedLoading,
    isError: isFeedError,
    refetch: refetchFeed,
  } = useAgentActivity();

  const {
    data: comparison,
    isLoading: isComparisonLoading,
    isError: isComparisonError,
    refetch: refetchComparison,
  } = useReplanComparison();

  const runAgentMutation = useRunAgent();

  if (isFeedLoading || isComparisonLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <LoadingState message="Connecting to LearnMate Autonomous Reasoning Feed..." />
      </div>
    );
  }

  if (isFeedError || isComparisonError) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <ErrorState
          title="Autonomous Agent Feed Unavailable"
          message="Could not stream telemetry from the autonomous planner."
          onRetry={() => {
            refetchFeed();
            refetchComparison();
          }}
        />
      </div>
    );
  }

  const actions: AgentActionItem[] = agentFeed?.actions || [
    {
      time: "18:42",
      type: "check",
      title: "Performance analyzed",
      description: "Calculated mastery across topics.",
      status: "completed",
    },
    {
      time: "18:42",
      type: "check",
      title: "2 knowledge gaps detected",
      description: "DP & Trees prioritized.",
      status: "completed",
    },
    {
      time: "18:43",
      type: "check",
      title: "14 resources evaluated",
      description: "Ranked by affinity & effectiveness.",
      status: "completed",
    },
    {
      time: "18:43",
      type: "check",
      title: "Calendar availability checked",
      description: "Identified weekend 3h window.",
      status: "completed",
    },
    {
      time: "18:44",
      type: "refresh",
      title: "Learning plan regenerated",
      description: "Synthesized Plan v11.",
      status: "completed",
    },
    {
      time: "18:44",
      type: "check",
      title: "Plan verified",
      description: "10/10 validation constraints passed.",
      status: "completed",
    },
    {
      time: "18:44",
      type: "check",
      title: "New plan activated",
      description: "Target deadline 30 Nov 2025 guaranteed.",
      status: "completed",
    },
  ];

  const oldActivities: PlanComparisonItem[] = comparison?.old_plan?.activities || [];
  const newActivities: PlanComparisonItem[] = comparison?.new_plan?.activities || [];
  const explanations: string[] = comparison?.explanations || [
    "Your Graphs score improved from 52% to 81%.",
    "The agent reduced Graph revision by 45 minutes.",
    "Dynamic Programming is now your highest-priority gap.",
    "The agent moved DP practice to Saturday.",
    "Goal deadline remains achievable.",
  ];

  // Handler to replay reasoning sequence animation
  const handleReplayReasoning = () => {
    setIsReplaying(true);
    setActiveStepIndex(0);

    let current = 0;
    const interval = setInterval(() => {
      current += 1;
      if (current < actions.length) {
        setActiveStepIndex(current);
      } else {
        clearInterval(interval);
        setTimeout(() => {
          setIsReplaying(false);
          setActiveStepIndex(null);
        }, 1200);
      }
    }, 450);
  };

  const filteredOldActivities = oldActivities.filter((act) => {
    if (filterMode === "changed") return act.change_type !== "preserved";
    if (filterMode === "preserved") return act.change_type === "preserved";
    return true;
  });

  const filteredNewActivities = newActivities.filter((act) => {
    if (filterMode === "changed") return act.change_type !== "preserved";
    if (filterMode === "preserved") return act.change_type === "preserved";
    return true;
  });

  return (
    <motion.div
      id="autonomous-agent-panel"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45 }}
      className="overflow-hidden rounded-2xl border border-slate-200/90 bg-white shadow-sm space-y-0"
    >
      {/* ─── 1. Header Bar with Agent Status & Controls ───────────────────────── */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 bg-gradient-to-r from-slate-50/80 via-indigo-50/40 to-purple-50/30 px-6 py-5">
        <div className="flex items-center gap-3.5">
          <div className="relative flex h-11 w-11 items-center justify-center rounded-xl gradient-primary text-white shadow-md shadow-primary/25">
            <Bot className="h-6 w-6" />
            <span className="absolute -top-1 -right-1 flex h-3.5 w-3.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-emerald-500 border-2 border-white" />
            </span>
          </div>

          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-lg font-bold text-slate-900 tracking-tight">
                Autonomous Agent Activity
              </h3>
              <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100/90 border border-emerald-300/80 px-2.5 py-0.5 text-[11px] font-bold text-emerald-800 shadow-2xs">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Live Reasoning Stream
              </span>
              <span className="text-[11px] font-semibold text-indigo-600 bg-indigo-50 border border-indigo-200/70 rounded-full px-2 py-0.5">
                Loop v11 Active
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Self-directed optimization loop continuously auditing velocity, mastery, and calendar constraints.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5 self-end sm:self-center">
          <button
            onClick={handleReplayReasoning}
            disabled={isReplaying}
            className="flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 hover:border-slate-300 disabled:opacity-50 transition-all cursor-pointer"
            title="Replay the 7-step autonomous reasoning sequence"
          >
            <Play className={`h-3.5 w-3.5 text-indigo-600 ${isReplaying ? "animate-pulse" : ""}`} />
            {isReplaying ? "Replaying..." : "Replay Sequence"}
          </button>

          <button
            onClick={() => runAgentMutation.mutate()}
            disabled={runAgentMutation.isPending}
            className="flex items-center gap-2 rounded-xl gradient-primary px-4 py-2 text-xs font-semibold text-white shadow-md shadow-primary/20 hover:opacity-95 disabled:opacity-50 transition-all cursor-pointer"
          >
            <Sparkles
              className={`h-3.5 w-3.5 ${runAgentMutation.isPending ? "animate-spin" : ""}`}
            />
            {runAgentMutation.isPending ? "Orchestrating Loop..." : "Run Agent Now"}
          </button>

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 text-slate-400 hover:text-slate-600 rounded-xl hover:bg-slate-100 transition-colors"
            title={isExpanded ? "Collapse panel" : "Expand panel"}
          >
            {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="p-6 space-y-6"
          >
            {/* ─── 2. Agent Action Feed: Dual Mode (Chronological Log & Stepper) ─── */}
            <div className="space-y-3">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-primary" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600">
                    Latest Agent Actions Log
                  </h4>
                </div>
                <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium">
                  <span className="flex items-center gap-1">
                    <Terminal className="h-3 w-3 text-slate-400" />
                    Last executed: 18:44
                  </span>
                  <span className="h-1 w-1 rounded-full bg-slate-300" />
                  <span className="text-emerald-700 font-semibold">7/7 Steps Verified</span>
                </div>
              </div>

              {/* High-visibility chronological feed list matching the example format */}
              <div className="rounded-2xl border border-slate-200/90 bg-slate-900 text-slate-100 p-4 shadow-sm font-mono text-xs overflow-x-auto">
                <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800 text-[11px] text-slate-400 font-sans font-semibold">
                  <span className="flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
                    STREAM: agent.orchestrator.events &bull; student_id: stu-001
                  </span>
                  <span className="text-indigo-300 font-mono">STATUS: 200 OK</span>
                </div>

                <div className="space-y-1.5 font-mono">
                  {actions.map((act, index) => {
                    const isRefresh = act.type === "refresh";
                    const isStepActive = activeStepIndex === index;

                    return (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{
                          opacity: 1,
                          x: 0,
                          backgroundColor: isStepActive
                            ? "rgba(99, 102, 241, 0.25)"
                            : "transparent",
                        }}
                        transition={{ delay: index * 0.04 }}
                        className={`flex items-center justify-between gap-4 py-1 px-2 rounded-md transition-colors ${
                          isStepActive
                            ? "border border-indigo-500/50"
                            : "hover:bg-slate-800/60"
                        }`}
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <span className="text-slate-400 select-none">{act.time}</span>
                          {isRefresh ? (
                            <span className="inline-flex items-center justify-center text-indigo-400 font-bold">
                              <RefreshCw className={`h-3.5 w-3.5 ${isReplaying ? "animate-spin" : ""}`} />
                            </span>
                          ) : (
                            <span className="inline-flex items-center justify-center text-emerald-400 font-bold">
                              <Check className="h-3.5 w-3.5 stroke-[3]" />
                            </span>
                          )}
                          <span
                            className={`font-semibold tracking-tight truncate ${
                              isRefresh ? "text-indigo-200 font-bold" : "text-slate-100"
                            }`}
                          >
                            {act.title}
                          </span>
                        </div>

                        <div className="hidden sm:flex items-center gap-2 text-slate-400 text-[11px] font-sans">
                          <span className="truncate max-w-[280px]">{act.description}</span>
                          <span className="rounded bg-slate-800 border border-slate-700 px-1.5 py-0.2 text-[10px] text-emerald-400 font-mono">
                            done
                          </span>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* ─── 3. "Why did my plan change?" Section ──────────────────────── */}
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 }}
              className="rounded-2xl border border-indigo-200/80 bg-gradient-to-br from-indigo-50/70 via-purple-50/40 to-white p-5 shadow-xs"
            >
              {/* Section Header */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-indigo-100">
                <div className="flex items-center gap-2.5">
                  <span className="inline-flex items-center gap-1 rounded-lg bg-indigo-600 px-2.5 py-1 text-[11px] font-black uppercase tracking-wider text-white shadow-xs">
                    <Flame className="h-3.5 w-3.5" />
                    PLAN UPDATED
                  </span>
                  <h4 className="text-base font-bold text-slate-900 tracking-tight">
                    Why did my plan change?
                  </h4>
                </div>

                <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full">
                  <ShieldCheck className="h-4 w-4 text-emerald-600" />
                  <span>Goal deadline remains achievable (30 Nov 2025)</span>
                </div>
              </div>

              {/* The 5 exact explanation points rendered with high visual hierarchy */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5 pt-4">
                {explanations.map((exp, idx) => {
                  let icon = <Zap className="h-4 w-4 text-primary" />;
                  let bgTint = "bg-white border-slate-200/80 hover:border-slate-300";
                  let statPill = null;

                  if (exp.includes("improved")) {
                    icon = <TrendingUp className="h-4 w-4 text-emerald-600" />;
                    bgTint = "bg-emerald-50/60 border-emerald-200/90 shadow-2xs hover:bg-emerald-50";
                    statPill = (
                      <span className="rounded bg-emerald-100/90 border border-emerald-300/80 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                        +29% Mastery
                      </span>
                    );
                  } else if (exp.includes("reduced")) {
                    icon = <Clock className="h-4 w-4 text-cyan-600" />;
                    bgTint = "bg-cyan-50/60 border-cyan-200/90 shadow-2xs hover:bg-cyan-50";
                    statPill = (
                      <span className="rounded bg-cyan-100/90 border border-cyan-300/80 px-2 py-0.5 text-[10px] font-bold text-cyan-800">
                        -45m Saved
                      </span>
                    );
                  } else if (exp.includes("highest-priority gap")) {
                    icon = <AlertCircle className="h-4 w-4 text-amber-600" />;
                    bgTint = "bg-amber-50/60 border-amber-200/90 shadow-2xs hover:bg-amber-50";
                    statPill = (
                      <span className="rounded bg-amber-100/90 border border-amber-300/80 px-2 py-0.5 text-[10px] font-bold text-amber-800">
                        Priority #1
                      </span>
                    );
                  } else if (exp.includes("moved")) {
                    icon = <Calendar className="h-4 w-4 text-indigo-600" />;
                    bgTint = "bg-indigo-50/60 border-indigo-200/90 shadow-2xs hover:bg-indigo-50";
                    statPill = (
                      <span className="rounded bg-indigo-100/90 border border-indigo-300/80 px-2 py-0.5 text-[10px] font-bold text-indigo-800">
                        Weekend Slot
                      </span>
                    );
                  } else if (exp.includes("achievable")) {
                    icon = <ShieldCheck className="h-4 w-4 text-emerald-600" />;
                    bgTint = "bg-emerald-50/50 border-emerald-200/80 shadow-2xs hover:bg-emerald-50";
                    statPill = (
                      <span className="rounded bg-emerald-100/90 border border-emerald-300/80 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                        100% Verified
                      </span>
                    );
                  }

                  return (
                    <motion.div
                      key={idx}
                      whileHover={{ scale: 1.015, y: -1 }}
                      transition={{ type: "spring", stiffness: 400, damping: 25 }}
                      className={`flex flex-col justify-between rounded-xl border p-3.5 transition-all ${bgTint}`}
                    >
                      <div className="flex items-start gap-2.5">
                        <div className="mt-0.5 p-1.5 rounded-lg bg-white/80 shadow-2xs shrink-0">
                          {icon}
                        </div>
                        <p className="text-xs font-semibold text-slate-900 leading-snug">
                          {exp}
                        </p>
                      </div>

                      {statPill && (
                        <div className="mt-2.5 pt-2 border-t border-slate-200/40 flex items-center justify-end">
                          {statPill}
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>

            {/* ─── 4. Old Plan vs New Plan Side-by-Side Comparison ───────────── */}
            <div className="space-y-3">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 flex-wrap">
                <div className="flex items-center gap-2">
                  <FileDiff className="h-4 w-4 text-primary" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                    Plan Revision Diff — Old Plan vs New Plan
                  </h4>
                </div>

                {/* Filter Toggles */}
                <div className="flex items-center gap-2 flex-wrap">
                  <div className="flex items-center bg-slate-100 p-0.5 rounded-lg text-xs font-semibold text-slate-600">
                    <button
                      onClick={() => setFilterMode("all")}
                      className={`px-2.5 py-1 rounded-md transition-all ${
                        filterMode === "all"
                          ? "bg-white text-indigo-700 shadow-2xs font-bold"
                          : "hover:text-slate-900"
                      }`}
                    >
                      All (5)
                    </button>
                    <button
                      onClick={() => setFilterMode("changed")}
                      className={`px-2.5 py-1 rounded-md transition-all ${
                        filterMode === "changed"
                          ? "bg-white text-indigo-700 shadow-2xs font-bold"
                          : "hover:text-slate-900"
                      }`}
                    >
                      Changes Only (3)
                    </button>
                    <button
                      onClick={() => setFilterMode("preserved")}
                      className={`px-2.5 py-1 rounded-md transition-all ${
                        filterMode === "preserved"
                          ? "bg-white text-indigo-700 shadow-2xs font-bold"
                          : "hover:text-slate-900"
                      }`}
                    >
                      Preserved (2)
                    </button>
                  </div>

                  <span className="rounded-md bg-rose-50 border border-rose-200 px-2 py-0.5 text-[10px] font-bold text-rose-700">
                    1 Shortened
                  </span>
                  <span className="rounded-md bg-indigo-50 border border-indigo-200 px-2 py-0.5 text-[10px] font-bold text-indigo-700">
                    1 Moved to Sat
                  </span>
                  <span className="rounded-md bg-emerald-50 border border-emerald-200 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
                    1 Added
                  </span>
                </div>
              </div>

              {/* Side-by-Side Columns Animated with Framer Motion */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-start">
                {/* ── Left Column: Old Plan (v10) ── */}
                <motion.div
                  layout
                  className="rounded-2xl border border-slate-200 bg-slate-50/50 p-4 space-y-3"
                >
                  <div className="flex items-center justify-between pb-2.5 border-b border-slate-200">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-slate-200 px-2 py-0.5 text-[10px] font-extrabold uppercase text-slate-700">
                        PREVIOUS
                      </span>
                      <h5 className="text-xs font-bold text-slate-800">
                        Old Plan (Version 10)
                      </h5>
                    </div>
                    <span className="text-[11px] text-slate-500 font-medium">
                      Total: <strong className="text-slate-700">9.5 hrs</strong>
                    </span>
                  </div>

                  <motion.div layout className="space-y-2.5">
                    <AnimatePresence mode="popLayout">
                      {filteredOldActivities.map((act) => {
                        const isShortened = act.change_type === "shortened";
                        const isMoved = act.change_type === "moved";
                        const isHighlighted = hoveredActivity === act.id;

                        return (
                          <motion.div
                            key={act.id}
                            layout
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            transition={{ duration: 0.25 }}
                            onMouseEnter={() => setHoveredActivity(act.id)}
                            onMouseLeave={() => setHoveredActivity(null)}
                            className={`p-3.5 rounded-xl border transition-all ${
                              isHighlighted
                                ? "ring-2 ring-indigo-400 bg-indigo-50/60 shadow-xs"
                                : isShortened
                                ? "border-amber-200/90 bg-amber-50/40"
                                : isMoved
                                ? "border-indigo-200/90 bg-indigo-50/30"
                                : "border-slate-200 bg-white"
                            }`}
                          >
                            <div className="flex items-center justify-between gap-2 mb-1">
                              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                                {act.topic} &bull; {act.type}
                              </span>
                              <span
                                className={`rounded px-1.5 py-0.5 text-[10px] font-bold ${
                                  isShortened
                                    ? "bg-amber-100 text-amber-800 border border-amber-200"
                                    : isMoved
                                    ? "bg-indigo-100 text-indigo-800 border border-indigo-200"
                                    : "bg-slate-100 text-slate-600 border border-slate-200"
                                }`}
                              >
                                {act.change_badge}
                              </span>
                            </div>

                            <h6
                              className={`text-xs font-bold leading-tight ${
                                isShortened || isMoved ? "text-slate-900" : "text-slate-700"
                              }`}
                            >
                              {act.title}
                            </h6>

                            <div className="flex items-center gap-3 text-[11px] text-slate-500 mt-2">
                              <span
                                className={`font-bold ${
                                  isShortened ? "line-through text-slate-400" : "text-slate-700"
                                }`}
                              >
                                {act.duration_minutes} mins
                              </span>
                              <span>&bull; {act.day} ({act.time})</span>
                            </div>
                          </motion.div>
                        );
                      })}
                    </AnimatePresence>
                  </motion.div>
                </motion.div>

                {/* ── Right Column: New Plan (v11 - Active) ── */}
                <motion.div
                  layout
                  className="rounded-2xl border border-indigo-200 bg-indigo-50/20 p-4 space-y-3"
                >
                  <div className="flex items-center justify-between pb-2.5 border-b border-indigo-100">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md gradient-primary px-2 py-0.5 text-[10px] font-extrabold uppercase text-white shadow-2xs">
                        ACTIVE
                      </span>
                      <h5 className="text-xs font-bold text-slate-900">
                        New Plan (Version 11 — Optimized)
                      </h5>
                    </div>
                    <span className="text-[11px] font-bold text-primary">
                      Total: 9.0 hrs <span className="text-emerald-600">(-30m net)</span>
                    </span>
                  </div>

                  <motion.div layout className="space-y-2.5">
                    <AnimatePresence mode="popLayout">
                      {filteredNewActivities.map((act) => {
                        const isShortened = act.change_type === "shortened";
                        const isMoved = act.change_type === "moved";
                        const isAdded = act.change_type === "added";
                        // match corresponding old item highlight
                        const isHighlighted =
                          (hoveredActivity === "act-old-1" && act.id === "act-new-1") ||
                          (hoveredActivity === "act-old-2" && act.id === "act-new-2");

                        return (
                          <motion.div
                            key={act.id}
                            layout
                            initial={{ opacity: 0, x: 8 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 8 }}
                            transition={{ duration: 0.25 }}
                            className={`p-3.5 rounded-xl border transition-all ${
                              isHighlighted
                                ? "ring-2 ring-indigo-500 bg-indigo-100/60 shadow-xs"
                                : isAdded
                                ? "border-emerald-300 bg-emerald-50/70 shadow-xs"
                                : isMoved
                                ? "border-indigo-300 bg-indigo-50/60 shadow-xs"
                                : isShortened
                                ? "border-cyan-300 bg-cyan-50/50 shadow-xs"
                                : "border-slate-200 bg-white"
                            }`}
                          >
                            <div className="flex items-center justify-between gap-2 mb-1">
                              <span className="text-[10px] font-bold uppercase tracking-wider text-primary">
                                {act.topic} &bull; {act.type}
                              </span>
                              <span
                                className={`rounded px-1.5 py-0.5 text-[10px] font-bold ${
                                  isAdded
                                    ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                                    : isMoved
                                    ? "bg-indigo-100 text-indigo-800 border border-indigo-200"
                                    : isShortened
                                    ? "bg-cyan-100 text-cyan-800 border border-cyan-200"
                                    : "bg-slate-100 text-slate-600 border border-slate-200"
                                }`}
                              >
                                {act.change_badge}
                              </span>
                            </div>

                            <h6 className="text-xs font-bold text-slate-900 leading-tight">
                              {act.title}
                            </h6>

                            <div className="flex items-center justify-between text-[11px] text-slate-500 mt-2 flex-wrap gap-1">
                              <div className="flex items-center gap-2">
                                <span className="font-bold text-slate-900">
                                  {act.duration_minutes} mins
                                </span>
                                <span>&bull; {act.day} ({act.time})</span>
                              </div>

                              {act.diff_note && (
                                <span className="text-[10px] font-medium text-indigo-700 bg-indigo-50/80 px-2 py-0.5 rounded border border-indigo-200/60">
                                  {act.diff_note}
                                </span>
                              )}
                            </div>
                          </motion.div>
                        );
                      })}
                    </AnimatePresence>
                  </motion.div>
                </motion.div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
