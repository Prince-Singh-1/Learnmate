/**
 * LearnMate React Query Hooks
 *
 * Provides reactive data-fetching and cache invalidation across all 9 connected services:
 * - Dashboard → student API
 * - Goals → goals API
 * - Performance → performance API
 * - Knowledge gaps → gaps API
 * - Resources → resources API
 * - Calendar → calendar API
 * - Activities → activities API
 * - Learning Plan → plan API
 * - Agent → agent API
 *
 * Automatically updates UI upon:
 * - completing an activity
 * - missing an activity
 * - submitting an assessment
 * - running the agent
 * - generating a new plan
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export interface StudentData {
  id: string;
  name: string;
  email: string;
  role: string;
  avatar: string;
  overall_progress: number;
  study_streak: number;
  topics_completed: number;
  time_spent_hours: number;
  weekly_goal_hours: number;
  current_goal_id: string;
  learning_velocity: number;
  level: string;
  preferred_study_times: string[];
  target_deadline?: string;
  degree?: string;
}

export interface GoalData {
  id: string;
  student_id: string;
  title: string;
  description: string;
  target_date: string;
  target_proficiency: number;
  current_progress: number;
  priority: string;
  status: string;
  days_remaining: number;
  topics: string[];
}

export interface PerformanceData {
  overall_mastery: number;
  strongest_topic: string;
  weakest_topic: string;
  topic_mastery: Array<{
    topic: string;
    mastery_score: number;
    trend: string;
    status: string;
    confidence?: number;
    target_mastery?: number;
  }>;
  points: Array<{
    day: string;
    points: number;
    hours: number;
    efficiency: number;
  }>;
}

export interface KnowledgeGapData {
  id: string;
  topic: string;
  gap_score: number;
  severity: "High" | "Medium" | "Low";
  priority: string;
  estimated_hours: number;
  estimated_learning_hours?: number;
  reason: string;
  recommended_action: string;
  prerequisites?: string[];
}

export interface ResourceData {
  id: string;
  title: string;
  type: string;
  source: string;
  detail: string;
  duration_minutes: number;
  difficulty: string;
  quality_score: number;
  match_score: number;
  match_label: string;
  color: string;
  url: string;
  topic: string;
}

export interface CalendarSlotData {
  id: string;
  day: string;
  start_time: string;
  end_time: string;
  duration_minutes: number;
  is_available: boolean;
  event_title?: string;
  color?: string;
}

export interface CalendarData {
  student_id: string;
  weekly_available_hours: number;
  available_study_hours: number;
  slots: CalendarSlotData[];
  upcoming_commitments: Array<{
    id: string;
    title: string;
    time: string;
    date: string;
    duration: string;
    color: string;
  }>;
}

export interface ActivityData {
  id: string;
  topic: string;
  title: string;
  type: string;
  duration_minutes: number;
  scheduled_start: string;
  scheduled_end?: string;
  status: "pending" | "completed" | "missed" | "in_progress";
  completed?: boolean;
  missed?: boolean;
  priority?: number;
}

export interface LearningPlanData {
  id: string;
  version: number;
  student_id: string;
  title: string;
  goal?: string;
  target_deadline: string;
  remaining_days: number;
  required_study_hours: number;
  scheduled_study_hours: number;
  feasibility_ratio: number;
  deadline_guaranteed: boolean;
  status: string;
  activities: ActivityData[];
}

export interface AgentActionItem {
  time: string;
  type: "check" | "refresh" | "sparkles" | string;
  title: string;
  description: string;
  status: "completed" | "in_progress" | "pending";
}

export interface AgentActivityFeed {
  status: string;
  last_run: string;
  actions: AgentActionItem[];
}

export interface PlanComparisonItem {
  id: string;
  title: string;
  topic: string;
  type: string;
  duration_minutes: number;
  day: string;
  time: string;
  diff_note?: string;
  change_badge: string;
  change_type: "shortened" | "moved" | "added" | "preserved" | "removed";
}

export interface ReplanComparisonData {
  status: string;
  headline: string;
  reason: string;
  goal_still_achievable: boolean;
  target_deadline: string;
  explanations: string[];
  stats: {
    moved_count: number;
    shortened_count: number;
    added_count: number;
    preserved_count: number;
  };
  old_plan: {
    version: number;
    total_hours: number;
    activities: PlanComparisonItem[];
  };
  new_plan: {
    version: number;
    total_hours: number;
    activities: PlanComparisonItem[];
  };
}

// ─── Query Keys ────────────────────────────────────────────────────────────

export const queryKeys = {
  student: ["student"] as const,
  goals: ["goals"] as const,
  performance: ["performance"] as const,
  gaps: (severity?: string) => ["gaps", severity] as const,
  resources: (topic?: string) => ["resources", topic] as const,
  calendar: ["calendar"] as const,
  activitiesToday: ["activities", "today"] as const,
  activitiesRecent: ["activities", "recent"] as const,
  plan: ["plan"] as const,
  agentStatus: ["agent", "status"] as const,
  agentActivity: ["agent", "activity"] as const,
  replanComparison: ["replan", "comparison"] as const,
  verification: ["verification"] as const,
};

// ─── Query Hooks ───────────────────────────────────────────────────────────

export function useStudent(id?: string) {
  return useQuery({
    queryKey: queryKeys.student,
    queryFn: () => api.getStudent<StudentData>(id),
  });
}

export function useGoals(studentId: string = "stu-001") {
  return useQuery({
    queryKey: queryKeys.goals,
    queryFn: () => api.getGoals<GoalData[]>(studentId),
  });
}

export function usePerformance(studentId: string = "stu-001") {
  return useQuery({
    queryKey: queryKeys.performance,
    queryFn: () => api.getPerformance<PerformanceData>(studentId),
  });
}

export function useKnowledgeGaps(severity?: string) {
  return useQuery({
    queryKey: queryKeys.gaps(severity),
    queryFn: () => api.getGaps<KnowledgeGapData[]>(severity),
  });
}

export function useResources(topic?: string) {
  return useQuery({
    queryKey: queryKeys.resources(topic),
    queryFn: () => api.getResources<ResourceData[]>(topic),
  });
}

export function useCalendar(studentId: string = "stu-001") {
  return useQuery({
    queryKey: queryKeys.calendar,
    queryFn: () => api.getCalendar<CalendarData>(studentId),
  });
}

export function useTodayActivities() {
  return useQuery({
    queryKey: queryKeys.activitiesToday,
    queryFn: () => api.getTodayActivities<ActivityData[]>(),
  });
}

export function useRecentActivities() {
  return useQuery({
    queryKey: queryKeys.activitiesRecent,
    queryFn: () => api.getRecentActivities<Array<Record<string, unknown>>>(),
  });
}

export function useLearningPlan(studentId: string = "stu-001") {
  return useQuery({
    queryKey: queryKeys.plan,
    queryFn: () => api.getPlan<LearningPlanData>(studentId),
  });
}

export function useAgentStatus() {
  return useQuery({
    queryKey: queryKeys.agentStatus,
    queryFn: () => api.getAgentStatus<Record<string, unknown>>(),
  });
}

export function useAgentActivity() {
  return useQuery({
    queryKey: queryKeys.agentActivity,
    queryFn: () => api.getAgentActivity<AgentActivityFeed>(),
  });
}

export function useReplanComparison() {
  return useQuery({
    queryKey: queryKeys.replanComparison,
    queryFn: () => api.getReplanComparison<ReplanComparisonData>(),
  });
}

// ─── Mutation Hooks with Targeted Cache Invalidation ───────────────────────

export function useCompleteActivity() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ activityId, notes }: { activityId: string; notes?: string }) =>
      api.completeActivity(activityId, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesToday });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesRecent });
      queryClient.invalidateQueries({ queryKey: queryKeys.student });
      queryClient.invalidateQueries({ queryKey: queryKeys.plan });
      queryClient.invalidateQueries({ queryKey: queryKeys.performance });
    },
  });
}

export function useMissActivity() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ activityId, reason }: { activityId: string; reason?: string }) =>
      api.missActivity(activityId, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesToday });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesRecent });
      queryClient.invalidateQueries({ queryKey: queryKeys.student });
      queryClient.invalidateQueries({ queryKey: queryKeys.plan });
      queryClient.invalidateQueries({ queryKey: queryKeys.performance });
    },
  });
}

export function useSubmitAssessment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { topic: string; score: number; max_score?: number }) =>
      api.submitAssessment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.performance });
      queryClient.invalidateQueries({ queryKey: queryKeys.gaps() });
      queryClient.invalidateQueries({ queryKey: queryKeys.student });
      queryClient.invalidateQueries({ queryKey: queryKeys.resources() });
      queryClient.invalidateQueries({ queryKey: queryKeys.plan });
    },
  });
}

export function useRunAgent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload?: { student_id?: string; force_replan?: boolean }) =>
      api.runAgent(payload),
    onSuccess: () => {
      // Invalidate all reactive telemetry queries across the app
      queryClient.invalidateQueries({ queryKey: queryKeys.student });
      queryClient.invalidateQueries({ queryKey: queryKeys.goals });
      queryClient.invalidateQueries({ queryKey: queryKeys.performance });
      queryClient.invalidateQueries({ queryKey: queryKeys.gaps() });
      queryClient.invalidateQueries({ queryKey: queryKeys.resources() });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesToday });
      queryClient.invalidateQueries({ queryKey: queryKeys.plan });
      queryClient.invalidateQueries({ queryKey: queryKeys.agentStatus });
      queryClient.invalidateQueries({ queryKey: queryKeys.agentActivity });
      queryClient.invalidateQueries({ queryKey: queryKeys.replanComparison });
    },
  });
}

export function useGeneratePlan() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (studentId?: string) => api.generatePlan(studentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.plan });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesToday });
      queryClient.invalidateQueries({ queryKey: queryKeys.replanComparison });
    },
  });
}

export function useTriggerReplan() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload?: { student_id?: string; reason?: string }) =>
      api.triggerReplan(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.plan });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesToday });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesRecent });
      queryClient.invalidateQueries({ queryKey: queryKeys.agentActivity });
      queryClient.invalidateQueries({ queryKey: queryKeys.replanComparison });
    },
  });
}

export interface SimulationResultData {
  success: boolean;
  scenario: string;
  title: string;
  summary: string;
  event_detected: Record<string, any>;
  state_updated: Record<string, any>;
  performance_reassessed: Record<string, any>;
  plan_regenerated: Record<string, any>;
  plan_verified: Record<string, any>;
  new_plan_activated: Record<string, any>;
  process_steps: Array<{
    step: number;
    name: string;
    label: string;
    description: string;
    status: string;
    timestamp: string;
    details?: Record<string, any>;
  }>;
  agent_reasoning: string;
  old_plan_summary: Record<string, any>;
  new_plan_summary: Record<string, any>;
}

export function useSimulateEvent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: { scenario: string; topic?: string; custom_note?: string }) =>
      api.simulateEvent<SimulationResultData>(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.student });
      queryClient.invalidateQueries({ queryKey: queryKeys.goals });
      queryClient.invalidateQueries({ queryKey: queryKeys.performance });
      queryClient.invalidateQueries({ queryKey: queryKeys.gaps() });
      queryClient.invalidateQueries({ queryKey: queryKeys.resources() });
      queryClient.invalidateQueries({ queryKey: queryKeys.calendar });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesToday });
      queryClient.invalidateQueries({ queryKey: queryKeys.activitiesRecent });
      queryClient.invalidateQueries({ queryKey: queryKeys.plan });
      queryClient.invalidateQueries({ queryKey: queryKeys.agentStatus });
      queryClient.invalidateQueries({ queryKey: queryKeys.agentActivity });
      queryClient.invalidateQueries({ queryKey: queryKeys.replanComparison });
      queryClient.invalidateQueries({ queryKey: queryKeys.verification });
    },
  });
}

export interface AdaptiveQuestionData {
  id: string;
  topic: string;
  difficulty: "Easy" | "Medium" | "Hard";
  question_text: string;
  options: Array<{ id: string; text: string }>;
  correct_option_id: string;
  explanation: string;
  target_concept: string;
  time_limit_seconds: number;
}

export interface AdaptiveAttemptResultData {
  attempt_id: string;
  question_id: string;
  topic: string;
  difficulty: string;
  selected_option_id: string;
  correct_option_id: string;
  is_correct: boolean;
  time_spent_seconds: number;
  attempt_number: number;
  adaptation: {
    previous_difficulty: string;
    was_correct: boolean;
    next_difficulty: "Easy" | "Medium" | "Hard";
    adaptation_reason: string;
    explanation?: string;
  };
  next_question?: AdaptiveQuestionData;
  topic_mastery_updated: number;
  knowledge_gap_severity: string;
  replan_required: boolean;
  replan_reason?: string;
  agent_run_id?: string;
  message: string;
}

export function useAdaptiveQuestion(topic: string = "Graphs", difficulty?: string) {
  return useQuery({
    queryKey: ["practice", "adaptive", "question", topic, difficulty],
    queryFn: () => api.getAdaptiveQuestion<AdaptiveQuestionData>(topic, difficulty),
  });
}

export function useSubmitAdaptiveAttempt() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: {
      question_id: string;
      topic: string;
      difficulty: string;
      selected_option_id: string;
      time_spent_seconds: number;
      attempt_number?: number;
      student_id?: string;
    }) => api.submitAdaptiveAttempt<AdaptiveAttemptResultData>(payload),
    onSuccess: (data) => {
      // Invalidate performance, gaps, and learning plan if replan was triggered
      queryClient.invalidateQueries({ queryKey: queryKeys.performance });
      queryClient.invalidateQueries({ queryKey: queryKeys.gaps() });
      queryClient.invalidateQueries({ queryKey: queryKeys.student });
      if (data.replan_required) {
        queryClient.invalidateQueries({ queryKey: queryKeys.plan });
        queryClient.invalidateQueries({ queryKey: queryKeys.activitiesToday });
        queryClient.invalidateQueries({ queryKey: queryKeys.activitiesRecent });
        queryClient.invalidateQueries({ queryKey: queryKeys.agentActivity });
        queryClient.invalidateQueries({ queryKey: queryKeys.replanComparison });
      }
    },
  });
}


