/**
 * TopicMasteryCard — Topic mastery progress bars dynamically powered by Performance API.
 */

import { motion } from "framer-motion";
import { Layers, ChevronRight } from "lucide-react";
import { usePerformance, useKnowledgeGaps } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

interface TopicMasteryCardProps {
  onViewDetails?: () => void;
}

const TOPIC_COLORS: Record<string, string> = {
  "Dynamic Programming": "#ec4899",
  "Graphs": "#8b5cf6",
  "Trees": "#06b6d4",
  "Binary Trees": "#06b6d4",
  "Arrays & Strings": "#10b981",
  "Sorting": "#f59e0b",
  "Heaps": "#f97316",
};

export function TopicMasteryCard({ onViewDetails }: TopicMasteryCardProps) {
  const { data: perf, isLoading, isError, error, refetch } = usePerformance();
  const { data: gaps } = useKnowledgeGaps();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <LoadingState message="Loading mastery breakdown..." className="p-4" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <ErrorState
          message={error instanceof Error ? error.message : "Failed to load topic mastery"}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  const masteryList = perf?.topic_mastery || [];

  if (masteryList.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full shadow-xs">
        <EmptyState title="No Topics" description="No topic mastery telemetry recorded yet." />
      </div>
    );
  }

  // Create gap lookup safely
  const gapList = Array.isArray(gaps) ? gaps : ((gaps as any)?.gaps || []);
  const gapSet = new Set(gapList.map((g: any) => (g?.topic || "").toLowerCase()));

  return (
    <div className="card-3d p-5 h-full flex flex-col justify-between shadow-xs">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-100">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-cyan-50 text-cyan-600 shadow-xs">
            <Layers className="h-4 w-4" />
          </div>
          <h3 className="text-sm font-bold text-slate-800">Topic Mastery</h3>
        </div>
        <button
          onClick={onViewDetails}
          className="flex items-center gap-1 text-xs font-medium text-slate-500 hover:text-slate-800 transition-colors cursor-pointer"
        >
          <span>View Details</span>
          <ChevronRight className="h-3 w-3 opacity-60" />
        </button>
      </div>

      {/* Mastery List with Mini Progress Rings */}
      <div className="space-y-3 pt-3">
        {masteryList.slice(0, 5).map((item: any) => {
          const topicName = item?.topic || "Topic";
          const color = TOPIC_COLORS[topicName] || item?.color || "#6366f1";
          const score = Math.round(item?.mastery ?? item?.mastery_score ?? 0);
          const hasGap = gapSet.has(topicName.toLowerCase());

          return (
            <div key={topicName} className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  {/* Mini SVG Progress Ring */}
                  <div className="relative h-4 w-4 flex items-center justify-center flex-shrink-0">
                    <svg className="h-full w-full -rotate-90" viewBox="0 0 32 32">
                      <circle cx="16" cy="16" r="12" fill="none" stroke="#e2e8f0" strokeWidth="3" />
                      <circle
                        cx="16"
                        cy="16"
                        r="12"
                        fill="none"
                        stroke={color}
                        strokeWidth="3"
                        strokeDasharray={`${(score / 100) * 75.4} 75.4`}
                        strokeLinecap="round"
                      />
                    </svg>
                  </div>
                  <span className="font-semibold text-slate-700 text-[12px]">
                    {topicName}
                  </span>
                  {hasGap && (
                    <span className="text-[10px] px-1.5 py-0.2 rounded bg-rose-50 border border-rose-200 text-rose-600 font-medium">
                      Gap
                    </span>
                  )}
                </div>
                <span className="font-bold text-slate-900 text-[12px]">
                  {score}%
                </span>
              </div>

              {/* Progress track */}
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${score}%` }}
                  transition={{ duration: 0.8, ease: "easeOut" }}
                  style={{ backgroundColor: color }}
                  className="h-full rounded-full"
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}


