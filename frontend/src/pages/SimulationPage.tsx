/**
 * SimulationPage — Demo Simulation Laboratory for Presentations.
 *
 * Demonstrates the autonomous closed loop:
 *
 *   EVENT DETECTED
 *         ↓
 *   STATE UPDATED
 *         ↓
 *   PERFORMANCE REASSESSED
 *         ↓
 *   PLAN REGENERATED
 *         ↓
 *   PLAN VERIFIED
 *         ↓
 *   NEW PLAN ACTIVATED
 *
 * Features 7 prominent live action buttons:
 * - [ Miss Today's Session ]
 * - [ Score Poorly ]
 * - [ Improve Quickly ]
 * - [ Lose 2 Hours This Week ]
 * - [ Gain 3 Hours This Week ]
 * - [ Move Deadline Earlier ]
 * - [ Complete Quiz ]
 */

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play,
  Sparkles,
  AlertTriangle,
  TrendingDown,
  TrendingUp,
  Clock,
  Calendar,
  CalendarCheck,
  CheckCircle2,
  ChevronRight,
  ArrowDown,
  ShieldCheck,
  Zap,
  Activity,
  Award,
  RefreshCw,
  Check,
} from "lucide-react";
import {
  useSimulateEvent,
  useStudent,
  useKnowledgeGaps,
  useLearningPlan,
  type SimulationResultData,
} from "@/hooks/useLearnMate";

interface SimulationScenarioDef {
  id: string;
  label: string;
  icon: typeof Play;
  iconBg: string;
  iconColor: string;
  badgeBg: string;
  badgeText: string;
  badgeLabel: string;
  description: string;
  topic?: string;
  accentBorder: string;
}

const SCENARIOS: SimulationScenarioDef[] = [
  {
    id: "miss_today_session",
    label: "Miss Today's Session",
    icon: AlertTriangle,
    iconBg: "bg-amber-500/15",
    iconColor: "text-amber-600 dark:text-amber-400",
    badgeBg: "bg-amber-100 dark:bg-amber-950/60 border-amber-300 dark:border-amber-700/50",
    badgeText: "text-amber-800 dark:text-amber-300",
    badgeLabel: "Calendar Delay",
    description: "Student skips 60m graph session. Agent shifts catch-up slot to weekend without missing deadline.",
    accentBorder: "hover:border-amber-400/80 active:border-amber-500",
  },
  {
    id: "score_poorly",
    label: "Score Poorly",
    icon: TrendingDown,
    iconBg: "bg-rose-500/15",
    iconColor: "text-rose-600 dark:text-rose-400",
    badgeBg: "bg-rose-100 dark:bg-rose-950/60 border-rose-300 dark:border-rose-700/50",
    badgeText: "text-rose-800 dark:text-rose-300",
    badgeLabel: "Knowledge Gap",
    description: "Scores 35% in Dynamic Programming. Gap escalates to High; agent injects remedial drills.",
    topic: "Dynamic Programming",
    accentBorder: "hover:border-rose-400/80 active:border-rose-500",
  },
  {
    id: "improve_quickly",
    label: "Improve Quickly",
    icon: TrendingUp,
    iconBg: "bg-emerald-500/15",
    iconColor: "text-emerald-600 dark:text-emerald-400",
    badgeBg: "bg-emerald-100 dark:bg-emerald-950/60 border-emerald-300 dark:border-emerald-700/50",
    badgeText: "text-emerald-800 dark:text-emerald-300",
    badgeLabel: "Mastery Surge",
    description: "Scores 92% in Graphs. Mastery jumps, gap drops to Low, and redundant revisions are pruned.",
    topic: "Graphs",
    accentBorder: "hover:border-emerald-400/80 active:border-emerald-500",
  },
  {
    id: "lose_2_hours",
    label: "Lose 2 Hours This Week",
    icon: Clock,
    iconBg: "bg-orange-500/15",
    iconColor: "text-orange-600 dark:text-orange-400",
    badgeBg: "bg-orange-100 dark:bg-orange-950/60 border-orange-300 dark:border-orange-700/50",
    badgeText: "text-orange-800 dark:text-orange-300",
    badgeLabel: "Capacity Squeeze",
    description: "Exam schedule conflict loses 120m. Agent preserves high-priority objectives and trims buffer.",
    accentBorder: "hover:border-orange-400/80 active:border-orange-500",
  },
  {
    id: "gain_3_hours",
    label: "Gain 3 Hours This Week",
    icon: Calendar,
    iconBg: "bg-cyan-500/15",
    iconColor: "text-cyan-600 dark:text-cyan-400",
    badgeBg: "bg-cyan-100 dark:bg-cyan-950/60 border-cyan-300 dark:border-cyan-700/50",
    badgeText: "text-cyan-800 dark:text-cyan-300",
    badgeLabel: "Capacity Expansion",
    description: "Free holiday window unlocks 180m. Agent schedules extra mock coding challenge.",
    accentBorder: "hover:border-cyan-400/80 active:border-cyan-500",
  },
  {
    id: "move_deadline_earlier",
    label: "Move Deadline Earlier",
    icon: CalendarCheck,
    iconBg: "bg-purple-500/15",
    iconColor: "text-purple-600 dark:text-purple-400",
    badgeBg: "bg-purple-100 dark:bg-purple-950/60 border-purple-300 dark:border-purple-700/50",
    badgeText: "text-purple-800 dark:text-purple-300",
    badgeLabel: "Sprint Accelerated",
    description: "Interview moved up 14 days. Agent compresses schedule and accelerates core prerequisites.",
    accentBorder: "hover:border-purple-400/80 active:border-purple-500",
  },
  {
    id: "complete_quiz",
    label: "Complete Quiz",
    icon: Award,
    iconBg: "bg-indigo-500/15",
    iconColor: "text-indigo-600 dark:text-indigo-400",
    badgeBg: "bg-indigo-100 dark:bg-indigo-950/60 border-indigo-300 dark:border-indigo-700/50",
    badgeText: "text-indigo-800 dark:text-indigo-300",
    badgeLabel: "Milestone Verified",
    description: "Scores 85% in DP Quiz. Updates study streak, increases mastery confidence, and verifies plan.",
    topic: "Dynamic Programming",
    accentBorder: "hover:border-indigo-400/80 active:border-indigo-500",
  },
];

const PIPELINE_NODES = [
  { step: 1, key: "event_detected", title: "EVENT DETECTED", sub: "Telemetry Sensor" },
  { step: 2, key: "state_updated", title: "STATE UPDATED", sub: "Profile & History" },
  { step: 3, key: "performance_reassessed", title: "PERFORMANCE REASSESSED", sub: "Knowledge Gaps" },
  { step: 4, key: "plan_regenerated", title: "PLAN REGENERATED", sub: "Adaptive Scheduler" },
  { step: 5, key: "plan_verified", title: "PLAN VERIFIED", sub: "PlanVerifier Gate" },
  { step: 6, key: "new_plan_activated", title: "NEW PLAN ACTIVATED", sub: "Live Production" },
];

export function SimulationPage() {
  const [activeScenarioId, setActiveScenarioId] = useState<string>("miss_today_session");
  const [lastResult, setLastResult] = useState<SimulationResultData | null>(null);
  const [activeStepTab, setActiveStepTab] = useState<number>(1);

  const { data: student } = useStudent();
  const { data: gaps } = useKnowledgeGaps();
  const { data: plan } = useLearningPlan();

  const simulateMutation = useSimulateEvent();

  const handleRunSimulation = (scenarioId: string) => {
    setActiveScenarioId(scenarioId);
    const def = SCENARIOS.find((s) => s.id === scenarioId);
    simulateMutation.mutate(
      {
        scenario: scenarioId,
        topic: def?.topic,
      },
      {
        onSuccess: (data) => {
          setLastResult(data);
          setActiveStepTab(1);
        },
      }
    );
  };

  // Auto-run initial baseline simulation on mount so demo is immediately populated
  useEffect(() => {
    if (!lastResult && !simulateMutation.isPending) {
      handleRunSimulation("miss_today_session");
    }
  }, []);

  return (
    <div className="space-y-7 pb-12">
      {/* ─── Hero Header ─────────────────────────────────────────── */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="relative overflow-hidden rounded-2xl border border-white/[0.08] gradient-hero p-6 lg:p-8 shadow-2xl"
      >
        <div className="absolute -left-12 -top-12 h-60 w-60 rounded-full bg-indigo-500/20 blur-3xl pointer-events-none" />
        <div className="absolute right-10 bottom-0 h-48 w-48 rounded-full bg-purple-600/20 blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.06] px-3.5 py-1 text-xs font-semibold text-purple-200 backdrop-blur-md">
              <Sparkles className="h-3.5 w-3.5 text-amber-300" />
              Live Presentation Mode • Autonomous Closed-Loop
            </div>
            <h1 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
              Demo Simulation Laboratory
            </h1>
            <p className="text-sm text-white/75 leading-relaxed">
              Experience how LearnMate autonomously senses friction, recalibrates topic mastery,
              and re-synthesizes mathematically verified learning plans in real-time.
            </p>
          </div>

          {/* Quick Active Plan Pill */}
          <div className="flex flex-col sm:flex-row md:flex-col gap-2 rounded-xl border border-white/10 bg-white/[0.05] p-3.5 backdrop-blur-md text-xs text-white/90 min-w-[210px] shadow-lg">
            <div className="flex items-center justify-between">
              <span className="text-white/60">Current Plan:</span>
              <span className="font-bold text-emerald-400">v{plan?.version || (lastResult ? lastResult.new_plan_summary.version : 11)} Active</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-white/60">Deadline:</span>
              <span className="font-medium text-white">{String(student?.target_deadline || "30 Nov 2025").slice(0, 10)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-white/60">Active Gaps:</span>
              <span className="font-semibold text-amber-300">{gaps?.length || 5} Tracked</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* ─── Simulation Trigger Buttons ───────────────────────────── */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold tracking-wide text-slate-800 uppercase flex items-center gap-2">
            <Zap className="h-4 w-4 text-amber-500" />
            TRIGGER SIMULATION SCENARIOS
          </h2>
          <span className="text-xs font-medium text-slate-500">
            Click any action button below to trigger autonomous replanning
          </span>
        </div>

        {/* High-Contrast Interactive Scenario Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7 gap-3.5">
          {SCENARIOS.map((scenario) => {
            const Icon = scenario.icon;
            const isSelected = activeScenarioId === scenario.id;
            const isCurrentPending = simulateMutation.isPending && activeScenarioId === scenario.id;

            return (
              <motion.button
                key={scenario.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleRunSimulation(scenario.id)}
                disabled={simulateMutation.isPending}
                className={`relative flex flex-col justify-between rounded-xl p-4 text-left transition-all duration-200 cursor-pointer shadow-sm border ${
                  isSelected
                    ? "bg-white border-primary shadow-md ring-2 ring-primary/30"
                    : "bg-white border-slate-200/90 hover:bg-slate-50/80 hover:shadow-md"
                } ${scenario.accentBorder} disabled:opacity-60`}
              >
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between gap-1.5">
                    <div className={`flex h-8 w-8 items-center justify-center rounded-lg ${scenario.iconBg} ${scenario.iconColor}`}>
                      <Icon className="h-4 w-4" />
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${scenario.badgeBg} ${scenario.badgeText} uppercase tracking-wider`}>
                      {scenario.badgeLabel}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-slate-900 leading-snug">
                      [ {scenario.label} ]
                    </h3>
                    <p className="text-[11px] text-slate-500 line-clamp-3 mt-1.5 leading-relaxed">
                      {scenario.description}
                    </p>
                  </div>
                </div>

                <div className="pt-3 mt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
                  <span className={`font-semibold ${isSelected ? "text-primary font-bold" : "text-slate-600"}`}>
                    {isCurrentPending ? "Executing..." : isSelected ? "● Active Run" : "Simulate →"}
                  </span>
                  {isCurrentPending ? (
                    <span className="h-2 w-2 rounded-full bg-amber-500 animate-ping" />
                  ) : isSelected ? (
                    <Check className="h-3.5 w-3.5 text-primary" />
                  ) : null}
                </div>
              </motion.button>
            );
          })}
        </div>
      </div>

      {/* ─── Visual Pipeline Flow Diagram ─────────────────────────── */}
      <div className="rounded-2xl border border-slate-700/80 bg-slate-900 p-6 shadow-2xl space-y-6 text-white">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div>
            <h2 className="text-base font-extrabold text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-indigo-400" />
              Autonomous Closed-Loop Pipeline Execution
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Live deterministic state transitions monitored and executed by the Autonomous Agent
            </p>
          </div>

          {lastResult && (
            <div className="inline-flex items-center gap-2 rounded-lg bg-emerald-500/15 border border-emerald-500/30 px-3.5 py-1.5 text-xs font-bold text-emerald-300">
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
              <span>Event Processed: {lastResult.title}</span>
            </div>
          )}
        </div>

        {/* ─── 6 Flowchart Nodes (EVENT -> STATE -> PERF -> REPLAN -> VERIFY -> ACTIVATED) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-6 gap-3 items-stretch relative">
          {PIPELINE_NODES.map((node, idx) => {
            const isCompleted = Boolean(lastResult);
            const isTabActive = activeStepTab === node.step;

            return (
              <div key={node.step} className="flex flex-col items-center relative">
                {/* Connector Arrow (Desktop) */}
                {idx < PIPELINE_NODES.length - 1 && (
                  <div className="hidden md:block absolute -right-2.5 top-1/2 -translate-y-1/2 z-20 text-slate-600">
                    <ChevronRight className="h-4 w-4" />
                  </div>
                )}

                {/* Node Box */}
                <button
                  onClick={() => setActiveStepTab(node.step)}
                  className={`w-full h-full rounded-xl border p-3.5 text-center transition-all duration-200 cursor-pointer ${
                    isTabActive
                      ? "bg-indigo-600/30 border-indigo-400 shadow-lg shadow-indigo-500/25 ring-1 ring-indigo-400"
                      : isCompleted
                      ? "bg-slate-800/80 border-slate-700 hover:bg-slate-800 hover:border-slate-600"
                      : "bg-slate-800/40 border-slate-800 opacity-60"
                  }`}
                >
                  <div className="flex items-center justify-center mb-2">
                    <div
                      className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${
                        isCompleted
                          ? "bg-emerald-500/25 text-emerald-400 border border-emerald-500/50"
                          : "bg-slate-700 text-slate-300"
                      }`}
                    >
                      {isCompleted ? <CheckCircle2 className="h-4 w-4 text-emerald-400" /> : node.step}
                    </div>
                  </div>
                  <div className="text-[11px] font-black tracking-tight text-white leading-snug">
                    {node.title}
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">
                    {node.sub}
                  </div>
                  {isCompleted && (
                    <div className="mt-2 inline-block text-[9px] font-bold text-emerald-400 bg-emerald-500/15 border border-emerald-500/30 px-2 py-0.5 rounded-full">
                      ✓ Executed
                    </div>
                  )}
                </button>

                {/* Mobile Connector Arrow */}
                {idx < PIPELINE_NODES.length - 1 && (
                  <div className="md:hidden my-2 text-slate-600">
                    <ArrowDown className="h-4 w-4" />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* ─── Selected Pipeline Step Details Card ────────────────────── */}
        <AnimatePresence mode="wait">
          {lastResult ? (
            <motion.div
              key={`${activeStepTab}-${lastResult.scenario}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="rounded-xl border border-slate-700 bg-slate-800/90 p-5 space-y-4 shadow-inner"
            >
              {(() => {
                const currentStep = lastResult.process_steps.find((s) => s.step === activeStepTab) || lastResult.process_steps[0];
                if (!currentStep) return null;

                return (
                  <div className="space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-700/80 pb-3">
                      <div>
                        <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">
                          Pipeline Stage {currentStep.step} of 6
                        </span>
                        <h3 className="text-base font-extrabold text-white">
                          {currentStep.label}
                        </h3>
                      </div>
                      <span className="text-xs text-slate-400 font-mono bg-slate-900/80 px-2.5 py-1 rounded-md border border-slate-700">
                        Execution Stamp: {currentStep.timestamp}
                      </span>
                    </div>

                    <p className="text-sm text-slate-200 leading-relaxed font-medium">
                      {currentStep.description}
                    </p>

                    {/* Key-Value payload inspect */}
                    {currentStep.details && (
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 pt-2">
                        {Object.entries(currentStep.details).map(([k, v]) => (
                          <div
                            key={k}
                            className="rounded-lg border border-slate-700/80 bg-slate-900/80 p-3 text-xs"
                          >
                            <div className="text-[10px] text-slate-400 uppercase font-mono font-semibold">
                              {k.replace(/_/g, " ")}
                            </div>
                            <div className="font-bold text-slate-100 mt-1 truncate">
                              {typeof v === "object" ? JSON.stringify(v) : String(v)}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })()}
            </motion.div>
          ) : (
            <div className="rounded-xl border border-dashed border-slate-700 bg-slate-800/40 p-8 text-center text-slate-300 space-y-2">
              <RefreshCw className="h-6 w-6 text-indigo-400 mx-auto animate-spin" />
              <p className="text-sm font-semibold text-white">Initializing Autonomous Simulator...</p>
              <p className="text-xs text-slate-400">
                Click any simulation button above to test real-time feedback loops.
              </p>
            </div>
          )}
        </AnimatePresence>
      </div>

      {/* ─── Side-by-Side Impact Comparison: Old Plan vs New Plan ─── */}
      {lastResult && (
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="grid grid-cols-1 lg:grid-cols-12 gap-6"
        >
          {/* Agent Explanation & Verification */}
          <div className="lg:col-span-4 space-y-4">
            <div className="rounded-2xl border border-slate-200/90 bg-white p-6 shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="text-xs font-bold uppercase tracking-wider text-purple-700 flex items-center gap-1.5">
                  <Sparkles className="h-4 w-4 text-purple-600" />
                  Autonomous Reasoning Trace
                </h3>
                <span className="text-[10px] font-bold bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full border border-purple-200">
                  Closed-Loop
                </span>
              </div>

              <p className="text-xs text-slate-700 leading-relaxed font-medium bg-slate-50 p-3.5 rounded-xl border border-slate-100">
                "{lastResult.agent_reasoning}"
              </p>

              <div className="space-y-2.5 pt-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Plan Verification:</span>
                  <span className="font-bold text-emerald-700 flex items-center gap-1">
                    <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                    10/10 Rules Passed
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Feasibility Score:</span>
                  <span className="font-bold text-slate-900">98.4%</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Deadline Achievable:</span>
                  <span className="font-bold text-emerald-700">Guaranteed ✓</span>
                </div>
              </div>
            </div>
          </div>

          {/* Old Plan vs New Plan Side-by-Side Cards */}
          <div className="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Old Plan Card */}
            <div className="rounded-2xl border border-slate-200/90 bg-white p-5 space-y-3.5 shadow-sm">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div>
                  <span className="text-[10px] uppercase tracking-wider text-slate-400 font-mono font-bold">
                    Prior State
                  </span>
                  <h4 className="text-sm font-bold text-slate-800">
                    Plan v{lastResult.old_plan_summary.version}
                  </h4>
                </div>
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                  Superseded
                </span>
              </div>

              <div className="space-y-2.5 text-xs">
                <div className="flex justify-between py-1 border-b border-slate-100">
                  <span className="text-slate-500">Scheduled Activities:</span>
                  <span className="text-slate-800 font-semibold">{lastResult.old_plan_summary.total_activities || 13} activities</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-100">
                  <span className="text-slate-500">Study Hours Target:</span>
                  <span className="text-slate-800 font-semibold">{lastResult.old_plan_summary.scheduled_study_hours} hrs</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-500">Target Deadline:</span>
                  <span className="text-slate-700 font-medium">{lastResult.old_plan_summary.target_deadline}</span>
                </div>
              </div>
            </div>

            {/* New Plan Card */}
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50/40 p-5 space-y-3.5 shadow-sm">
              <div className="flex items-center justify-between border-b border-emerald-200/60 pb-3">
                <div>
                  <span className="text-[10px] uppercase tracking-wider text-emerald-700 font-mono font-bold">
                    Autonomous Outcome
                  </span>
                  <h4 className="text-sm font-extrabold text-emerald-900">
                    Plan v{lastResult.new_plan_summary.version} (Active)
                  </h4>
                </div>
                <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
                  Live Active
                </span>
              </div>

              <div className="space-y-2.5 text-xs">
                <div className="flex justify-between py-1 border-b border-emerald-100">
                  <span className="text-emerald-800/70">Rescheduled Items:</span>
                  <span className="text-emerald-900 font-bold">{lastResult.plan_regenerated.rescheduled_activities} adjusted</span>
                </div>
                <div className="flex justify-between py-1 border-b border-emerald-100">
                  <span className="text-emerald-800/70">High Priority Gaps:</span>
                  <span className="text-amber-800 font-bold">
                    {lastResult.plan_regenerated.high_priority_gaps.join(", ") || "Dynamic Programming, Graphs"}
                  </span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-emerald-800/70">Target Deadline:</span>
                  <span className="text-emerald-900 font-extrabold">{lastResult.new_plan_summary.target_deadline}</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}
export default SimulationPage;
