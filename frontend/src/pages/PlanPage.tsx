/**
 * PlanPage — Interactive Learning Plan timeline connected to FastAPI plan & activity APIs.
 * Supports completing activities, marking missed activities, regenerating plans,
 * and triggering the autonomous re-planner.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import {
  CalendarDays,
  RefreshCw,
  CheckCircle2,
  Clock,
  Sparkles,
  AlertTriangle,
  Check,
  XCircle,
} from "lucide-react";
import { AutonomousReplanModal } from "@/components/dashboard";
import {
  useLearningPlan,
  useGeneratePlan,
  useCompleteActivity,
  useMissActivity,
  useTriggerReplan,
} from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

export function PlanPage() {
  const [filter, setFilter] = useState<string>("all");
  const [replanModalOpen, setReplanModalOpen] = useState(false);
  const [replanReason, setReplanReason] = useState<string>(
    "User Requested Strategic Schedule Optimization"
  );
  const [optimisticOverrides, setOptimisticOverrides] = useState<Record<string, string>>({});

  const { data: plan, isLoading, isError, error, refetch } = useLearningPlan();
  const generatePlanMutation = useGeneratePlan();
  const completeActivityMutation = useCompleteActivity();
  const missActivityMutation = useMissActivity();
  const triggerReplanMutation = useTriggerReplan();

  if (isLoading) {
    return <LoadingState message="Loading your personalized adaptive learning plan..." />;
  }

  if (isError) {
    return (
      <ErrorState
        error={error}
        onRetry={() => refetch()}
        title="Could Not Load Learning Plan"
      />
    );
  }

  const activities = (plan?.activities || []).map((act) => ({
    ...act,
    status: optimisticOverrides[act.id] || act.status,
  }));

  const handleGeneratePlan = () => {
    generatePlanMutation.mutate("stu-001");
  };

  const handleComplete = (activityId: string) => {
    // Instant optimistic visual feedback
    setOptimisticOverrides((prev) => ({ ...prev, [activityId]: "completed" }));
    completeActivityMutation.mutate(
      { activityId },
      {
        onError: () => {
          setOptimisticOverrides((prev) => {
            const copy = { ...prev };
            delete copy[activityId];
            return copy;
          });
        },
      }
    );
  };

  const handleMiss = (activityId: string, title: string) => {
    setOptimisticOverrides((prev) => ({ ...prev, [activityId]: "missed" }));
    missActivityMutation.mutate(
      { activityId, reason: "Activity missed by user" },
      {
        onSuccess: () => {
          setReplanReason(`Missed session: ${title} (Autonomous re-balance scheduled)`);
          setReplanModalOpen(true);
        },
        onError: () => {
          setOptimisticOverrides((prev) => {
            const copy = { ...prev };
            delete copy[activityId];
            return copy;
          });
        },
      }
    );
  };

  const filteredActivities = activities.filter((act) => {
    if (filter === "all") return true;
    return act.status === filter;
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Plan Header Card */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-5 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary">
              <CalendarDays className="h-3.5 w-3.5" />
              Plan v{plan?.version ?? 1}
            </span>
            {plan?.deadline_guaranteed ? (
              <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 text-xs font-bold text-emerald-700">
                <Check className="h-3 w-3" />
                Deadline Guaranteed
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 border border-amber-200 px-2.5 py-0.5 text-xs font-bold text-amber-700">
                <AlertTriangle className="h-3 w-3" />
                Feasibility Alert
              </span>
            )}
            <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600">
              Target: {plan?.target_deadline || "30 Nov 2025"} ({plan?.remaining_days ?? 0} days left)
            </span>
          </div>

          <h2 className="text-2xl font-bold text-slate-900">
            {plan?.title || plan?.goal || "Adaptive Machine Learning & Algorithms Plan"}
          </h2>
          <p className="text-xs text-slate-500 max-w-2xl">
            Real-time deterministic schedule synthesized to close high-severity knowledge gaps
            before deadline. Total required: <span className="font-semibold text-slate-700">{plan?.required_study_hours ?? 0} hrs</span> •
            Scheduled: <span className="font-semibold text-slate-700">{plan?.scheduled_study_hours ?? 0} hrs</span>.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={handleGeneratePlan}
            disabled={generatePlanMutation.isPending}
            className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 px-4 py-2.5 text-xs font-semibold text-slate-700 shadow-2xs transition-all disabled:opacity-50"
          >
            <Sparkles className={`h-4 w-4 text-primary ${generatePlanMutation.isPending ? "animate-spin" : ""}`} />
            {generatePlanMutation.isPending ? "Generating..." : "Generate New Plan"}
          </button>

          <button
            onClick={() => {
              setReplanReason("User initiated manual schedule rebalance");
              setReplanModalOpen(true);
            }}
            disabled={triggerReplanMutation.isPending}
            className="flex items-center gap-2 rounded-xl gradient-primary px-4 py-2.5 text-xs font-semibold text-white shadow-md shadow-primary/25 hover:opacity-95 transition-all"
          >
            <RefreshCw className={`h-4 w-4 ${triggerReplanMutation.isPending ? "animate-spin" : ""}`} />
            Autonomous Replan
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between gap-4 overflow-x-auto pb-1">
        <div className="flex items-center gap-2">
          {["all", "pending", "completed", "missed"].map((tab) => {
            const count =
              tab === "all"
                ? activities.length
                : activities.filter((a) => a.status === tab).length;
            return (
              <button
                key={tab}
                onClick={() => setFilter(tab)}
                className={`rounded-xl px-4 py-2 text-xs font-semibold capitalize transition-all flex items-center gap-1.5 ${
                  filter === tab
                    ? "gradient-primary text-white shadow-xs"
                    : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                }`}
              >
                <span>{tab.replace("_", " ")}</span>
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  filter === tab ? "bg-white/20 text-white" : "bg-slate-100 text-slate-500"
                }`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        <span className="text-xs text-slate-400 font-medium hidden sm:inline">
          Interactive activities update backend in real-time
        </span>
      </div>

      {/* Activity Timeline List */}
      {filteredActivities.length === 0 ? (
        <EmptyState
          title={`No ${filter === "all" ? "" : filter} activities`}
          description={
            filter === "all"
              ? "Your learning plan has no scheduled activities. Click 'Generate New Plan' to synthesize one."
              : `There are currently no activities with status '${filter}'.`
          }
          actionLabel="Generate Plan"
          onAction={handleGeneratePlan}
        />
      ) : (
        <div className="space-y-3">
          {filteredActivities.map((act, index) => {
            const isCompleted = act.status === "completed";
            const isMissed = act.status === "missed";
            const isPending = act.status === "pending" || act.status === "in_progress";

            return (
              <motion.div
                key={act.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.04 }}
                className={`flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-2xl border p-4 transition-all ${
                  isCompleted
                    ? "border-emerald-200 bg-emerald-50/30"
                    : isMissed
                    ? "border-rose-200 bg-rose-50/30"
                    : "border-slate-200/80 bg-white hover:border-indigo-200 shadow-2xs"
                }`}
              >
                <div className="flex items-start sm:items-center gap-3.5">
                  <button
                    onClick={() => !isCompleted && handleComplete(act.id)}
                    disabled={completeActivityMutation.isPending}
                    title={isCompleted ? "Completed" : "Click to mark complete"}
                    className="mt-0.5 sm:mt-0 flex-shrink-0 transition-transform active:scale-90"
                  >
                    {isCompleted ? (
                      <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                    ) : isMissed ? (
                      <XCircle className="h-5 w-5 text-rose-400" />
                    ) : (
                      <div className="h-5 w-5 rounded-full border-2 border-slate-300 hover:border-primary transition-colors" />
                    )}
                  </button>

                  <div>
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-slate-100 border border-slate-200 px-2 py-0.5 text-[10px] font-bold text-slate-600 uppercase">
                        {act.type}
                      </span>
                      <span className="text-[11px] font-semibold text-primary">
                        {act.topic}
                      </span>
                    </div>
                    <h4
                      className={`text-sm font-bold mt-1 ${
                        isCompleted
                          ? "line-through text-slate-400"
                          : isMissed
                          ? "text-rose-900"
                          : "text-slate-900"
                      }`}
                    >
                      {act.title}
                    </h4>
                    <div className="flex items-center gap-3 text-xs text-slate-500 mt-1 font-medium">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3 text-slate-400" />
                        {act.duration_minutes} mins
                      </span>
                      {act.scheduled_start && (
                        <span>• Scheduled: {act.scheduled_start}</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Actions & Status badge */}
                <div className="flex items-center gap-2 self-end sm:self-center">
                  {isPending && (
                    <>
                      <button
                        onClick={() => handleComplete(act.id)}
                        disabled={completeActivityMutation.isPending}
                        className="flex items-center gap-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-3 py-1.5 text-xs font-semibold text-emerald-700 transition-colors"
                      >
                        <Check className="h-3.5 w-3.5" />
                        Complete
                      </button>

                      <button
                        onClick={() => handleMiss(act.id, act.title)}
                        disabled={missActivityMutation.isPending}
                        className="flex items-center gap-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 border border-rose-200 px-2.5 py-1.5 text-xs font-medium text-rose-700 transition-colors"
                      >
                        Miss
                      </button>
                    </>
                  )}

                  <span
                    className={`rounded-lg px-2.5 py-1 text-xs font-bold capitalize ${
                      isCompleted
                        ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                        : isMissed
                        ? "bg-rose-100 text-rose-800 border border-rose-200"
                        : "bg-slate-100 text-slate-600 border border-slate-200"
                    }`}
                  >
                    {act.status.replace("_", " ")}
                  </span>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}

      <AutonomousReplanModal
        isOpen={replanModalOpen}
        onClose={() => setReplanModalOpen(false)}
        triggerReason={replanReason}
      />
    </motion.div>
  );
}
