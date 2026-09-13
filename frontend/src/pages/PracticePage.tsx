/**
 * PracticePage — Adaptive Practice & Challenge Suite.
 *
 * Core Features:
 * 1. Question difficulty responds dynamically to student performance:
 *    - Easy -> correct -> Medium
 *    - Medium -> correct -> Hard
 *    - Hard -> wrong -> Medium + explanation
 *    - Medium -> wrong -> Easy + explanation
 * 2. Tracks:
 *    - question
 *    - topic
 *    - difficulty
 *    - answer
 *    - correctness
 *    - time
 *    - attempt number
 * 3. After an assessment / attempt:
 *    - Updates topic mastery score
 *    - Updates knowledge gaps
 *    - Checks whether replanning is required
 * 4. Connects assessment results directly to the autonomous learning agent.
 */

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  FlaskConical,
  CheckCircle2,
  XCircle,
  Clock,
  Sparkles,
  AlertTriangle,
  TrendingUp,
  ArrowRight,
  HelpCircle,
} from "lucide-react";
import {
  useKnowledgeGaps,
  usePerformance,
  useAdaptiveQuestion,
  useSubmitAdaptiveAttempt,
  type AdaptiveQuestionData,
  type AdaptiveAttemptResultData,
} from "@/hooks/useLearnMate";

export function PracticePage() {
  const [selectedTopic, setSelectedTopic] = useState<string>("Graphs");
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [secondsSpent, setSecondsSpent] = useState<number>(0);
  const [attemptCount, setAttemptCount] = useState<number>(1);
  const [lastAttemptResult, setLastAttemptResult] = useState<AdaptiveAttemptResultData | null>(null);

  // Active question from backend
  const { data: initialQ, isLoading: isQLoading } = useAdaptiveQuestion(selectedTopic);
  const [currentQuestion, setCurrentQuestion] = useState<AdaptiveQuestionData | null>(null);

  // Telemetry log history
  const [attemptHistory, setAttemptHistory] = useState<Array<{
    id: string;
    question: string;
    topic: string;
    difficulty: string;
    answer: string;
    correctness: boolean;
    time: number;
    attempt: number;
  }>>([]);

  const { data: gaps } = useKnowledgeGaps();
  const { data: performance } = usePerformance();
  const submitAttemptMutation = useSubmitAdaptiveAttempt();

  useEffect(() => {
    if (initialQ && !currentQuestion) {
      setCurrentQuestion(initialQ);
    }
  }, [initialQ]);

  // Timer
  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsSpent((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleTopicChange = (newTopic: string) => {
    setSelectedTopic(newTopic);
    setSelectedOption(null);
    setSecondsSpent(0);
    setAttemptCount(1);
    setLastAttemptResult(null);
    setCurrentQuestion(null);
  };

  const handleSubmitAnswer = () => {
    if (!currentQuestion || !selectedOption || submitAttemptMutation.isPending) return;

    submitAttemptMutation.mutate(
      {
        question_id: currentQuestion.id,
        topic: currentQuestion.topic,
        difficulty: currentQuestion.difficulty,
        selected_option_id: selectedOption,
        time_spent_seconds: secondsSpent,
        attempt_number: attemptCount,
      },
      {
        onSuccess: (data) => {
          setLastAttemptResult(data);

          const selectedText =
            currentQuestion.options.find((o) => o.id === selectedOption)?.text || selectedOption;

          // Add to tracked telemetry list
          setAttemptHistory((prev) => [
            {
              id: data.attempt_id,
              question: currentQuestion.question_text,
              topic: currentQuestion.topic,
              difficulty: currentQuestion.difficulty,
              answer: selectedText,
              correctness: data.is_correct,
              time: secondsSpent,
              attempt: attemptCount,
            },
            ...prev,
          ]);

          // Progress to next question if provided
          if (data.next_question) {
            setCurrentQuestion(data.next_question);
          }
          setSelectedOption(null);
          setSecondsSpent(0);
          setAttemptCount((prev) => prev + 1);
        },
      }
    );
  };

  // Find active gap for selected topic
  const activeGap = gaps?.find(
    (g) => g.topic.toLowerCase() === selectedTopic.toLowerCase()
  );

  const activeMastery = performance?.topic_mastery?.find(
    (m) => m.topic.toLowerCase() === selectedTopic.toLowerCase()
  );

  return (
    <div className="space-y-6 pb-12">
      {/* ─── Hero Banner ─────────────────────────────────────────── */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-3d p-6 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-6"
      >
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 border border-indigo-100 text-primary shadow-xs">
            <FlaskConical className="h-7 w-7" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-50 border border-indigo-200 px-2.5 py-0.5 text-[11px] font-bold text-primary">
                <Sparkles className="h-3.5 w-3.5 text-amber-500" />
                Adaptive Practice Engine
              </span>
              {lastAttemptResult?.replan_required && (
                <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 border border-amber-300 px-2.5 py-0.5 text-[11px] font-bold text-amber-800 animate-pulse">
                  <AlertTriangle className="h-3 w-3 text-amber-600" />
                  Autonomous Replan Connected
                </span>
              )}
            </div>
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
              Adaptive Practice & Mastery Calibration
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Difficulty continuously responds to your answer accuracy:{" "}
              <span className="font-semibold text-slate-700">Easy → Medium → Hard</span>, or steps down with guided explanations.
            </p>
          </div>
        </div>

        {/* Topic Selector & Level */}
        <div className="flex items-center gap-3">
          <div className="text-right text-xs">
            <div className="text-slate-400 font-medium">Active Gap:</div>
            <div className="font-bold text-rose-600">
              {activeGap?.severity || "High"} Priority ({activeMastery?.mastery_score || 30}% Mastery)
            </div>
          </div>
          <select
            value={selectedTopic}
            onChange={(e) => handleTopicChange(e.target.value)}
            className="rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-bold text-slate-800 outline-none shadow-2xs cursor-pointer focus:border-primary"
          >
            <option value="Graphs">Graphs</option>
            <option value="Dynamic Programming">Dynamic Programming</option>
          </select>
        </div>
      </motion.div>

      {/* ─── Main Practice Workspace & Progression ────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Adaptive Question Card (8 cols) */}
        <div className="lg:col-span-8 space-y-5">
          <div className="card-3d p-6 shadow-xs space-y-6">
            {/* Header: Difficulty Badge + Timer + Attempt # */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2.5">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                    currentQuestion?.difficulty === "Hard"
                      ? "bg-rose-50 text-rose-700 border border-rose-200"
                      : currentQuestion?.difficulty === "Medium"
                      ? "bg-amber-50 text-amber-700 border border-amber-200"
                      : "bg-emerald-50 text-emerald-700 border border-emerald-200"
                  }`}
                >
                  {currentQuestion?.difficulty || "Medium"} Difficulty
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  Topic: <strong className="text-slate-700">{currentQuestion?.topic || selectedTopic}</strong>
                </span>
              </div>

              <div className="flex items-center gap-4 text-xs font-medium text-slate-600">
                <span className="flex items-center gap-1.5 bg-slate-50 px-3 py-1 rounded-lg border border-slate-200">
                  <Clock className="h-3.5 w-3.5 text-slate-400" />
                  Time: <strong className="font-mono text-slate-900">{secondsSpent}s</strong>
                </span>
                <span className="bg-slate-50 px-3 py-1 rounded-lg border border-slate-200">
                  Attempt: <strong className="text-primary">#{attemptCount}</strong>
                </span>
              </div>
            </div>

            {/* Question Body */}
            {isQLoading && !currentQuestion ? (
              <div className="p-8 text-center text-xs text-slate-400">
                Loading adaptive question...
              </div>
            ) : (
              <div className="space-y-4">
                <h2 className="text-base font-bold text-slate-900 leading-snug">
                  {currentQuestion?.question_text}
                </h2>

                {/* Multiple Choice Options */}
                <div className="space-y-2.5 pt-2">
                  {currentQuestion?.options.map((opt) => {
                    const isChecked = selectedOption === opt.id;
                    return (
                      <button
                        key={opt.id}
                        onClick={() => setSelectedOption(opt.id)}
                        className={`flex w-full items-center gap-3 rounded-xl border p-3.5 text-left text-xs transition-all cursor-pointer ${
                          isChecked
                            ? "border-primary bg-indigo-50/50 text-primary font-bold shadow-xs ring-1 ring-primary/30"
                            : "border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
                        }`}
                      >
                        <div
                          className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full text-[11px] font-bold border ${
                            isChecked
                              ? "border-primary bg-primary text-white"
                              : "border-slate-300 text-slate-500"
                          }`}
                        >
                          {opt.id.replace("opt-", "")}
                        </div>
                        <span className="flex-1">{opt.text}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Footer Submission Action */}
            <div className="flex items-center justify-between pt-4 border-t border-slate-100">
              <span className="text-xs text-slate-400">
                Concept Target: <strong className="text-slate-600">{currentQuestion?.target_concept}</strong>
              </span>

              <button
                onClick={handleSubmitAnswer}
                disabled={!selectedOption || submitAttemptMutation.isPending}
                className="flex items-center gap-2 rounded-xl gradient-primary px-5 py-2.5 text-xs font-bold text-white shadow-xs hover:opacity-95 disabled:opacity-40 transition-all cursor-pointer"
              >
                <span>{submitAttemptMutation.isPending ? "Evaluating..." : "Submit Answer"}</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* ─── Adaptive Feedback Banner (Shown after Attempt) ──────── */}
          {lastAttemptResult && (
            <motion.div
              initial={{ opacity: 0, scale: 0.98, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              className={`rounded-2xl border p-5 space-y-3 ${
                lastAttemptResult.is_correct
                  ? "bg-emerald-50/70 border-emerald-200 text-emerald-900"
                  : "bg-rose-50/70 border-rose-200 text-rose-900"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {lastAttemptResult.is_correct ? (
                    <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                  ) : (
                    <XCircle className="h-5 w-5 text-rose-600" />
                  )}
                  <h3 className="text-sm font-bold">
                    {lastAttemptResult.is_correct
                      ? "Correct! Difficulty Escalated"
                      : "Incorrect — Adaptive Reinforcement"}
                  </h3>
                </div>

                <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-white/70 border border-slate-200">
                  Next Level: {lastAttemptResult.adaptation.next_difficulty}
                </span>
              </div>

              <p className="text-xs leading-relaxed font-medium">
                {lastAttemptResult.adaptation.adaptation_reason}
              </p>

              {/* In-depth concept explanation on wrong answer */}
              {lastAttemptResult.adaptation.explanation && (
                <div className="rounded-xl border border-slate-200 bg-white p-3 text-xs text-slate-700 leading-relaxed shadow-2xs space-y-1">
                  <div className="font-bold text-slate-900 flex items-center gap-1.5">
                    <HelpCircle className="h-3.5 w-3.5 text-primary" />
                    Pedagogical Explanation:
                  </div>
                  <p>{lastAttemptResult.adaptation.explanation}</p>
                </div>
              )}

              {/* Autonomous Agent Connection Alert */}
              {lastAttemptResult.replan_required && (
                <div className="rounded-xl border border-amber-300 bg-amber-50 p-3 text-xs text-amber-900 space-y-1">
                  <div className="font-bold flex items-center gap-1.5 text-amber-950">
                    <AlertTriangle className="h-4 w-4 text-amber-600" />
                    Autonomous Learning Agent Triggered
                  </div>
                  <p className="text-amber-800">
                    "{lastAttemptResult.replan_reason}"
                  </p>
                  <div className="text-[11px] text-amber-700 font-mono pt-1">
                    ✓ Knowledge gaps updated • Autonomous schedule updated • Deadline verified
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </div>

        {/* Right Column: Tracked Telemetry & Adaptation Rules (4 cols) */}
        <div className="lg:col-span-4 space-y-5">
          {/* Difficulty State Machine Card */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
              <TrendingUp className="h-4 w-4 text-primary" />
              Adaptive Difficulty Logic
            </h3>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50 border border-slate-200/70">
                <span className="font-medium text-slate-700">Easy → Correct</span>
                <span className="font-bold text-emerald-600">→ Medium</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50 border border-slate-200/70">
                <span className="font-medium text-slate-700">Medium → Correct</span>
                <span className="font-bold text-indigo-600">→ Hard</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50 border border-slate-200/70">
                <span className="font-medium text-slate-700">Hard → Wrong</span>
                <span className="font-bold text-amber-600">→ Medium + Expl</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50 border border-slate-200/70">
                <span className="font-medium text-slate-700">Medium → Wrong</span>
                <span className="font-bold text-rose-600">→ Easy + Expl</span>
              </div>
            </div>
          </div>

          {/* Real-time Tracked Attempts List */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs space-y-3">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <Clock className="h-4 w-4 text-primary" />
                Tracked Telemetry Logs
              </h3>
              <span className="text-[11px] text-slate-400 font-semibold">
                {attemptHistory.length} recorded
              </span>
            </div>

            <div className="max-h-[360px] overflow-y-auto space-y-2.5 pr-1 scrollbar-none">
              {attemptHistory.length === 0 ? (
                <div className="p-6 text-center text-xs text-slate-400 italic">
                  No attempts recorded yet. Submit your first answer to start tracking telemetry.
                </div>
              ) : (
                attemptHistory.map((att, i) => (
                  <div
                    key={att.id || i}
                    className="rounded-xl border border-slate-200 bg-slate-50/50 p-3 text-xs space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <span
                        className={`font-bold text-[11px] px-2 py-0.5 rounded-md ${
                          att.correctness
                            ? "bg-emerald-100 text-emerald-800"
                            : "bg-rose-100 text-rose-800"
                        }`}
                      >
                        {att.correctness ? "✓ Correct" : "✗ Wrong"} ({att.difficulty})
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">
                        {att.time}s • Attempt #{att.attempt}
                      </span>
                    </div>

                    <div className="font-semibold text-slate-800 line-clamp-1">
                      {att.question}
                    </div>
                    <div className="text-[11px] text-slate-500 truncate">
                      Answer: <span className="font-medium text-slate-700">{att.answer}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default PracticePage;
