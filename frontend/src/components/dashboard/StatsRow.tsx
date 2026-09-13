/**
 * StatsRow — Horizontal summary metric bar dynamically powered by Student API.
 */

import { motion } from "framer-motion";
import { BarChart3, Flame, Trophy, Clock, Sparkles } from "lucide-react";
import { useStudent } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState } from "@/components/ui/states";

export function StatsRow() {
  const { data: student, isLoading, isError, error, refetch } = useStudent();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-4 shadow-xs">
        <LoadingState message="Connecting to Student API telemetry..." className="py-2" />
      </div>
    );
  }

  if (isError) {
    return (
      <ErrorState
        message={error instanceof Error ? error.message : "Failed to load student metrics"}
        onRetry={() => refetch()}
        className="py-3"
      />
    );
  }

  const progress = student?.overall_progress ?? 68.5;
  const streak = student?.study_streak ?? 14;
  const topicsCompleted = student?.topics_completed ?? 6;
  const timeSpent = `${student?.time_spent_hours ?? 42.5} hrs`;

  const statItems = [
    {
      id: "progress",
      label: "Overall Progress",
      value: `${progress}%`,
      icon: BarChart3,
      iconColor: "text-emerald-500",
      bgColor: "bg-emerald-50",
      borderColor: "border-slate-200/80",
    },
    {
      id: "streak",
      label: "Day Streak",
      value: `${streak}`,
      icon: Flame,
      iconColor: "text-orange-500",
      bgColor: "bg-orange-50",
      borderColor: "border-slate-200/80",
    },
    {
      id: "topics",
      label: "Topics Completed",
      value: `${topicsCompleted}`,
      icon: Trophy,
      iconColor: "text-amber-500",
      bgColor: "bg-amber-50",
      borderColor: "border-slate-200/80",
    },
    {
      id: "time",
      label: "Time Spent",
      value: timeSpent,
      icon: Clock,
      iconColor: "text-blue-500",
      bgColor: "bg-blue-50",
      borderColor: "border-slate-200/80",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
      {statItems.map((item, index) => {
        const Icon = item.icon;
        return (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ y: -2, transition: { duration: 0.2 } }}
            className={`flex items-center gap-3 rounded-2xl border ${item.borderColor} bg-white p-3.5 shadow-xs`}
          >
            <div
              className={`flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl ${item.bgColor} ${item.iconColor}`}
            >
              <Icon className="h-5 w-5" />
            </div>
            <div>
              <p className="text-lg font-extrabold tracking-tight text-slate-900">
                {item.value}
              </p>
              <p className="text-[11px] text-slate-500 font-medium">{item.label}</p>
            </div>
          </motion.div>
        );
      })}

      {/* Motivational item */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
        whileHover={{ y: -2, transition: { duration: 0.2 } }}
        className="col-span-2 md:col-span-1 flex items-center gap-3 rounded-2xl border border-purple-200/80 bg-white p-3.5 shadow-xs"
      >
        <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl bg-purple-50 text-purple-600">
          <Sparkles className="h-5 w-5" />
        </div>
        <div>
          <p className="text-xs font-semibold text-purple-700 italic">
            "Consistency beats intensity every time."
          </p>
          <p className="text-[10px] text-slate-400 mt-0.5 font-medium">Daily Affirmation</p>
        </div>
      </motion.div>
    </div>
  );
}

