/**
 * TodaySchedule — Today's study plan dynamically powered by Activities API.
 * Updates UI immediately upon completing or missing an activity.
 */

import { motion, AnimatePresence } from "framer-motion";
import {
  Calendar as CalendarIcon,
  ChevronLeft,
  ChevronRight,
  CheckCircle2,
  Circle,
  PlayCircle,
  Clock,
  ExternalLink,
  AlertTriangle,
} from "lucide-react";
import {
  useTodayActivities,
  useCompleteActivity,
  useMissActivity,
  type ActivityData,
} from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

interface TodayScheduleProps {
  onViewCalendar?: () => void;
  onStudyNow?: (item: ActivityData) => void;
}

export function TodaySchedule({ onViewCalendar, onStudyNow }: TodayScheduleProps) {
  const { data: activities, isLoading, isError, error, refetch } = useTodayActivities();
  const completeMutation = useCompleteActivity();
  const missMutation = useMissActivity();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <LoadingState message="Loading today's activities from API..." className="p-4" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <ErrorState
          message={error instanceof Error ? error.message : "Failed to load today's activities"}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  const items = activities || [];

  if (items.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full shadow-xs">
        <EmptyState
          title="No Activities Scheduled"
          description="All caught up! The autonomous agent will schedule your next study blocks soon."
        />
      </div>
    );
  }

  const completedCount = items.filter((i) => i.completed || i.status === "completed").length;
  const missedCount = items.filter((i) => i.missed || i.status === "missed").length;

  return (
    <div className="card-3d p-5 h-full flex flex-col justify-between shadow-xs">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-primary shadow-xs">
              <CalendarIcon className="h-4 w-4" />
            </div>
            <div>
              <span className="text-sm font-bold text-slate-800">
                Today's Schedule
              </span>
            </div>
            <div className="flex items-center gap-0.5 ml-1">
              <button
                className="p-1 text-slate-400 hover:text-slate-700 rounded-md hover:bg-slate-100 transition-colors"
                title="Previous Day"
              >
                <ChevronLeft className="h-3.5 w-3.5" />
              </button>
              <button
                className="p-1 text-slate-400 hover:text-slate-700 rounded-md hover:bg-slate-100 transition-colors"
                title="Next Day"
              >
                <ChevronRight className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          <button
            onClick={onViewCalendar}
            className="flex items-center gap-1.5 rounded-lg bg-blue-600 px-3 py-1 text-xs font-semibold text-white hover:bg-blue-700 transition-colors shadow-xs cursor-pointer"
          >
            <span>View Calendar</span>
            <ExternalLink className="h-3 w-3 opacity-80" />
          </button>
        </div>

        {/* Schedule List */}
        <div className="space-y-2.5 pt-4">
          <AnimatePresence>
            {items.map((item, index) => {
              const isDone = item.completed || item.status === "completed";
              const isMissed = item.missed || item.status === "missed";
              const isCurrent = !isDone && !isMissed && index === 0;

              return (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.08 }}
                  className={`group relative flex items-center justify-between gap-3 rounded-xl p-3 border transition-all ${
                    isCurrent
                      ? "border-primary/40 bg-indigo-50/50 shadow-xs"
                      : isDone
                      ? "border-emerald-200 bg-emerald-50/40"
                      : isMissed
                      ? "border-rose-200 bg-rose-50/40"
                      : "border-slate-200/70 bg-slate-50/60 hover:bg-slate-50 hover:border-slate-300"
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    {/* Status indicator toggle */}
                    <button
                      onClick={() => {
                        if (!isDone) {
                          completeMutation.mutate({ activityId: item.id });
                        }
                      }}
                      disabled={completeMutation.isPending}
                      className="flex-shrink-0 transition-transform active:scale-90 cursor-pointer"
                      title={isDone ? "Completed" : "Click to mark completed"}
                    >
                      {isDone ? (
                        <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                      ) : isMissed ? (
                        <AlertTriangle className="h-5 w-5 text-rose-500" />
                      ) : isCurrent ? (
                        <div className="relative flex h-5 w-5 items-center justify-center">
                          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-400 opacity-40" />
                          <Circle className="relative h-5 w-5 text-primary stroke-[2.5]" />
                        </div>
                      ) : (
                        <Circle className="h-5 w-5 text-slate-300 group-hover:text-slate-400" />
                      )}
                    </button>

                    {/* Activity details */}
                    <div className="min-w-0">
                      <p
                        className={`text-xs sm:text-sm font-semibold truncate ${
                          isDone
                            ? "text-slate-400 line-through"
                            : isMissed
                            ? "text-rose-600 line-through"
                            : isCurrent
                            ? "text-slate-900"
                            : "text-slate-800"
                        }`}
                      >
                        {item.title}
                      </p>
                      <div className="flex items-center gap-2 text-[11px] text-slate-500 mt-0.5">
                        <Clock className="h-3 w-3 opacity-70" />
                        <span>{item.duration_minutes} mins • {item.topic}</span>
                        {isMissed && (
                          <span className="text-[10px] text-rose-600 font-bold bg-rose-100/80 px-1.5 py-0.2 rounded">
                            Missed
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Actions (Complete / Miss / Study) */}
                  <div className="flex items-center gap-1.5">
                    {!isDone && !isMissed && (
                      <button
                        onClick={() => missMutation.mutate({ activityId: item.id, reason: "Session skipped" })}
                        disabled={missMutation.isPending}
                        className="p-1 rounded-md text-slate-400 hover:text-rose-500 hover:bg-rose-50 transition-colors text-xs cursor-pointer"
                        title="Mark Missed (triggers auto-replan)"
                      >
                        <AlertTriangle className="h-3.5 w-3.5" />
                      </button>
                    )}

                    {isCurrent && !isDone && (
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => onStudyNow?.(item)}
                        className="flex-shrink-0 flex items-center gap-1.5 rounded-lg gradient-primary px-3 py-1.5 text-xs font-semibold text-white shadow-xs cursor-pointer"
                      >
                        <PlayCircle className="h-3.5 w-3.5" />
                        Study Now
                      </motion.button>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      </div>

      {/* Footer stats badge */}
      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
        <span>{items.length} Activities Today ({completedCount} done, {missedCount} missed)</span>
        <span className="text-emerald-600 font-bold">
          {items.length > 0 ? `${Math.round((completedCount / items.length) * 100)}% completed` : "Ready"}
        </span>
      </div>
    </div>
  );
}

