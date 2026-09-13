/**
 * RecentActivityCard — Displays recent learning events dynamically from Activities API.
 */

import { motion } from "framer-motion";
import {
  CalendarCheck,
  CheckCircle2,
  XCircle,
  Clock,
  Award,
  ChevronRight,
} from "lucide-react";
import { useRecentActivities } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

interface RecentActivityCardProps {
  onViewAll?: () => void;
  onMissedActivityClick?: () => void;
}

export function RecentActivityCard({
  onViewAll,
  onMissedActivityClick,
}: RecentActivityCardProps) {
  const { data: activities, isLoading, isError, error, refetch } = useRecentActivities();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <LoadingState message="Loading recent activities..." className="p-4" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <ErrorState
          message={error instanceof Error ? error.message : "Failed to load recent activity feed"}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  const items = activities || [];

  if (items.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full shadow-xs">
        <EmptyState title="No Activity Yet" description="Your study session history will appear here." />
      </div>
    );
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="h-4 w-4 text-emerald-500" />;
      case "missed":
        return <XCircle className="h-4 w-4 text-red-500" />;
      case "scored":
        return <Award className="h-4 w-4 text-cyan-600" />;
      default:
        return <Clock className="h-4 w-4 text-purple-500" />;
    }
  };

  return (
    <div className="card-3d p-5 h-full flex flex-col justify-between shadow-xs">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600 shadow-xs">
              <CalendarCheck className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-800">
                Recent Activity
              </h3>
              <p className="text-[11px] text-slate-500 font-medium">
                Telemetry from completed study sessions
              </p>
            </div>
          </div>

          <button
            onClick={onViewAll}
            className="flex items-center gap-1 text-xs font-medium text-slate-500 hover:text-slate-800 transition-colors cursor-pointer"
          >
            <span>View All</span>
            <ChevronRight className="h-3 w-3 opacity-60" />
          </button>
        </div>
      </div>

      {/* Activity Items */}
      <div className="space-y-2 pt-3">
        {items.slice(0, 4).map((act, index) => {
          const status = String(act.status || "completed");
          const isMissed = status === "missed";
          const desc = String(act.description || act.title || "Study Session");
          const time = String(act.timestamp || "Today");

          return (
            <motion.div
              key={String(act.id || index)}
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.06 }}
              onClick={isMissed ? onMissedActivityClick : undefined}
              className={`flex items-center justify-between gap-2 rounded-xl p-2.5 border transition-all ${
                isMissed
                  ? "border-red-200 bg-red-50/50 cursor-pointer hover:bg-red-50"
                  : "border-slate-200/60 bg-slate-50/60 hover:bg-slate-50"
              }`}
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <div className="flex-shrink-0">{getStatusIcon(status)}</div>
                <div className="min-w-0">
                  <p className="text-xs font-semibold text-slate-800 truncate">
                    {desc}
                  </p>
                  <p className="text-[10px] text-slate-500">{time}</p>
                </div>
              </div>

              {isMissed && (
                <span className="flex-shrink-0 rounded-md bg-red-100 border border-red-200 px-2 py-0.5 text-[10px] font-bold text-red-600">
                  Replan
                </span>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

