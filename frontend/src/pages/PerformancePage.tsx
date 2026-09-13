/**
 * PerformancePage — Detailed analytics and knowledge gaps dynamically powered by API.
 */

import { motion } from "framer-motion";
import { BarChart3, TrendingUp, Layers } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
} from "recharts";
import { usePerformance, useKnowledgeGaps } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

export function PerformancePage() {
  const { data: perf, isLoading: perfLoading, isError: perfError, error: perfErr, refetch: refetchPerf } = usePerformance();
  const { data: gaps, isLoading: gapsLoading, isError: gapsError, error: gapsErr, refetch: refetchGaps } = useKnowledgeGaps();

  if (perfLoading || gapsLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-8 shadow-xs">
        <LoadingState message="Fetching analytics from Performance & Gaps API..." />
      </div>
    );
  }

  if (perfError || gapsError) {
    return (
      <ErrorState
        message={(perfErr || gapsErr)?.message || "Failed to load performance analytics"}
        onRetry={() => {
          refetchPerf();
          refetchGaps();
        }}
      />
    );
  }

  const topicMasteryList = perf?.topic_mastery || [];
  const masteryChartData = topicMasteryList.map((tm: any) => ({
    name: tm.topic,
    mastery: Math.round(tm.mastery ?? tm.mastery_score ?? 0),
  }));

  const trendData = (perf?.points || []).map((pt: any) => ({
    week: pt.week || pt.day || "Week",
    score: pt.score ?? pt.points ?? 0,
    target: pt.target ?? 80,
  }));

  const knowledgeGapList = Array.isArray(gaps) ? gaps : ((gaps as any)?.gaps || []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary mb-2">
            <BarChart3 className="h-3.5 w-3.5" />
            Learning Analytics & Trajectory
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Performance Overview</h2>
          <p className="text-xs text-slate-500 mt-1">
            Real-time evaluation of concept retention, quiz velocity, and knowledge gaps.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-3.5 py-2 text-center">
            <p className="text-xs text-emerald-700 font-bold">+12% Velocity</p>
            <p className="text-[10px] text-emerald-600/80 font-medium">Above goal baseline</p>
          </div>
        </div>
      </div>

      {/* Two main charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Trend Line */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-primary" />
              Weekly Score vs Target Trend
            </h3>
            <span className="text-xs text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
              {Math.round(perf?.overall_mastery ?? 68)}% Overall Mastery
            </span>
          </div>

          <div className="h-64 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="week" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    borderColor: "#e2e8f0",
                    borderRadius: "0.75rem",
                    color: "#0f172a",
                    boxShadow: "0 4px 12px rgba(15, 23, 42, 0.08)",
                  }}
                />
                <Line type="monotone" dataKey="target" stroke="#06b6d4" strokeDasharray="4 4" strokeWidth={2} name="Target" />
                <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={3} dot={{ r: 4, fill: "#6366f1" }} name="Your Score" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Topic Mastery Distribution */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Layers className="h-4 w-4 text-cyan-600" />
              Mastery By Topic
            </h3>
            <span className="text-xs text-slate-500 font-medium">Target: 80%</span>
          </div>

          <div className="h-64 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={masteryChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={10} />
                <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    borderColor: "#e2e8f0",
                    borderRadius: "0.75rem",
                    color: "#0f172a",
                    boxShadow: "0 4px 12px rgba(15, 23, 42, 0.08)",
                  }}
                />
                <Bar dataKey="mastery" fill="#8b5cf6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Identified Knowledge Gaps Breakdown */}
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <h3 className="text-sm font-bold text-slate-900 mb-4">
          Identified Knowledge Gaps (From Diagnostic Telemetry)
        </h3>
        {knowledgeGapList.length === 0 ? (
          <EmptyState title="Zero Knowledge Gaps" description="All topics currently meet the target mastery threshold." />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {knowledgeGapList.map((gap: any) => {
              const estimatedHours = gap.estimated_hours ?? gap.estimated_learning_hours ?? (
                gap.severity === "High" ? 6.0 : gap.severity === "Medium" ? 4.0 : 2.0
              );
              const description = gap.reason || gap.description || gap.recommended_action || "Targeted concept remediation required";

              return (
                <div
                  key={gap.id}
                  className={`rounded-xl p-4 border ${
                    gap.severity === "High"
                      ? "border-rose-200 bg-rose-50/40"
                      : gap.severity === "Medium"
                      ? "border-amber-200 bg-amber-50/40"
                      : "border-sky-200 bg-sky-50/40"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-slate-900">{gap.topic}</span>
                    <span
                      className={`rounded px-2 py-0.5 text-[10px] font-bold ${
                        gap.severity === "High"
                          ? "bg-rose-100 text-rose-800"
                          : gap.severity === "Medium"
                          ? "bg-amber-100 text-amber-800"
                          : "bg-sky-100 text-sky-800"
                      }`}
                    >
                      {gap.severity} Priority
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 line-clamp-2">{description}</p>
                  <div className="mt-3 flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span>Estimated Remediation</span>
                    <span className="font-bold text-slate-900">{estimatedHours} hrs</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </motion.div>
  );
}

