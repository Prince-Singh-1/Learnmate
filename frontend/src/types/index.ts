/**
 * TypeScript type definitions for LearnMate entities.
 */

export interface Student {
  id: string;
  name: string;
  email: string;
  learning_goals: string[];
  target_deadline: string;
  created_at: string;
}

export interface PerformanceRecord {
  id: string;
  student_id: string;
  topic: string;
  score: number;
  mastery_level: number;
  assessed_at: string;
}

export interface PerformanceSummary {
  overall_mastery: number;
  strongest_topic: string;
  weakest_topic: string;
  total_assessments: number;
  topic_mastery: Record<string, number>;
}

export interface PerformanceData {
  student_id: string;
  records: PerformanceRecord[];
  summary: PerformanceSummary | null;
}

export interface PlanActivity {
  id: string;
  topic: string;
  resource_title: string;
  resource_type: string;
  scheduled_start: string;
  scheduled_end: string;
  status: "pending" | "completed" | "missed" | "deferred";
  priority: number;
}

export interface LearningPlan {
  id: string;
  student_id: string;
  version: number;
  status: string;
  created_at: string;
  valid_until: string;
  activities: PlanActivity[];
}

export interface LearningResource {
  id: string;
  title: string;
  type: string;
  url: string;
  topic: string;
  difficulty: string;
  duration_minutes: number;
}

export interface CalendarSlot {
  id: string;
  student_id: string;
  start_time: string;
  end_time: string;
  is_available: boolean;
}
