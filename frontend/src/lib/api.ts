/**
 * API client for communicating with the LearnMate backend.
 *
 * Supports all 12 API groups exposed by the FastAPI server:
 * - /api/student
 * - /api/goals
 * - /api/performance
 * - /api/gaps
 * - /api/resources
 * - /api/calendar
 * - /api/activities
 * - /api/assessments
 * - /api/plan
 * - /api/agent
 * - /api/replan
 * - /api/verification
 */

const API_HOST = import.meta.env.VITE_API_URL ? String(import.meta.env.VITE_API_URL).replace(/\/+$/, "") : "";
const BASE_URL = `${API_HOST}/api`;

let authToken: string | null = typeof window !== "undefined" ? (localStorage.getItem("learnmate_token") || sessionStorage.getItem("learnmate_token")) : null;

export function setAuthToken(token: string | null, remember: boolean = true) {
  authToken = token;
  if (typeof window !== "undefined") {
    if (token) {
      if (remember) {
        localStorage.setItem("learnmate_token", token);
      } else {
        sessionStorage.setItem("learnmate_token", token);
      }
    } else {
      localStorage.removeItem("learnmate_token");
      sessionStorage.removeItem("learnmate_token");
    }
  }
}

export function getAuthToken(): string | null {
  return authToken;
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options?.headers as Record<string, string> || {}),
  };

  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    credentials: "include",
    headers,
    ...options,
  });

  if (!response.ok) {
    let errorDetail = `API Error: ${response.status} ${response.statusText}`;
    try {
      const errJson = await response.json();
      if (errJson?.detail) {
        if (typeof errJson.detail === "string") {
          errorDetail = errJson.detail;
        } else if (Array.isArray(errJson.detail)) {
          errorDetail = errJson.detail.map((e: any) => e.msg || e.message || JSON.stringify(e)).join(", ");
        }
      }
    } catch {
      // Fall back to default error text
    }
    const error = new Error(errorDetail);
    (error as any).status = response.status;
    throw error;
  }

  return response.json();
}

export const api = {
  // Health
  health: () => request<{ status: string; service: string; version: string }>("/health"),

  // 1. Student
  getStudent: <T = Record<string, unknown>>(id?: string) =>
    request<T>(id ? `/student/${id}` : "/student"),
  getStudents: <T = Array<Record<string, unknown>>>() => request<T>("/students"),

  // 2. Goals
  getGoals: async <T = Array<Record<string, unknown>>>(studentId: string = "stu-001"): Promise<T> => {
    const res = await request<any>(`/goals?student_id=${studentId}`);
    const data = Array.isArray(res) ? res : (res?.goals || []);
    return data as T;
  },

  // 3. Performance
  getPerformance: <T = Record<string, unknown>>(studentId: string = "stu-001") =>
    request<T>(`/performance?student_id=${studentId}`),
  getPerformanceTrends: <T = Record<string, string>>(studentId: string = "stu-001") =>
    request<T>(`/performance/trends?student_id=${studentId}`),

  // 4. Knowledge Gaps
  getGaps: async <T = Array<Record<string, unknown>>>(severity?: string): Promise<T> => {
    const url = severity ? `/gaps?severity=${encodeURIComponent(severity)}` : "/gaps";
    const res = await request<any>(url);
    const data = Array.isArray(res) ? res : (res?.gaps || []);
    return data as T;
  },

  // 5. Recommended Resources
  getResources: async <T = Array<Record<string, unknown>>>(topic?: string): Promise<T> => {
    const url = topic ? `/resources?topic=${encodeURIComponent(topic)}` : "/resources";
    const res = await request<any>(url);
    const data = Array.isArray(res) ? res : (res?.resources || []);
    return data as T;
  },

  // 6. Calendar Availability
  getCalendar: async <T = Record<string, unknown>>(studentId: string = "stu-001"): Promise<T> => {
    const res = await request<any>(`/calendar?student_id=${studentId}`);
    return res as T;
  },
  getCalendarSlots: async <T = Array<Record<string, unknown>>>(): Promise<T> => {
    const res = await request<any>("/calendar");
    const data = Array.isArray(res) ? res : (res?.slots || []);
    return data as T;
  },

  // 7. Today's Activities & Actions
  getTodayActivities: async <T = Array<Record<string, unknown>>>(): Promise<T> => {
    const res = await request<any>("/activities/today");
    const data = Array.isArray(res) ? res : (res?.activities || []);
    return data as T;
  },
  getRecentActivities: async <T = Array<Record<string, unknown>>>(): Promise<T> => {
    try {
      const res = await request<any>("/activities/recent");
      const data = Array.isArray(res) ? res : (res?.activities || []);
      return data as T;
    } catch {
      return [] as unknown as T;
    }
  },
  completeActivity: <T = Record<string, unknown>>(activityId: string, notes?: string) =>
    request<T>(`/activities/${activityId}/complete`, {
      method: "POST",
      body: JSON.stringify({ activity_id: activityId, notes }),
    }),
  missActivity: <T = Record<string, unknown>>(activityId: string, reason?: string) =>
    request<T>(`/activities/${activityId}/missed`, {
      method: "POST",
      body: JSON.stringify({ activity_id: activityId, reason }),
    }),

  // 8. Assessments
  getAssessments: async <T = Array<Record<string, unknown>>>(): Promise<T> => {
    const res = await request<any>("/assessments");
    const data = Array.isArray(res) ? res : (res?.assessments || []);
    return data as T;
  },
  submitAssessment: <T = Record<string, unknown>>(data: { topic: string; score: number; max_score?: number }) =>
    request<T>("/assessments", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  // 9. Learning Plan
  getPlan: <T = Record<string, unknown>>(studentId: string = "stu-001") =>
    request<T>(`/plan?student_id=${studentId}`),
  generatePlan: <T = Record<string, unknown>>(studentId: string = "stu-001") =>
    request<T>(`/plan/generate?student_id=${studentId}`, {
      method: "POST",
    }),

  // 10. Autonomous Agent
  runAgent: <T = Record<string, unknown>>(payload?: { student_id?: string; force_replan?: boolean }) =>
    request<T>("/agent/run", {
      method: "POST",
      body: JSON.stringify(payload || {}),
    }),
  getAgentStatus: <T = Record<string, unknown>>() =>
    request<T>("/agent/status"),
  getAgentActivity: <T = Record<string, unknown>>() =>
    request<T>("/agent/activity"),

  // 11. Autonomous Replan
  triggerReplan: <T = Record<string, unknown>>(payload?: { student_id?: string; reason?: string }) =>
    request<T>("/replan", {
      method: "POST",
      body: JSON.stringify(payload || {}),
    }),
  getReplanStatus: <T = Record<string, unknown>>() =>
    request<T>("/replan/status"),
  getReplanComparison: <T = Record<string, unknown>>() =>
    request<T>("/replan/comparison"),

  // 12. Plan Verification
  verifyPlan: <T = Record<string, unknown>>(payload?: { student_id?: string; target_deadline?: string }) =>
    request<T>("/verification", {
      method: "POST",
      body: JSON.stringify(payload || {}),
    }),
  getVerification: <T = Record<string, unknown>>() =>
    request<T>("/verification"),

  // 13. Demo Simulation
  simulateEvent: <T = Record<string, unknown>>(payload: { scenario: string; topic?: string; custom_note?: string }) =>
    request<T>("/simulation/simulate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // 14. OpenAI Reasoning Intelligence
  aiExplainGap: <T = Record<string, unknown>>(payload: { topic: string; severity?: string; mastery?: number }) =>
    request<T>("/ai/explain-gap", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  aiExplainResource: <T = Record<string, unknown>>(payload: { resource_id: string; resource_title: string; topic: string; resource_type: string }) =>
    request<T>("/ai/explain-resource", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  aiExplainPlanChange: <T = Record<string, unknown>>(payload: { new_version?: number; reason?: string }) =>
    request<T>("/ai/explain-plan-change", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  aiPersonalizedAdvice: <T = Record<string, unknown>>(payload?: { student_id?: string }) =>
    request<T>("/ai/personalized-advice", {
      method: "POST",
      body: JSON.stringify(payload || {}),
    }),
  aiSuggestStrategies: <T = Record<string, unknown>>(payload?: { challenge?: string; available_hours?: number }) =>
    request<T>("/ai/strategies", {
      method: "POST",
      body: JSON.stringify(payload || {}),
    }),
  aiAnswerQuestion: <T = Record<string, unknown>>(payload: {
    question: string;
    topic?: string;
    student_id?: string;
    quick_action?: string;
    student_answer?: string;
  }) =>
    request<T>("/ai/answer-question", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  aiProblemHints: <T = Record<string, unknown>>(payload: { problem_title: string; topic?: string; difficulty?: string }) =>
    request<T>("/ai/problem-hints", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // 15. Adaptive Practice
  getAdaptiveQuestion: <T = Record<string, unknown>>(topic: string = "Graphs", difficulty?: string) => {
    const diffQuery = difficulty ? `&difficulty=${encodeURIComponent(difficulty)}` : "";
    return request<T>(`/practice/adaptive/question?topic=${encodeURIComponent(topic)}${diffQuery}`);
  },
  submitAdaptiveAttempt: <T = Record<string, unknown>>(payload: {
    question_id: string;
    topic: string;
    difficulty: string;
    selected_option_id: string;
    time_spent_seconds: number;
    attempt_number?: number;
    student_id?: string;
  }) =>
    request<T>("/practice/adaptive/attempt", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // 16. Authentication & Session
  login: <T = Record<string, unknown>>(payload: { email: string; password: string; remember_me?: boolean }) =>
    request<T>("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  register: <T = Record<string, unknown>>(payload: {
    full_name: string;
    email: string;
    password: string;
    confirm_password: string;
    terms?: boolean;
  }) =>
    request<T>("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  logout: <T = Record<string, unknown>>() =>
    request<T>("/auth/logout", {
      method: "POST",
    }),
  getMe: <T = Record<string, unknown>>() =>
    request<T>("/auth/me"),
  forgotPassword: <T = Record<string, unknown>>(payload: { email: string }) =>
    request<T>("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  resetPassword: <T = Record<string, unknown>>(payload: {
    token: string;
    new_password: string;
    confirm_password: string;
  }) =>
    request<T>("/auth/reset-password", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  completeOnboarding: <T = Record<string, unknown>>(payload: {
    current_goal?: string;
    target_deadline?: string;
    weekly_target_hours?: number;
    subjects?: string[];
  }) =>
    request<T>("/auth/onboarding", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  googleAuth: <T = Record<string, unknown>>(payload: {
    email: string;
    full_name?: string;
    avatar_url?: string;
    google_id?: string;
    id_token?: string;
  }) =>
    request<T>("/auth/google", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};



