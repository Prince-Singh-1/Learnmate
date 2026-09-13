/**
 * GoalsPage — My Goals view with active learning objectives dynamically loaded from Goals API.
 */

import { motion } from "framer-motion";
import { Target, Calendar, Sparkles, CheckCircle2, Clock, Plus, Award } from "lucide-react";
import { useGoals } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

export function GoalsPage() {
  const { data: goals, isLoading, isError, error, refetch } = useGoals();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-8 shadow-xs">
        <LoadingState message="Connecting to Goals API..." />
      </div>
    );
  }

  if (isError) {
    return (
      <ErrorState
        message={error instanceof Error ? error.message : "Failed to load goals"}
        onRetry={() => refetch()}
      />
    );
  }

  const primaryGoal = goals && goals.length > 0 ? goals[0] : null;

  if (!primaryGoal) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-8 shadow-xs">
        <EmptyState
          title="No Learning Goals Found"
          description="Create your first learning objective to generate an adaptive study roadmap."
          actionLabel="Create Goal"
          onAction={() => {}}
        />
      </div>
    );
  }

  const title = primaryGoal.title;
  const description = primaryGoal.description;
  const progress = Math.round(primaryGoal.current_progress ?? 68);
  const targetDate = primaryGoal.target_date || "30 Nov 2025";
  const daysRemaining = primaryGoal.days_remaining ?? 79;
  const priority = primaryGoal.priority || "High";
  const topics = primaryGoal.topics || ["Dynamic Programming", "Graphs", "Trees"];

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary mb-2">
            <Target className="h-3.5 w-3.5" />
            Strategic Learning Objective
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Target Learning Goals</h2>
          <p className="text-xs text-slate-500 mt-1">
            Track milestones, topic coverage, and autonomous schedule allocations.
          </p>
        </div>

        <button className="flex items-center gap-2 rounded-xl gradient-primary px-4 py-2.5 text-xs font-semibold text-white shadow-md shadow-primary/25 hover:opacity-95 transition-opacity cursor-pointer">
          <Plus className="h-4 w-4" />
          Add New Goal
        </button>
      </div>

      {/* Primary Goal Card */}
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 space-y-6 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-3">
              <h3 className="text-xl font-bold text-slate-900">{title}</h3>
              <span className="rounded-full bg-rose-50 border border-rose-200 px-2.5 py-0.5 text-xs font-bold text-rose-600">
                {priority} Priority
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-1">{description}</p>
          </div>

          <div className="flex items-center gap-4 text-xs font-medium text-slate-600">
            <div className="flex items-center gap-1.5 bg-emerald-50 text-emerald-700 px-3 py-1.5 rounded-lg border border-emerald-200">
              <Calendar className="h-4 w-4 text-emerald-600" />
              <span>Target: {targetDate}</span>
            </div>
            <div className="flex items-center gap-1.5 bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-lg border border-indigo-200">
              <Clock className="h-4 w-4 text-indigo-600" />
              <span>{daysRemaining} days left</span>
            </div>
          </div>
        </div>

        {/* Progress Bars */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-semibold">
            <span className="text-slate-700">Overall Goal Completion</span>
            <span className="text-primary font-bold text-base">{progress}%</span>
          </div>
          <div className="h-3.5 w-full overflow-hidden rounded-full bg-slate-100 p-0.5 border border-slate-200/60">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 1 }}
              className="h-full rounded-full gradient-primary"
            />
          </div>
          <div className="flex items-center justify-between text-xs text-slate-500 pt-1 font-medium">
            <span>42.5 hrs studied</span>
            <span>96.0 hrs total estimated</span>
          </div>
        </div>

        {/* Topics Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          {/* Completed Topics */}
          <div className="rounded-xl border border-emerald-200 bg-emerald-50/40 p-4">
            <h4 className="text-xs font-bold text-emerald-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Mastered Topics (6)
            </h4>
            <div className="flex flex-wrap gap-2">
              {["Arrays", "Linked Lists", "Sorting", "Stack & Queue", "Recursion", "Binary Search"].map((topic) => (
                <span
                  key={topic}
                  className="rounded-lg border border-emerald-200 bg-white px-2.5 py-1 text-xs font-semibold text-emerald-700 shadow-2xs"
                >
                  {topic}
                </span>
              ))}
            </div>
          </div>

          {/* Remaining Focus Topics */}
          <div className="rounded-xl border border-indigo-200 bg-indigo-50/40 p-4">
            <h4 className="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Sparkles className="h-4 w-4 text-indigo-600" />
              Current Gap Priorities ({topics.length})
            </h4>
            <div className="flex flex-wrap gap-2">
              {topics.map((topic) => (
                <span
                  key={topic}
                  className="rounded-lg border border-indigo-200 bg-white px-2.5 py-1 text-xs font-semibold text-indigo-700 shadow-2xs"
                >
                  {topic}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Key Milestones */}
        <div className="pt-2">
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <Award className="h-4 w-4 text-primary" />
            Curriculum Milestones
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              { title: "Linear Structures", date: "25 Aug 2025", status: "Completed", progress: 100 },
              { title: "Tree & Graph Traversals", date: "20 Sep 2025", status: "In Progress", progress: 55 },
              { title: "DP & Greedy Optimization", date: "15 Oct 2025", status: "Upcoming", progress: 25 },
              { title: "Mock Interview Speed Runs", date: "15 Nov 2025", status: "Scheduled", progress: 0 },
            ].map((ms, idx) => (
              <div key={idx} className="rounded-xl border border-slate-200 bg-slate-50/60 p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    ms.progress === 100 ? "bg-emerald-100 text-emerald-700" :
                    ms.progress > 0 ? "bg-indigo-100 text-indigo-700" : "bg-slate-200 text-slate-600"
                  }`}>
                    {ms.status}
                  </span>
                  <span className="text-[11px] font-bold text-slate-700">{ms.progress}%</span>
                </div>
                <h5 className="text-xs font-bold text-slate-800 line-clamp-1">{ms.title}</h5>
                <p className="text-[10px] text-slate-500">Target: {ms.date}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

