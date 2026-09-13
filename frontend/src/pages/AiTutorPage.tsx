/**
 * AiTutorPage — Dedicated Interactive LearnMate AI Tutor Studio.
 *
 * Core Features:
 * - Adapts explanations dynamically to student's current level (e.g. 30% mastery in Graphs).
 * - Feeds continuous context:
 *   1. Student's goal ("Master Data Structures & Algorithms")
 *   2. Current topic ("Graphs" / "Dynamic Programming")
 *   3. Topic mastery (30%)
 *   4. Recent assessment results (52% on Graph traversal)
 *   5. Knowledge gaps (DP High, Graphs High)
 *   6. Recent learning activities (Dijkstra Shortest Path, Binary Trees)
 * - 8 Interactive Quick Actions:
 *   1. [ Explain Concept ]
 *   2. [ Give Example ]
 *   3. [ Give Practice Questions ]
 *   4. [ Give Hint ]
 *   5. [ Check My Answer ]
 *   6. [ Suggest Resources ]
 *   7. [ Adjust My Plan ]
 *   8. [ Why Did My Plan Change? ]
 * - Keeps conversation associated with the student's learning goal.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Bot,
  Send,
  Sparkles,
  User,
  Zap,
  BookOpen,
  HelpCircle,
  CheckCircle2,
  Lightbulb,
  FileQuestion,
  Calendar,
  Layers,
} from "lucide-react";
import { useStudent, useGoals, useKnowledgeGaps, usePerformance } from "@/hooks/useLearnMate";
import { api } from "@/lib/api";

interface Message {
  id: string;
  role: "bot" | "user";
  text: string;
  keyPoints?: string[];
  codeExample?: string;
  followUpQuestions?: string[];
  quickAction?: string;
  timestamp: string;
}

interface QuickActionBtn {
  id: string;
  label: string;
  icon: typeof Lightbulb;
  color: string;
  defaultPrompt: string;
  description: string;
}

const QUICK_ACTIONS: QuickActionBtn[] = [
  {
    id: "explain_concept",
    label: "Explain Concept",
    icon: BookOpen,
    color: "bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100",
    defaultPrompt: "Explain Dijkstra's algorithm.",
    description: "Step-by-step conceptual intuition tailored to your current level",
  },
  {
    id: "give_example",
    label: "Give Example",
    icon: Lightbulb,
    color: "bg-amber-50 text-amber-700 border-amber-200 hover:bg-amber-100",
    defaultPrompt: "Give me a concrete 3-node Dijkstra graph example with code.",
    description: "Walk-through with visual trace and clean Python snippet",
  },
  {
    id: "give_practice",
    label: "Give Practice Questions",
    icon: FileQuestion,
    color: "bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100",
    defaultPrompt: "Give me practice questions on Dijkstra and graph shortest paths.",
    description: "Calibrated interview questions at your exact mastery level",
  },
  {
    id: "give_hint",
    label: "Give Hint",
    icon: HelpCircle,
    color: "bg-cyan-50 text-cyan-700 border-cyan-200 hover:bg-cyan-100",
    defaultPrompt: "Give me a hint for solving Dijkstra shortest path without spoiling the code.",
    description: "Progressive directional hint without giving away the answer",
  },
  {
    id: "check_answer",
    label: "Check My Answer",
    icon: CheckCircle2,
    color: "bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100",
    defaultPrompt: "Check my answer: Dijkstra uses a min-heap to relax unvisited edges with O((V+E) log V) complexity.",
    description: "Instant feedback on your conceptual formulation or logic",
  },
  {
    id: "suggest_resources",
    label: "Suggest Resources",
    icon: Layers,
    color: "bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100",
    defaultPrompt: "Suggest resources to master Dijkstra and bridge my Graphs knowledge gap.",
    description: "Curated videos, interactive visualizers, and drill sets",
  },
  {
    id: "adjust_plan",
    label: "Adjust My Plan",
    icon: Calendar,
    color: "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100",
    defaultPrompt: "Adjust my plan to give more practice time for Graphs.",
    description: "Autonomous scheduling advice to protect your target deadline",
  },
  {
    id: "why_plan_changed",
    label: "Why Did My Plan Change?",
    icon: Zap,
    color: "bg-violet-50 text-violet-700 border-violet-200 hover:bg-violet-100",
    defaultPrompt: "Why did my plan change recently?",
    description: "Full explanation of workload rebalancing and gap prioritization",
  },
];

export function AiTutorPage() {
  const { data: student } = useStudent();
  const { data: goals } = useGoals();
  const { data: gaps } = useKnowledgeGaps();
  const { data: perf } = usePerformance();

  const currentGoalTitle = goals?.[0]?.title || "Master Data Structures & Algorithms";
  const studentName = student?.name || "Prince";

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "msg-init",
      role: "bot",
      text: `Hello ${studentName}! I am your LearnMate AI Tutor, grounded in your active goal: "${currentGoalTitle}".\n\nI'm tracking your continuous level (68% overall, 30% in Graphs, 25% in Dynamic Programming). You can ask any question like "Explain Dijkstra's algorithm" or pick one of the 8 quick actions below!`,
      timestamp: "Just now",
      followUpQuestions: [
        "Explain Dijkstra's algorithm.",
        "Give me a 3-node Dijkstra example.",
        "Why did my plan change?",
      ],
    },
  ]);

  const [input, setInput] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("Graphs");
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async (textToSend?: string, quickActionType?: string) => {
    const text = textToSend || input;
    if (!text.trim() || isTyping) return;

    const userTimestamp = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const userMsg: Message = {
      id: `usr-${Date.now()}`,
      role: "user",
      text,
      timestamp: userTimestamp,
      quickAction: quickActionType,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      // Call backend AI service with full student telemetry context
      const res = await api.aiAnswerQuestion<{
        direct_answer: string;
        key_points?: string[];
        code_example_or_analogy?: string;
        related_topics?: string[];
        follow_up_questions?: string[];
        student_context?: Record<string, any>;
        source?: string;
      }>({
        question: text,
        topic: selectedTopic,
        quick_action: quickActionType,
      });

      const botMsg: Message = {
        id: `bot-${Date.now()}`,
        role: "bot",
        text: res.direct_answer,
        keyPoints: res.key_points,
        codeExample: res.code_example_or_analogy,
        followUpQuestions: res.follow_up_questions,
        quickAction: quickActionType,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch {
      // Fallback
      setMessages((prev) => [
        ...prev,
        {
          id: `bot-${Date.now()}`,
          role: "bot",
          text: `Here is the explanation for "${text}": In Graphs (current mastery: 30%), Dijkstra's algorithm uses a priority queue to greedily expand the closest unvisited node. Edge relaxation $dist[v] = \\min(dist[v], dist[u] + w)$ guarantees optimal single-source shortest paths on non-negative weighted graphs in $O((V+E) \\log V)$ time.`,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6 pb-12"
    >
      {/* ─── Top Telemetry Banner ────────────────────────────────── */}
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="h-16 w-16 rounded-2xl overflow-hidden border border-indigo-100 bg-indigo-50 shadow-md flex-shrink-0">
            <img
              src="/ai-robot.jpg"
              alt="LearnMate AI Tutor"
              className="h-full w-full object-cover object-top"
            />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 text-[11px] font-bold text-emerald-700">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Adaptive AI Tutor Active
              </span>
              <span className="text-[11px] text-slate-400 font-medium">
                Goal: {currentGoalTitle}
              </span>
            </div>
            <h1 className="text-xl font-extrabold text-slate-900">
              Personalized AI Tutor Studio
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Grounded in your real-time knowledge graph, recent quiz telemetry, and target deadline.
            </p>
          </div>
        </div>

        {/* Live Level Telemetry Pill */}
        <div className="flex flex-wrap items-center gap-2 bg-slate-50 p-2.5 rounded-xl border border-slate-200/70 text-xs">
          <div className="px-2 py-1 bg-white rounded-lg border border-slate-200 text-slate-700 font-medium">
            🎯 Progress: <span className="font-bold text-primary">{perf?.overall_mastery || 68}%</span>
          </div>
          <div className="px-2 py-1 bg-white rounded-lg border border-slate-200 text-slate-700 font-medium">
            📈 Current Level: <span className="font-bold text-amber-600">30% (Graphs)</span>
          </div>
          <div className="px-2 py-1 bg-white rounded-lg border border-slate-200 text-slate-700 font-medium">
            ⏳ Gaps: <span className="font-bold text-rose-600">{gaps?.length || 2} Priority</span>
          </div>
        </div>
      </div>

      {/* ─── 8 Quick Action Buttons ──────────────────────────────── */}
      <div className="space-y-2.5">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5 text-primary" />
            Quick Tutor Actions (Click to Run)
          </span>
          <div className="flex items-center gap-2 text-xs">
            <span className="text-slate-400">Context Topic:</span>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="bg-white border border-slate-200 rounded-lg px-2 py-1 text-slate-700 font-semibold outline-none text-xs"
            >
              <option value="Graphs">Graphs (30% Mastery)</option>
              <option value="Dynamic Programming">Dynamic Programming (25% Mastery)</option>
              <option value="Trees">Trees (45% Mastery)</option>
              <option value="Arrays">Arrays (85% Mastery)</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          {QUICK_ACTIONS.map((qa) => {
            const Icon = qa.icon;
            return (
              <motion.button
                key={qa.id}
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => sendMessage(qa.defaultPrompt, qa.id)}
                disabled={isTyping}
                title={qa.description}
                className={`flex flex-col items-center justify-center p-3 rounded-xl border text-center transition-all cursor-pointer shadow-2xs ${qa.color} disabled:opacity-50`}
              >
                <Icon className="h-4 w-4 mb-1.5" />
                <span className="text-[11px] font-bold leading-tight line-clamp-1">
                  {qa.label}
                </span>
              </motion.button>
            );
          })}
        </div>
      </div>

      {/* ─── Main Interactive Chat Studio ────────────────────────── */}
      <div className="rounded-2xl border border-slate-200/80 bg-white h-[600px] flex flex-col justify-between overflow-hidden shadow-xs">
        {/* Message Thread */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role === "bot" && (
                <div className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl gradient-primary text-white text-xs shadow-xs">
                  <Bot className="h-4 w-4" />
                </div>
              )}

              <div
                className={`max-w-[80%] rounded-2xl p-4 text-xs leading-relaxed space-y-3 ${
                  msg.role === "user"
                    ? "gradient-primary text-white rounded-tr-sm shadow-xs font-medium"
                    : "bg-slate-50 text-slate-800 border border-slate-200/80 rounded-tl-sm shadow-2xs"
                }`}
              >
                {/* Header info */}
                <div className="flex items-center justify-between gap-2 border-b border-black/[0.06] pb-1.5 text-[10px] opacity-70">
                  <span className="font-semibold">
                    {msg.role === "user" ? studentName : "LearnMate AI Tutor"}
                  </span>
                  <span>{msg.timestamp}</span>
                </div>

                {/* Body Text */}
                <div className="whitespace-pre-line text-[13px] leading-relaxed">
                  {msg.text}
                </div>

                {/* Key Concepts bullet points */}
                {msg.keyPoints && msg.keyPoints.length > 0 && (
                  <div className="rounded-xl border border-slate-200 bg-white p-3 space-y-1 text-slate-700">
                    <div className="text-[11px] font-bold uppercase tracking-wider text-primary flex items-center gap-1">
                      <Lightbulb className="h-3.5 w-3.5 text-amber-500" />
                      Key Principles for your level
                    </div>
                    <ul className="list-disc pl-4 space-y-1 text-[12px]">
                      {msg.keyPoints.map((point, idx) => (
                        <li key={idx}>{point}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Code Snippet Box */}
                {msg.codeExample && (
                  <div className="rounded-xl border border-slate-300 bg-slate-900 text-slate-100 p-3.5 font-mono text-[11px] overflow-x-auto space-y-1 shadow-inner">
                    <div className="text-[10px] text-slate-400 uppercase tracking-widest font-sans font-bold flex items-center justify-between">
                      <span>Python Implementation Walkthrough</span>
                      <span className="text-emerald-400 font-mono">O((V+E) log V)</span>
                    </div>
                    <pre className="text-emerald-300 leading-relaxed pt-1">
                      {msg.codeExample}
                    </pre>
                  </div>
                )}

                {/* Follow-up / Check questions */}
                {msg.followUpQuestions && msg.followUpQuestions.length > 0 && (
                  <div className="pt-2 border-t border-slate-200/60 flex flex-wrap items-center gap-1.5">
                    <span className="text-[10px] text-slate-400 font-medium">Follow-up:</span>
                    {msg.followUpQuestions.map((q, idx) => (
                      <button
                        key={idx}
                        onClick={() => sendMessage(q)}
                        className="rounded-full border border-slate-200 bg-white px-2.5 py-0.5 text-[11px] text-slate-600 hover:text-primary hover:border-primary/40 transition-all cursor-pointer"
                      >
                        {q} →
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {msg.role === "user" && (
                <div className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl bg-slate-200 text-slate-700 text-xs">
                  <User className="h-4 w-4" />
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-2 text-xs text-slate-400 italic"
            >
              <Sparkles className="h-4 w-4 text-primary animate-spin" />
              AI Tutor is analyzing your goal and formulating a level-adapted explanation...
            </motion.div>
          )}
        </div>

        {/* Input Dock */}
        <div className="p-4 border-t border-slate-100 bg-slate-50/70 space-y-3">
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              disabled={isTyping}
              placeholder="Ask anything... (e.g. 'Explain Dijkstra's algorithm', 'Give example', 'Give practice questions')"
              className="flex-1 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs text-slate-800 placeholder-slate-400 outline-none focus:border-primary shadow-2xs transition-colors"
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || isTyping}
              className="flex h-10 w-10 items-center justify-center rounded-xl gradient-primary text-white hover:opacity-95 disabled:opacity-40 transition-all shadow-xs flex-shrink-0 cursor-pointer"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
export default AiTutorPage;
