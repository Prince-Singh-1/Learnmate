/**
 * LearnMate — Centralized Mock Data
 *
 * All synthetic data used across the dashboard.
 * Components import from here — never hardcode data inside components.
 */

// ─── Student Profile ───────────────────────────────────────────
export const studentProfile = {
  id: "stu-001",
  name: "Prince",
  fullName: "Prince Singh",
  email: "prince.singh@university.edu",
  program: "B.Tech (CSE)",
  avatar: "/prince-avatar.jpg",
  joinedDate: "2025-06-15",
};

// ─── Learning Goal ─────────────────────────────────────────────
export const learningGoal = {
  id: "goal-001",
  title: "Master Data Structures & Algorithms",
  description:
    "Become interview ready with strong problem solving skills.",
  progress: 68,
  targetDate: "2025-11-30",
  daysRemaining: 79,
  priority: "High" as const,
  estimatedHours: 120,
  hoursCompleted: 82,
  totalTopics: 12,
  completedTopics: 8,
  remainingTopics: [
    "Dynamic Programming",
    "Graphs",
    "Trees (Advanced)",
    "Hashing (Advanced)",
  ],
};

// ─── Stats ─────────────────────────────────────────────────────
export const stats = {
  overallProgress: 68,
  studyStreak: 12,
  topicsCompleted: 8,
  timeSpent: "24 hrs",
  motivationalQuote: "Progress, not perfection.",
};

// ─── Knowledge Gaps ────────────────────────────────────────────
export type GapSeverity = "High" | "Medium" | "Low";

export interface KnowledgeGap {
  id: string;
  topic: string;
  severity: GapSeverity;
  mastery: number;
  description: string;
}

export const knowledgeGaps: KnowledgeGap[] = [
  {
    id: "gap-1",
    topic: "Dynamic Programming",
    severity: "High",
    mastery: 25,
    description: "Weak in memoization and tabulation patterns",
  },
  {
    id: "gap-2",
    topic: "Graphs",
    severity: "High",
    mastery: 30,
    description: "Need practice with shortest path and traversals",
  },
  {
    id: "gap-3",
    topic: "Trees",
    severity: "Medium",
    mastery: 45,
    description: "Balanced trees and segment trees need work",
  },
  {
    id: "gap-4",
    topic: "Hashing",
    severity: "Medium",
    mastery: 50,
    description: "Collision handling and advanced hash maps",
  },
  {
    id: "gap-5",
    topic: "Sorting",
    severity: "Low",
    mastery: 80,
    description: "Quick review of advanced sorting algorithms",
  },
];

// ─── Topic Mastery ─────────────────────────────────────────────
export interface TopicMasteryItem {
  id: string;
  topic: string;
  mastery: number;
  color: string;
  icon: string;
}

export const topicMastery: TopicMasteryItem[] = [
  { id: "tm-1", topic: "Arrays", mastery: 85, color: "#6366f1", icon: "📊" },
  { id: "tm-2", topic: "Linked Lists", mastery: 70, color: "#8b5cf6", icon: "🔗" },
  { id: "tm-3", topic: "Trees", mastery: 45, color: "#a78bfa", icon: "🌳" },
  { id: "tm-4", topic: "Graphs", mastery: 30, color: "#c084fc", icon: "📈" },
  {
    id: "tm-5",
    topic: "Dynamic Programming",
    mastery: 25,
    color: "#e879f9",
    icon: "🧩",
  },
  { id: "tm-6", topic: "Sorting", mastery: 80, color: "#22d3ee", icon: "📶" },
];

// ─── Performance Data (Chart) ──────────────────────────────────
export interface PerformancePoint {
  week: string;
  score: number;
  target: number;
}

export const performanceData: PerformancePoint[] = [
  { week: "Week 1", score: 45, target: 60 },
  { week: "Week 2", score: 55, target: 65 },
  { week: "Week 3", score: 62, target: 70 },
  { week: "Week 4", score: 68, target: 75 },
];

// ─── Today's Plan ──────────────────────────────────────────────
export interface ScheduleItem {
  id: string;
  time: string;
  endTime: string;
  title: string;
  type: "video" | "practice" | "reading" | "quiz";
  completed: boolean;
  current?: boolean;
}

export const todaysSchedule: ScheduleItem[] = [
  {
    id: "sched-1",
    time: "9:00",
    endTime: "10:00 AM",
    title: "Graph Algorithms (Video)",
    type: "video",
    completed: false,
    current: true,
  },
  {
    id: "sched-2",
    time: "10:30",
    endTime: "11:30 AM",
    title: "Practice: Dijkstra's Algorithm",
    type: "practice",
    completed: false,
  },
  {
    id: "sched-3",
    time: "2:00",
    endTime: "3:00 PM",
    title: "Read: DP Notes",
    type: "reading",
    completed: false,
  },
  {
    id: "sched-4",
    time: "6:00",
    endTime: "6:30 PM",
    title: "Quiz: Graphs (20 Questions)",
    type: "quiz",
    completed: false,
  },
];

// ─── Recommended Resources ─────────────────────────────────────
export interface Resource {
  id: string;
  title: string;
  type: "video" | "pdf" | "practice" | "tool";
  source: string;
  detail: string;
  matchScore: number;
  matchLabel: string;
  duration?: string;
  color: string;
}

export const recommendedResources: Resource[] = [
  {
    id: "res-1",
    title: "Graph Algorithms Explained",
    type: "video",
    source: "Video • freeCodeCamp",
    detail: "30:15",
    matchScore: 95,
    matchLabel: "High Match",
    color: "#6366f1",
  },
  {
    id: "res-2",
    title: "DP Cheat Sheet",
    type: "pdf",
    source: "PDF • 12 pages",
    detail: "",
    matchScore: 90,
    matchLabel: "Very Useful",
    color: "#ef4444",
  },
  {
    id: "res-3",
    title: "Practice Problems: DP",
    type: "practice",
    source: "Question Bank • 50 problems",
    detail: "",
    matchScore: 88,
    matchLabel: "Recommended",
    color: "#10b981",
  },
  {
    id: "res-4",
    title: "Interactive Visualizer",
    type: "tool",
    source: "Graphs & Trees",
    detail: "Web Tool",
    matchScore: 92,
    matchLabel: "Try Now",
    color: "#3b82f6",
  },
];

// ─── Recent Activity ───────────────────────────────────────────
export type ActivityStatus =
  | "completed"
  | "missed"
  | "scored"
  | "rescheduled";

export interface ActivityItem {
  id: string;
  status: ActivityStatus;
  description: string;
  timestamp: string;
}

export const recentActivity: ActivityItem[] = [
  {
    id: "act-1",
    status: "completed",
    description: "Completed: Arrays Practice Set",
    timestamp: "Today, 10:15 AM",
  },
  {
    id: "act-2",
    status: "missed",
    description: "Missed: Binary Trees Video",
    timestamp: "Yesterday, 6:00 PM",
  },
  {
    id: "act-3",
    status: "scored",
    description: "Scored 80% in Sorting Quiz",
    timestamp: "10 Sep 2025",
  },
  {
    id: "act-4",
    status: "completed",
    description: "Completed: Hashing Notes",
    timestamp: "9 Sep 2025",
  },
  {
    id: "act-5",
    status: "rescheduled",
    description: "Rescheduled: DP Practice",
    timestamp: "9 Sep 2025",
  },
];

// ─── Agent Status ──────────────────────────────────────────────
export interface AgentStep {
  id: string;
  label: string;
  completed: boolean;
  timestamp?: string;
}

export const agentSteps: AgentStep[] = [
  {
    id: "agent-1",
    label: "Performance analyzed",
    completed: true,
    timestamp: "2 min ago",
  },
  {
    id: "agent-2",
    label: "Knowledge gaps checked",
    completed: true,
    timestamp: "2 min ago",
  },
  {
    id: "agent-3",
    label: "Resources selected",
    completed: true,
    timestamp: "1 min ago",
  },
  {
    id: "agent-4",
    label: "Calendar checked",
    completed: true,
    timestamp: "1 min ago",
  },
  {
    id: "agent-5",
    label: "Plan verified",
    completed: true,
    timestamp: "Just now",
  },
];

// ─── Learning Journey Steps ────────────────────────────────────
export interface JourneyStep {
  id: string;
  step: number;
  title: string;
  subtitle: string;
  icon: string;
  color: string;
  completed: boolean;
  active?: boolean;
}

export const journeySteps: JourneyStep[] = [
  {
    id: "j-1",
    step: 1,
    title: "Analyze",
    subtitle: "Your Performance",
    icon: "📊",
    color: "#ef4444",
    completed: true,
  },
  {
    id: "j-2",
    step: 2,
    title: "Identify",
    subtitle: "Knowledge Gaps",
    icon: "🔍",
    color: "#f59e0b",
    completed: true,
  },
  {
    id: "j-3",
    step: 3,
    title: "Select",
    subtitle: "Best Resources",
    icon: "📚",
    color: "#ef4444",
    completed: true,
  },
  {
    id: "j-4",
    step: 4,
    title: "Create",
    subtitle: "Smart Plan",
    icon: "📝",
    color: "#8b5cf6",
    completed: true,
  },
  {
    id: "j-5",
    step: 5,
    title: "Learn",
    subtitle: "& Track Progress",
    icon: "🎯",
    color: "#10b981",
    completed: false,
    active: true,
  },
  {
    id: "j-6",
    step: 6,
    title: "Adapt",
    subtitle: "Automatically",
    icon: "🔄",
    color: "#3b82f6",
    completed: false,
  },
];

// ─── AI Assistant Actions ──────────────────────────────────────
export interface AIAction {
  id: string;
  label: string;
  icon: string;
}

export const aiActions: AIAction[] = [
  { id: "ai-1", label: "Explain a concept", icon: "💡" },
  { id: "ai-2", label: "Give practice questions", icon: "📝" },
  { id: "ai-3", label: "Suggest resources", icon: "📚" },
  { id: "ai-4", label: "Adjust my plan", icon: "📅" },
  { id: "ai-5", label: "Answer doubts", icon: "❓" },
];

// ─── Goal Forecast ─────────────────────────────────────────────
export const goalForecast = {
  onTrack: true,
  message: "You're on the right path!",
  badges: ["Consistent", "Focused", "Improving"],
  quote:
    '"A better you is a brighter tomorrow."',
};

// ─── Sidebar Navigation ───────────────────────────────────────
export interface NavItem {
  id: string;
  label: string;
  iconName: string;
  badge?: number;
}

export const sidebarNavItems: NavItem[] = [
  { id: "dashboard", label: "Dashboard", iconName: "LayoutDashboard" },
  { id: "goals", label: "My Goals", iconName: "Target" },
  { id: "plan", label: "Learning Plan", iconName: "CalendarDays" },
  { id: "resources", label: "Resources", iconName: "BookOpen" },
  { id: "practice", label: "Practice & Tests", iconName: "FlaskConical" },
  { id: "progress", label: "Progress", iconName: "BarChart3" },
  { id: "calendar", label: "Calendar", iconName: "Calendar" },
  { id: "ai-tutor", label: "AI Tutor", iconName: "Bot" },
  { id: "achievements", label: "Achievements", iconName: "Trophy" },
  { id: "simulation", label: "Demo Simulation", iconName: "Sparkles" },
  { id: "settings", label: "Settings", iconName: "Settings" },
];


