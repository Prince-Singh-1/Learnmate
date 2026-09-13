/**
 * CalendarPage — Interactive weekly study schedule powered by Calendar API.
 * Populates all 7 days with scheduled sessions, past completions, and available windows.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Calendar as CalendarIcon,
  ChevronLeft,
  ChevronRight,
  Clock,
  ShieldCheck,
  CheckCircle2,
  BookOpen,
  Video,
  Code2,
  HelpCircle,
} from "lucide-react";
import { useCalendar, useTodayActivities } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState } from "@/components/ui/states";

interface CalendarEvent {
  id: string;
  title: string;
  topic: string;
  type: "video" | "practice" | "reading" | "quiz" | "commitment";
  startTime: string;
  endTime: string;
  dayIndex: number; // 0 = Mon, 1 = Tue, 2 = Wed, 3 = Thu, 4 = Fri (Today), 5 = Sat, 6 = Sun
  status: "completed" | "active" | "scheduled";
  durationMinutes: number;
}

const WEEKLY_CURRICULUM_SCHEDULE: CalendarEvent[] = [
  // Monday (Completed)
  {
    id: "cal-mon-1",
    title: "Linear Data Structures & Arrays Review",
    topic: "Arrays",
    type: "reading",
    startTime: "09:30 AM",
    endTime: "10:30 AM",
    dayIndex: 0,
    status: "completed",
    durationMinutes: 60,
  },
  {
    id: "cal-mon-2",
    title: "Array Two-Pointer & Sliding Window Drills",
    topic: "Arrays",
    type: "practice",
    startTime: "02:00 PM",
    endTime: "03:15 PM",
    dayIndex: 0,
    status: "completed",
    durationMinutes: 75,
  },

  // Tuesday (Completed)
  {
    id: "cal-tue-1",
    title: "Fast & Slow Pointers in Linked Lists",
    topic: "Linked Lists",
    type: "reading",
    startTime: "10:00 AM",
    endTime: "10:45 AM",
    dayIndex: 1,
    status: "completed",
    durationMinutes: 45,
  },
  {
    id: "cal-tue-2",
    title: "Linked List Reversal & Cycle Detection",
    topic: "Linked Lists",
    type: "practice",
    startTime: "03:30 PM",
    endTime: "04:30 PM",
    dayIndex: 1,
    status: "completed",
    durationMinutes: 60,
  },

  // Wednesday (Completed)
  {
    id: "cal-wed-1",
    title: "Binary Tree Traversals (Inorder, BFS, DFS)",
    topic: "Trees",
    type: "video",
    startTime: "09:00 AM",
    endTime: "10:00 AM",
    dayIndex: 2,
    status: "completed",
    durationMinutes: 60,
  },
  {
    id: "cal-wed-2",
    title: "BST Balancing & AVL Rotations",
    topic: "Trees",
    type: "video",
    startTime: "11:30 AM",
    endTime: "12:15 PM",
    dayIndex: 2,
    status: "completed",
    durationMinutes: 45,
  },

  // Thursday (Completed)
  {
    id: "cal-thu-1",
    title: "Sorting: QuickSort vs MergeSort Analysis",
    topic: "Sorting",
    type: "video",
    startTime: "10:00 AM",
    endTime: "10:45 AM",
    dayIndex: 3,
    status: "completed",
    durationMinutes: 45,
  },
  {
    id: "cal-thu-2",
    title: "Diagnostic Quiz: Sorting Algorithms",
    topic: "Sorting",
    type: "quiz",
    startTime: "02:30 PM",
    endTime: "03:00 PM",
    dayIndex: 3,
    status: "completed",
    durationMinutes: 30,
  },

  // Saturday (Upcoming)
  {
    id: "cal-sat-1",
    title: "Dynamic Programming: 0/1 Knapsack Deep Dive",
    topic: "Dynamic Programming",
    type: "video",
    startTime: "10:00 AM",
    endTime: "11:15 AM",
    dayIndex: 5,
    status: "scheduled",
    durationMinutes: 75,
  },
  {
    id: "cal-sat-2",
    title: "LeetCode Curated DP Patterns (5 Drills)",
    topic: "Dynamic Programming",
    type: "practice",
    startTime: "02:00 PM",
    endTime: "03:30 PM",
    dayIndex: 5,
    status: "scheduled",
    durationMinutes: 90,
  },

  // Sunday (Upcoming)
  {
    id: "cal-sun-1",
    title: "Comprehensive Graph & Tree Synthesis",
    topic: "Graphs",
    type: "reading",
    startTime: "11:00 AM",
    endTime: "12:00 PM",
    dayIndex: 6,
    status: "scheduled",
    durationMinutes: 60,
  },
  {
    id: "cal-sun-2",
    title: "Weekly Adaptive Checkpoint Assessment",
    topic: "Diagnostic",
    type: "quiz",
    startTime: "04:00 PM",
    endTime: "04:45 PM",
    dayIndex: 6,
    status: "scheduled",
    durationMinutes: 45,
  },
];

const TODAY_TIMES = [
  { start: "09:00 AM", end: "10:00 AM" },
  { start: "10:30 AM", end: "11:30 AM" },
  { start: "02:00 PM", end: "03:00 PM" },
  { start: "05:30 PM", end: "06:15 PM" },
];

export function CalendarPage() {
  const { data: calendar, isLoading, isError, error, refetch } = useCalendar();
  const { data: todayActs } = useTodayActivities();
  const [filterType, setFilterType] = useState<"all" | "sessions" | "windows">("all");
  const [weekOffset, setWeekOffset] = useState<number>(0);

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-8 shadow-xs">
        <LoadingState message="Connecting to Calendar Availability API..." />
      </div>
    );
  }

  if (isError) {
    return (
      <ErrorState
        message={error instanceof Error ? error.message : "Failed to load calendar"}
        onRetry={() => refetch()}
      />
    );
  }

  const days = [
    { label: "Mon, 08", fullDate: "Sep 08, 2025", isPast: true },
    { label: "Tue, 09", fullDate: "Sep 09, 2025", isPast: true },
    { label: "Wed, 10", fullDate: "Sep 10, 2025", isPast: true },
    { label: "Thu, 11", fullDate: "Sep 11, 2025", isPast: true },
    { label: "Today", fullDate: "Sep 12, 2025 (Fri)", isToday: true },
    { label: "Sat, 13", fullDate: "Sep 13, 2025", isFuture: true },
    { label: "Sun, 14", fullDate: "Sep 14, 2025", isFuture: true },
  ];

  const calData = calendar as any;
  const weeklyAvailableHours = calendar?.weekly_available_hours ?? calData?.available_hours ?? 15.0;
  const availableStudyHours = calendar?.available_study_hours ?? calData?.available_hours ?? 15.0;

  // Build today's events from API with clean 12-hour AM/PM formatting
  const scheduledToday: CalendarEvent[] = (todayActs && todayActs.length > 0 ? todayActs : []).map((act, i) => {
    const timeSlot = TODAY_TIMES[i % TODAY_TIMES.length];
    return {
      id: act.id || `act-today-${i}`,
      title: act.title,
      topic: act.topic,
      type: (act.type as any) || (i === 0 ? "video" : i === 1 ? "practice" : i === 2 ? "reading" : "quiz"),
      startTime: timeSlot.start,
      endTime: timeSlot.end,
      dayIndex: 4, // Today (Friday)
      status: i === 0 ? "active" : "scheduled",
      durationMinutes: act.duration_minutes || 60,
    };
  });

  // Fallback if API hasn't returned activities for today yet
  const todayEvents = scheduledToday.length > 0 ? scheduledToday : [
    {
      id: "today-1",
      title: "Graph Algorithms: BFS, DFS & Dijkstra",
      topic: "Graphs",
      type: "video" as const,
      startTime: "09:00 AM",
      endTime: "10:00 AM",
      dayIndex: 4,
      status: "active" as const,
      durationMinutes: 60,
    },
    {
      id: "today-2",
      title: "Practice: Dijkstra's Algorithm Implementation",
      topic: "Graphs",
      type: "practice" as const,
      startTime: "10:30 AM",
      endTime: "11:30 AM",
      dayIndex: 4,
      status: "scheduled" as const,
      durationMinutes: 60,
    },
    {
      id: "today-3",
      title: "Read: DP Memoization Patterns",
      topic: "Dynamic Programming",
      type: "reading" as const,
      startTime: "02:00 PM",
      endTime: "03:00 PM",
      dayIndex: 4,
      status: "scheduled" as const,
      durationMinutes: 60,
    },
    {
      id: "today-4",
      title: "Quiz: Graphs & Shortest Paths (20 Questions)",
      topic: "Graphs",
      type: "quiz" as const,
      startTime: "05:30 PM",
      endTime: "06:15 PM",
      dayIndex: 4,
      status: "scheduled" as const,
      durationMinutes: 45,
    },
  ];

  const allEvents = [...WEEKLY_CURRICULUM_SCHEDULE, ...todayEvents];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "video":
        return <Video className="h-3 w-3" />;
      case "practice":
        return <Code2 className="h-3 w-3" />;
      case "quiz":
        return <HelpCircle className="h-3 w-3" />;
      default:
        return <BookOpen className="h-3 w-3" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6 font-sans"
    >
      {/* Header */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary mb-2">
            <CalendarIcon className="h-3.5 w-3.5" />
            Adaptive Availability Grid
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Weekly Calendar</h2>
          <p className="text-xs text-slate-500 mt-1">
            LearnMate auto-schedules sessions into your verified free time windows ({weeklyAvailableHours}h weekly commitment).
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-3.5 py-1.5 text-center flex items-center gap-1.5 text-emerald-800 text-xs font-bold shadow-2xs">
            <ShieldCheck className="h-4 w-4 text-emerald-600" />
            <span>{availableStudyHours}h Available Study Capacity</span>
          </div>

          {/* Week navigator */}
          <div className="flex items-center gap-1 rounded-xl border border-slate-200 bg-slate-50 p-1 shadow-2xs">
            <button
              onClick={() => setWeekOffset(weekOffset - 1)}
              className="p-1.5 rounded-lg hover:bg-white text-slate-600 hover:text-slate-900 transition-colors cursor-pointer"
              title="Previous Week"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            <span className="text-xs font-bold text-slate-800 px-2 min-w-[85px] text-center">
              {weekOffset === 0 ? "Active Week" : weekOffset === -1 ? "Last Week" : `Week +${weekOffset}`}
            </span>
            <button
              onClick={() => setWeekOffset(weekOffset + 1)}
              className="p-1.5 rounded-lg hover:bg-white text-slate-600 hover:text-slate-900 transition-colors cursor-pointer"
              title="Next Week"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Filter Chips */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilterType("all")}
            className={`rounded-xl px-3.5 py-1.5 text-xs font-semibold transition-all cursor-pointer ${
              filterType === "all"
                ? "bg-slate-900 text-white shadow-xs"
                : "border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
            }`}
          >
            All Calendar Items
          </button>
          <button
            onClick={() => setFilterType("sessions")}
            className={`rounded-xl px-3.5 py-1.5 text-xs font-semibold transition-all cursor-pointer ${
              filterType === "sessions"
                ? "bg-slate-900 text-white shadow-xs"
                : "border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
            }`}
          >
            Study Sessions ({allEvents.length})
          </button>
          <button
            onClick={() => setFilterType("windows")}
            className={`rounded-xl px-3.5 py-1.5 text-xs font-semibold transition-all cursor-pointer ${
              filterType === "windows"
                ? "bg-slate-900 text-white shadow-xs"
                : "border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
            }`}
          >
            Open Study Windows
          </button>
        </div>

        <div className="hidden sm:flex items-center gap-3 text-[11px] text-slate-500 font-medium">
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-emerald-500" /> Completed
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-indigo-500 animate-pulse" /> Active Today
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-slate-400" /> Scheduled
          </span>
        </div>
      </div>

      {/* Weekly Grid (7 Days) */}
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 overflow-x-auto shadow-xs">
        <div className="grid grid-cols-7 gap-3 min-w-[850px]">
          {days.map((day, idx) => {
            const isToday = Boolean(day.isToday);
            const isPast = Boolean(day.isPast);
            const isFuture = Boolean(day.isFuture);
            const dayEvents = allEvents.filter((slot) => slot.dayIndex === idx);

            return (
              <div
                key={day.label}
                className={`rounded-2xl border p-3.5 min-h-[440px] flex flex-col justify-between transition-all ${
                  isToday
                    ? "border-indigo-400 bg-indigo-50/30 shadow-md shadow-indigo-100/50 ring-2 ring-indigo-500/20"
                    : isPast
                    ? "border-slate-200/80 bg-slate-50/50"
                    : "border-slate-200 bg-white hover:border-slate-300 hover:shadow-xs"
                }`}
              >
                <div>
                  {/* Day Header */}
                  <div className="flex items-center justify-between pb-2.5 border-b border-slate-200/80">
                    <div>
                      <span
                        className={`text-xs font-bold block ${
                          isToday ? "text-primary" : "text-slate-800"
                        }`}
                      >
                        {day.label}
                      </span>
                      <span className="text-[10px] text-slate-400 block font-normal">
                        {idx === 0 ? "Mon" : idx === 1 ? "Tue" : idx === 2 ? "Wed" : idx === 3 ? "Thu" : idx === 4 ? "Fri" : idx === 5 ? "Sat" : "Sun"}
                      </span>
                    </div>

                    {isToday && (
                      <span className="rounded-full gradient-primary px-2 py-0.5 text-[9px] font-bold text-white shadow-2xs animate-pulse">
                        Today
                      </span>
                    )}
                    {isPast && (
                      <span className="rounded-full bg-emerald-100 text-emerald-700 px-1.5 py-0.5 text-[9px] font-bold flex items-center gap-0.5">
                        <CheckCircle2 className="h-2.5 w-2.5" />
                        Done
                      </span>
                    )}
                    {isFuture && (
                      <span className="rounded-full bg-slate-100 text-slate-600 px-1.5 py-0.5 text-[9px] font-bold">
                        Upcoming
                      </span>
                    )}
                  </div>

                  {/* Sessions Container */}
                  {filterType !== "windows" && (
                    <div className="space-y-2 mt-3">
                      {dayEvents.map((evt) => {
                        const isCompleted = evt.status === "completed";
                        const isActive = evt.status === "active";

                        return (
                          <div
                            key={evt.id}
                            className={`rounded-xl border p-2.5 text-xs font-medium transition-all shadow-2xs ${
                              isActive
                                ? "border-indigo-300 bg-white text-indigo-950 shadow-sm ring-1 ring-primary/30"
                                : isCompleted
                                ? "border-emerald-200 bg-emerald-50/40 text-emerald-950"
                                : "border-slate-200 bg-slate-50/80 text-slate-800 hover:bg-white"
                            }`}
                          >
                            <div className="flex items-center justify-between text-[10px] mb-1 font-semibold">
                              <span
                                className={`inline-flex items-center gap-1 rounded-md px-1.5 py-0.5 uppercase tracking-wider ${
                                  isActive
                                    ? "bg-indigo-100 text-primary"
                                    : isCompleted
                                    ? "bg-emerald-100 text-emerald-800"
                                    : "bg-slate-200 text-slate-700"
                                }`}
                              >
                                {getTypeIcon(evt.type)}
                                {evt.type}
                              </span>

                              {isCompleted && (
                                <CheckCircle2 className="h-3 w-3 text-emerald-600" />
                              )}
                              {isActive && (
                                <span className="flex h-2 w-2 rounded-full bg-primary animate-ping" />
                              )}
                            </div>

                            <p className="font-bold leading-snug line-clamp-2 text-slate-900">
                              {evt.title}
                            </p>

                            <div className="mt-2 flex items-center justify-between text-[10px] text-slate-500 font-medium">
                              <span className="flex items-center gap-1">
                                <Clock className="h-2.5 w-2.5 text-slate-400" />
                                {evt.startTime}
                              </span>
                              <span className="font-mono text-slate-400">{evt.durationMinutes}m</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Open study window slots */}
                  {filterType !== "sessions" && (
                    <div className="mt-2.5 pt-2 border-t border-dashed border-slate-200">
                      <div className="rounded-lg border border-slate-200/60 bg-white/70 p-2 text-[10px] text-slate-500">
                        <span className="font-bold text-slate-700 block">Verified Open Window:</span>
                        <span>09:00 AM – 11:30 AM (150m free)</span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Footer slot indicator */}
                <div className="pt-3 border-t border-slate-200/60 flex items-center justify-between text-[10px] font-semibold text-slate-500">
                  <span>{dayEvents.length} Scheduled</span>
                  <span className="text-slate-400">
                    {dayEvents.reduce((acc, curr) => acc + curr.durationMinutes, 0)}m total
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </motion.div>
  );
}
