/**
 * DashboardPage — Main Autonomous Learning Planner Dashboard.
 * Accurately matches the layout of the LearnMate reference image:
 * Left 2/3: Welcome Hero -> Stats Row -> (Goal, Performance, Mastery) -> (Recommended, Recent Activity)
 * Right 1/3: Today's Schedule -> AI Assistant -> Motivation & Goal Forecast
 * Bottom: Full-width Autonomous Learning Journey & Platform Footer.
 */

import { useState } from "react";
import {
  WelcomeHero,
  TodaySchedule,
  StatsRow,
  GoalCard,
  PerformanceChartCard,
  TopicMasteryCard,
  RecommendedResources,
  RecentActivityCard,
  AiAssistantCard,
  MotivationCard,
  LearningJourney,
  Footer,
  AutonomousReplanModal,
  AutonomousAgentPanel,
  AiChatModal,
} from "@/components/dashboard";
import { VideoPlayerModal, type VideoResourceData } from "@/components/ui/VideoPlayerModal";
import type { ActivityData } from "@/hooks/useLearnMate";

interface DashboardPageProps {
  onNavigate?: (page: string) => void;
}

export function DashboardPage({ onNavigate }: DashboardPageProps) {
  const [replanModalOpen, setReplanModalOpen] = useState(false);
  const [replanReason, setReplanReason] = useState<string>(
    "Missed Study Session: Binary Trees Video"
  );
  const [aiChatOpen, setAiChatOpen] = useState(false);
  const [aiInitialPrompt, setAiInitialPrompt] = useState("");
  const [activeVideo, setActiveVideo] = useState<VideoResourceData | null>(null);

  const triggerReplan = (reason: string) => {
    setReplanReason(reason);
    setReplanModalOpen(true);
  };

  const openAiWithPrompt = (prompt: string) => {
    setAiInitialPrompt(prompt);
    setAiChatOpen(true);
  };

  const handleStudyNow = (item: ActivityData) => {
    setActiveVideo({
      id: item.id,
      title: item.title,
      topic: item.topic,
      duration_minutes: item.duration_minutes,
      source: "Scheduled Video Lecture",
    });
  };

  return (
    <div className="space-y-6">
      {/* ─── Main Two-Column Structure (Left 8 cols, Right 4 cols) ────── */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 items-start">
        {/* ─── Left Column (8 cols on XL): Hero, Stats, Analytics, Resources */}
        <div className="xl:col-span-8 space-y-6">
          {/* 1. Welcome Hero Banner */}
          <WelcomeHero
            onContinueLearning={() =>
              handleStudyNow({
                id: "act-hero",
                title: "Graph Algorithms: BFS, DFS & Dijkstra Explained",
                topic: "Graphs",
                duration_minutes: 45,
                scheduled_start: "10:00 AM",
                status: "pending",
                completed: false,
                type: "video",
              })
            }
            onViewPlan={() => onNavigate?.("plan")}
            onOpenSimulation={() => onNavigate?.("simulation")}
          />

          {/* 2. Stats Metric Bar */}
          <StatsRow />

          {/* 3. Middle Row: Goal + Performance + Topic Mastery (3 cards) */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <GoalCard onEdit={() => onNavigate?.("goals")} />
            <PerformanceChartCard />
            <TopicMasteryCard onViewDetails={() => onNavigate?.("progress")} />
          </div>

          {/* 4. Lower Row: Recommended Resources (8 cols) + Recent Activity (4 cols) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
            <div className="lg:col-span-8">
              <RecommendedResources
                onViewAll={() => onNavigate?.("resources")}
                onOpenResource={() =>
                  openAiWithPrompt("Tell me more about this recommended resource")
                }
              />
            </div>
            <div className="lg:col-span-4">
              <RecentActivityCard
                onViewAll={() => onNavigate?.("progress")}
                onMissedActivityClick={() =>
                  triggerReplan("Missed Session: Binary Trees Video (Rescheduling...)")
                }
              />
            </div>
          </div>
        </div>

        {/* ─── Right Column (4 cols on XL): Schedule -> AI Assistant -> Motivation */}
        <div className="xl:col-span-4 space-y-6">
          {/* Today's Schedule */}
          <TodaySchedule
            onViewCalendar={() => onNavigate?.("calendar")}
            onStudyNow={handleStudyNow}
          />

          {/* AI Learning Assistant */}
          <AiAssistantCard
            onOpenFullChat={() => setAiChatOpen(true)}
            onActionSelect={(prompt) => openAiWithPrompt(prompt)}
          />

          {/* Motivation & Goal Forecast */}
          <MotivationCard />
        </div>
      </div>

      {/* ─── Autonomous Agent Activity & Plan Change Diff Panel ───────── */}
      <AutonomousAgentPanel />

      {/* ─── Bottom Full-Width Section: Autonomous Learning Journey ──── */}
      <LearningJourney
        onStepClick={(stepIndex) =>
          triggerReplan(`Inspecting Stage ${stepIndex + 1} of Autonomous Pipeline`)
        }
      />

      {/* ─── Platform Footer ────────────────────────────────────────── */}
      <Footer />

      {/* ─── Interactive Modals ─────────────────────────────────────── */}
      <AutonomousReplanModal
        isOpen={replanModalOpen}
        onClose={() => setReplanModalOpen(false)}
        triggerReason={replanReason}
      />

      <AiChatModal
        isOpen={aiChatOpen}
        onClose={() => setAiChatOpen(false)}
        initialPrompt={aiInitialPrompt}
      />

      <VideoPlayerModal
        isOpen={Boolean(activeVideo)}
        resource={activeVideo}
        onClose={() => setActiveVideo(null)}
      />
    </div>
  );
}
