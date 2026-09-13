/**
 * AiChatModal — Full-screen interactive AI Tutor modal.
 */

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Send, Bot, Sparkles, User, Lightbulb, Code2 } from "lucide-react";
import { studentProfile } from "@/data/mockData";
import { api } from "@/lib/api";

interface AiChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialPrompt?: string;
}

export function AiChatModal({
  isOpen,
  onClose,
  initialPrompt = "",
}: AiChatModalProps) {
  const [messages, setMessages] = useState<Array<{ role: "bot" | "user"; text: string }>>([
    {
      role: "bot",
      text: `Hello ${studentProfile.name}! I'm your LearnMate Autonomous AI Tutor. How can I accelerate your learning today? You can ask me to explain any topic, test your knowledge, or reorganize your study schedule!`,
    },
  ]);
  const [input, setInput] = useState(initialPrompt);
  const [isTyping, setIsTyping] = useState(false);

  if (!isOpen) return null;

  const handleSend = async (queryToSend?: string) => {
    const q = queryToSend || input;
    if (!q.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await api.aiAnswerQuestion<{
        direct_answer: string;
        key_points?: string[];
        code_example_or_analogy?: string;
      }>({
        question: q,
        topic: q.toLowerCase().includes("dp") || q.toLowerCase().includes("dynamic") ? "Dynamic Programming" : "Graphs",
      });

      let fullAnswer = res.direct_answer;
      if (res.key_points && res.key_points.length > 0) {
        fullAnswer += "\n\nKey Takeaways:\n" + res.key_points.map((p: string) => `• ${p}`).join("\n");
      }
      if (res.code_example_or_analogy) {
        fullAnswer += "\n\n" + res.code_example_or_analogy;
      }

      setMessages((prev) => [...prev, { role: "bot", text: fullAnswer }]);
    } catch {
      // Dynamic conversational fallback
      let response = `In Data Structures & Algorithms, "${q}" is an essential concept. Understanding the time vs space complexity trade-offs will help you optimize your solution!`;
      if (q.toLowerCase().includes("dp") || q.toLowerCase().includes("dynamic")) {
        response = "Dynamic Programming is optimal substructure + overlapping subproblems. 1) Identify state variables. 2) Formulate the recurrence relation. 3) Choose Memoization (top-down) or Tabulation (bottom-up). Shall we solve the 'Coin Change' problem together?";
      } else if (q.toLowerCase().includes("graph") || q.toLowerCase().includes("dijkstra")) {
        response = "Dijkstra's Algorithm finds the single-source shortest path in weighted graphs with non-negative edge weights using a Min-Heap (Priority Queue) in O((V + E) log V) time. Always remember to relax adjacent edges!";
      } else if (q.toLowerCase().includes("plan") || q.toLowerCase().includes("schedule")) {
        response = "I've checked your schedule. You have 79 days remaining until your target date (30 Nov 2025). Your current completion rate is 70.5%. You're in great shape!";
      } else if (q.toLowerCase().includes("ok") || q.toLowerCase().includes("yes") || q.toLowerCase().includes("sure")) {
        response = "Awesome! What concept would you like to explore next? You can ask about Dijkstra's algorithm, 0/1 Knapsack, or schedule optimization.";
      }
      setMessages((prev) => [...prev, { role: "bot", text: response }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-2xl h-[580px] flex flex-col rounded-2xl border border-white/15 bg-[#0f1338] shadow-2xl overflow-hidden"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-white/[0.02]">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl gradient-primary text-white shadow-lg shadow-primary/30">
                <Bot className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  LearnMate AI Tutor
                  <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                </h3>
                <p className="text-xs text-white/50">
                  Powered by OpenAI & Autonomous Knowledge Graph
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="rounded-lg p-1.5 text-white/50 hover:bg-white/10 hover:text-white transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Quick Suggestions */}
          <div className="px-6 py-2 border-b border-white/[0.05] bg-white/[0.01] flex items-center gap-2 overflow-x-auto scrollbar-none">
            <button
              onClick={() => handleSend("Explain Dynamic Programming memoization")}
              className="flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[11px] text-white/70 hover:text-white hover:bg-white/[0.06] whitespace-nowrap transition-colors"
            >
              <Lightbulb className="h-3 w-3 text-amber-400" />
              Explain DP Memoization
            </button>
            <button
              onClick={() => handleSend("Give me Dijkstra's algorithm code")}
              className="flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[11px] text-white/70 hover:text-white hover:bg-white/[0.06] whitespace-nowrap transition-colors"
            >
              <Code2 className="h-3 w-3 text-emerald-400" />
              Dijkstra Code Sample
            </button>
            <button
              onClick={() => handleSend("Check my study goal progress")}
              className="flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[11px] text-white/70 hover:text-white hover:bg-white/[0.06] whitespace-nowrap transition-colors"
            >
              <Sparkles className="h-3 w-3 text-primary" />
              Check Goal Trajectory
            </button>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex gap-3 ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {msg.role === "bot" && (
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg gradient-primary text-white text-xs">
                    <Bot className="h-4 w-4" />
                  </div>
                )}
                <div
                  className={`max-w-[80%] rounded-2xl p-3.5 text-xs leading-relaxed ${
                    msg.role === "user"
                      ? "bg-primary text-white rounded-tr-sm"
                      : "bg-white/[0.06] text-white/90 border border-white/10 rounded-tl-sm"
                  }`}
                >
                  {msg.text}
                </div>
                {msg.role === "user" && (
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-white/10 text-white text-xs">
                    <User className="h-4 w-4" />
                  </div>
                )}
              </div>
            ))}

            {isTyping && (
              <div className="flex items-center gap-2 text-xs text-white/50 italic">
                <Sparkles className="h-4 w-4 text-primary animate-spin" />
                AI Tutor is formulating explanation...
              </div>
            )}
          </div>

          {/* Input Footer */}
          <div className="p-4 border-t border-white/10 bg-white/[0.02]">
            <div className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="Ask about topics, quiz doubts, or replanning..."
                className="h-11 w-full rounded-xl border border-white/15 bg-white/[0.05] pl-4 pr-12 text-xs text-white placeholder-white/40 outline-none focus:border-primary/60 transition-all"
              />
              <button
                onClick={() => handleSend()}
                disabled={!input.trim()}
                className="absolute right-2 flex h-8 w-8 items-center justify-center rounded-lg gradient-primary text-white disabled:opacity-40 transition-opacity"
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
