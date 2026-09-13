/**
 * GoalCard — Current Learning Goal card powered by Goals API.
 */

import { motion } from "framer-motion";
import { Target, Calendar, Hourglass, Flag, Edit3 } from "lucide-react";
import { useGoals } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

interface GoalCardProps {
  onEdit?: () => void;
}

export function GoalCard({ onEdit }: GoalCardProps) {
  const { data: goals, isLoading, isError, error, refetch } = useGoals();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <LoadingState message="Loading goal from Goals API..." className="p-4" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <ErrorState
          message={error instanceof Error ? error.message : "Failed to load goals"}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  const primaryGoal = goals && goals.length > 0 ? goals[0] : null;

  if (!primaryGoal) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full shadow-xs">
        <EmptyState
          title="No Learning Goal Set"
          description="Define a target learning goal to initiate autonomous planning."
          actionLabel="Add Goal"
          onAction={onEdit}
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

  return (
    <div className="card-3d p-5 h-full flex flex-col justify-between shadow-xs">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between pb-3">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-pink-50 text-pink-500 shadow-xs">
              <Target className="h-4 w-4" />
            </div>
            <h3 className="text-sm font-bold text-slate-800">My Learning Goal</h3>
          </div>
          <button
            onClick={onEdit}
            className="flex items-center gap-1 text-xs font-semibold text-primary hover:text-primary/80 transition-colors cursor-pointer"
          >
            <Edit3 className="h-3 w-3" />
            Edit
          </button>
        </div>

        {/* Goal Info */}
        <div className="mt-2 space-y-1">
          <h4 className="text-sm font-bold text-slate-900 tracking-tight">
            {title}
          </h4>
          <p className="text-xs text-slate-500 leading-relaxed">
            {description}
          </p>
        </div>

        {/* Progress Bar & Ring Indicator */}
        <div className="mt-4 space-y-2">
          <div className="flex justify-between items-center text-xs font-semibold">
            <span className="text-slate-500">Milestone Progress</span>
            <div className="flex items-center gap-2">
              {/* Subtle SVG progress ring */}
              <div className="relative h-6 w-6 flex items-center justify-center">
                <svg className="h-full w-full -rotate-90" viewBox="0 0 36 36">
                  <circle
                    cx="18"
                    cy="18"
                    r="14"
                    fill="none"
                    stroke="#e2e8f0"
                    strokeWidth="3.5"
                  />
                  <circle
                    cx="18"
                    cy="18"
                    r="14"
                    fill="none"
                    stroke="url(#goalGradient)"
                    strokeWidth="3.5"
                    strokeDasharray={`${(progress / 100) * 88} 88`}
                    strokeLinecap="round"
                  />
                  <defs>
                    <linearGradient id="goalGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#6366f1" />
                      <stop offset="100%" stopColor="#ec4899" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <span className="text-primary font-bold">{progress}%</span>
            </div>
          </div>
          <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-100 p-0.5 border border-slate-200/60 shadow-inner">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
              className="h-full rounded-full gradient-primary shadow-xs"
            />
          </div>
        </div>
      </div>

      {/* Metric Badges */}
      <div className="grid grid-cols-3 gap-2 pt-4 mt-2 border-t border-slate-100">
        <div className="rounded-xl border border-slate-200/60 bg-slate-50 p-2 text-center">
          <div className="flex items-center justify-center gap-1 text-[10px] text-slate-500 mb-1">
            <Calendar className="h-3 w-3 text-emerald-500" />
            Target Date
          </div>
          <p className="text-xs font-bold text-slate-800">{targetDate}</p>
        </div>

        <div className="rounded-xl border border-slate-200/60 bg-slate-50 p-2 text-center">
          <div className="flex items-center justify-center gap-1 text-[10px] text-slate-500 mb-1">
            <Hourglass className="h-3 w-3 text-purple-500" />
            Remaining
          </div>
          <p className="text-xs font-bold text-slate-800">
            {daysRemaining} days
          </p>
        </div>

        <div className="rounded-xl border border-slate-200/60 bg-slate-50 p-2 text-center">
          <div className="flex items-center justify-center gap-1 text-[10px] text-slate-500 mb-1">
            <Flag className="h-3 w-3 text-red-500" />
            Priority
          </div>
          <p className={`text-xs font-bold ${priority.toLowerCase() === "high" ? "text-red-500" : "text-amber-500"}`}>
            {priority}
          </p>
        </div>
      </div>
    </div>
  );
}

