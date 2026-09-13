/**
 * AiAssistantCard — AI Learning Assistant companion card with 3D robot mascot,
 * interactive quick action pills, and chat input. (Light theme)
 */

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, Send, Sparkles } from "lucide-react";
import { aiActions, studentProfile } from "@/data/mockData";

interface AiAssistantCardProps {
  onOpenFullChat?: () => void;
  onActionSelect?: (prompt: string) => void;
}

export function AiAssistantCard({
  onOpenFullChat: _onOpenFullChat,
  onActionSelect,
}: AiAssistantCardProps) {

  const [inputQuery, setInputQuery] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "bot" | "user"; text: string }>>([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = (textToSend?: string) => {
    const query = textToSend || inputQuery;
    if (!query.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: query }]);
    setInputQuery("");
    setIsTyping(true);

    setTimeout(() => {
      let botResponse = "I've analyzed your question. Let's focus on Dynamic Programming memoization patterns!";
      if (query.toLowerCase().includes("plan") || query.toLowerCase().includes("adjust")) {
        botResponse = "I checked your calendar. Rescheduling 'Binary Trees' to tomorrow 4:00 PM will keep you 100% on track for your Nov 30 deadline!";
      } else if (query.toLowerCase().includes("practice") || query.toLowerCase().includes("question")) {
        botResponse = "Here is a high-yield question: 'Given an array of integers, find the maximum subarray sum in O(n) time.' Ready to solve?";
      } else if (query.toLowerCase().includes("resource")) {
        botResponse = "Recommended: 'Graph Algorithms Explained' by freeCodeCamp (30 mins). It directly bridges your shortest-path knowledge gap!";
      }

      setMessages((prev) => [...prev, { role: "bot", text: botResponse }]);
      setIsTyping(false);
    }, 900);
  };

  return (
    <div className="card-3d p-5 h-full flex flex-col justify-between shadow-xs">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-primary shadow-xs">
              <Bot className="h-4 w-4" />
            </div>
            <h3 className="text-sm font-bold text-slate-800">
              AI Learning Assistant
            </h3>
          </div>

          <div className="flex items-center gap-1.5 rounded-full bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 text-[10px] font-bold text-emerald-600 shadow-2xs">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
            Online
          </div>
        </div>

        {/* Mascot + Initial Bubble */}
        <div className="flex items-start gap-3 pt-3">
          <motion.div
            whileHover={{ rotate: [0, -6, 6, 0], scale: 1.08 }}
            transition={{ type: "spring", stiffness: 260, damping: 15 }}
            className="relative flex-shrink-0 h-16 w-16 rounded-2xl overflow-hidden border border-slate-200/90 shadow-md bg-slate-950 ring-2 ring-indigo-500/20"
          >
            <img
              src="/ai-robot-3d.jpg"
              alt="3D AI Assistant Mascot"
              className="h-full w-full object-cover object-center transition-transform hover:scale-110 duration-300"
            />
          </motion.div>

          <div className="flex-1 rounded-2xl rounded-tl-sm border border-indigo-100/80 bg-indigo-50/50 p-3 text-xs leading-relaxed text-slate-700 shadow-2xs">
            <p className="font-bold text-slate-900 mb-0.5">
              Hi {studentProfile.name}! 👋
            </p>
            <p className="text-[11px] text-slate-500">
              I'm your AI learning companion. I can help you with:
            </p>
          </div>
        </div>

        {/* Chat History if any */}
        {messages.length > 0 && (
          <div className="mt-3 max-h-36 overflow-y-auto space-y-2 pr-1 scrollbar-none">
            <AnimatePresence>
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`text-xs p-2.5 rounded-xl max-w-[90%] ${
                    msg.role === "user"
                      ? "ml-auto bg-primary text-white font-medium"
                      : "mr-auto bg-slate-50 text-slate-800 border border-slate-200"
                  }`}
                >
                  {msg.text}
                </motion.div>
              ))}
              {isTyping && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-[11px] text-slate-500 italic flex items-center gap-1.5"
                >
                  <Sparkles className="h-3 w-3 text-primary animate-spin" />
                  AI Tutor is thinking...
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}

        {/* Action Pills */}
        <div className="mt-3 space-y-1.5">
          {aiActions.map((action) => (
            <motion.button
              key={action.id}
              whileHover={{ x: 2, backgroundColor: "#f8fafc" }}
              whileTap={{ scale: 0.98 }}
              onClick={() => {
                handleSend(action.label);
                onActionSelect?.(action.label);
              }}
              className="flex w-full items-center gap-2.5 rounded-xl border border-slate-200/80 bg-slate-50/50 px-3 py-1.5 text-left text-xs font-semibold text-slate-700 hover:text-primary hover:border-primary/40 transition-all"
            >
              <span className="text-sm">{action.icon}</span>
              <span className="flex-1 truncate">{action.label}</span>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Input box */}
      <div className="relative mt-4 pt-2">
        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask me anything..."
          className="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 pl-3.5 pr-10 text-xs text-slate-800 placeholder-slate-400 outline-none focus:border-primary/50 focus:bg-white transition-all shadow-2xs"
        />
        <button
          onClick={() => handleSend()}
          disabled={!inputQuery.trim()}
          className="absolute right-1.5 top-3.5 flex h-7 w-7 items-center justify-center rounded-lg gradient-primary text-white disabled:opacity-40 transition-opacity hover:opacity-90 shadow-xs"
        >
          <Send className="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  );
}
