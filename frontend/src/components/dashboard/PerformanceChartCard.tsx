/**
 * PerformanceChartCard — Performance Overview chart with score vs target line trends.
 */

import { useState } from "react";
import { TrendingUp, ChevronDown } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { usePerformance } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";

export function PerformanceChartCard() {
  const [timeframe] = useState("Weekly telemetry");
  const { data: perf, isLoading, isError, error, refetch } = usePerformance();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <LoadingState message="Loading telemetry from Performance API..." className="p-4" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full flex items-center justify-center shadow-xs">
        <ErrorState
          message={error instanceof Error ? error.message : "Failed to load performance telemetry"}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  const chartData = (perf?.points || []).map((pt: any) => ({
    week: pt.week || pt.day || "Week",
    score: pt.score ?? pt.points ?? 0,
    target: pt.target ?? 80,
    hours: pt.hours ?? 3.5,
  }));

  if (chartData.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-5 h-full shadow-xs">
        <EmptyState title="No Performance Data" description="Complete study sessions to generate performance trends." />
      </div>
    );
  }

  const overallMastery = Math.round(perf?.overall_mastery ?? 68);

  return (
    <div className="card-3d p-5 h-full flex flex-col justify-between shadow-xs">
      {/* Header */}
      <div className="flex items-center justify-between pb-2">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-primary">
            <TrendingUp className="h-4 w-4" />
          </div>
          <h3 className="text-sm font-bold text-slate-800">
            Performance Overview
          </h3>
        </div>

        {/* Dropdown button */}
        <div className="relative">
          <button className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs font-medium text-slate-700 hover:bg-slate-100 transition-colors">
            <span>{timeframe}</span>
            <ChevronDown className="h-3 w-3 opacity-60" />
          </button>
        </div>
      </div>

      {/* Legend & Stat pill */}
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs py-2">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-indigo-600 shadow-xs" />
            <span className="text-slate-600 font-medium text-[11px]">Mastery Score</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-0.5 w-3 bg-cyan-500 border-dashed" />
            <span className="text-slate-500 text-[11px]">Target (80%)</span>
          </div>
        </div>

        <div className="inline-flex items-center gap-1.5 rounded-lg border border-indigo-200 bg-indigo-50 px-2 py-0.5 text-[11px] font-semibold text-primary">
          <span>{overallMastery}%</span>
          <span className="text-emerald-600 font-bold">+12% velocity</span>
        </div>
      </div>

      {/* Chart Area */}
      <div className="h-[180px] w-full mt-2">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 10, right: 10, left: -25, bottom: 0 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#f1f5f9"
              vertical={false}
            />
            <XAxis
              dataKey="week"
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#ffffff",
                borderColor: "#e2e8f0",
                borderRadius: "0.75rem",
                boxShadow: "0 10px 25px -5px rgba(0,0,0,0.1)",
                fontSize: "12px",
                color: "#0f172a",
              }}
              formatter={(value: any, name: any) => [
                `${value}%`,
                name === "score" ? "Mastery Score" : "Target",
              ]}
            />
            <Line
              type="monotone"
              dataKey="target"
              stroke="#06b6d4"
              strokeDasharray="4 4"
              strokeWidth={2}
              dot={{ r: 3, fill: "#06b6d4" }}
              animationDuration={1200}
              animationEasing="ease-out"
            />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#6366f1"
              strokeWidth={3.5}
              dot={{ r: 4.5, fill: "#6366f1", strokeWidth: 2, stroke: "#ffffff" }}
              activeDot={{ r: 7, fill: "#8b5cf6", stroke: "#ffffff", strokeWidth: 2 }}
              animationDuration={1400}
              animationEasing="ease-out"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

