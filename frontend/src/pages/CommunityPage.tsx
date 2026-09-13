/**
 * CommunityPage — Peer study groups, peer question discussions, and leaderboard. (Light Theme)
 */

import { motion } from "framer-motion";
import { Users, MessageSquare, Award, Flame } from "lucide-react";

export function CommunityPage() {
  const leaderboard = [
    { rank: 1, name: "Aarav Sharma", streak: 28, solved: 142, points: 3420 },
    { rank: 2, name: "Prince Singh (You)", streak: 12, solved: 42, points: 2180 },
    { rank: 3, name: "Sneha Patel", streak: 19, solved: 88, points: 2040 },
    { rank: 4, name: "Rohan Gupta", streak: 9, solved: 35, points: 1820 },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary mb-2">
            <Users className="h-3.5 w-3.5" />
            Collaborative Learning Network
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Community & Leaderboard</h2>
          <p className="text-xs text-slate-500 mt-1">
            Learn alongside fellow students preparing for interviews and exams.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Leaderboard */}
        <div className="lg:col-span-7 rounded-2xl border border-slate-200/80 bg-white p-6 space-y-4 shadow-xs">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Award className="h-4 w-4 text-amber-500" />
              University CSE Leaderboard
            </h3>
            <span className="text-xs text-slate-500 font-medium">Weekly Rankings</span>
          </div>

          <div className="space-y-2.5">
            {leaderboard.map((user) => (
              <div
                key={user.rank}
                className={`flex items-center justify-between p-3 rounded-xl border transition-all ${
                  user.rank === 2
                    ? "border-indigo-300 bg-indigo-50/40 shadow-xs font-semibold"
                    : "border-slate-200/70 bg-white hover:bg-slate-50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span
                    className={`flex h-7 w-7 items-center justify-center rounded-lg text-xs font-bold ${
                      user.rank === 1
                        ? "bg-amber-100 text-amber-800"
                        : user.rank === 2
                        ? "gradient-primary text-white shadow-2xs"
                        : "bg-slate-100 text-slate-600"
                    }`}
                  >
                    #{user.rank}
                  </span>
                  <span className="text-xs font-bold text-slate-800">{user.name}</span>
                </div>

                <div className="flex items-center gap-4 text-xs font-medium text-slate-600">
                  <span className="flex items-center gap-1 text-orange-600 font-semibold">
                    <Flame className="h-3 w-3" /> {user.streak}d
                  </span>
                  <span className="font-mono text-slate-900 font-bold">{user.points} pts</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Study Groups */}
        <div className="lg:col-span-5 rounded-2xl border border-slate-200/80 bg-white p-6 space-y-4 shadow-xs">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <MessageSquare className="h-4 w-4 text-cyan-600" />
              Active Study Circles
            </h3>
          </div>

          <div className="space-y-3">
            {[
              { name: "DSA Sprint 2025", members: 48, topic: "DP & Trees", active: "12 online" },
              { name: "System Design Prep", members: 32, topic: "Scalability", active: "5 online" },
              { name: "Competitive Coders", members: 64, topic: "Codeforces/LeetCode", active: "21 online" },
            ].map((group) => (
              <div key={group.name} className="p-3 rounded-xl border border-slate-200/80 bg-slate-50/60 hover:bg-white transition-all shadow-2xs">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-slate-900">{group.name}</h4>
                  <span className="text-[10px] text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">{group.active}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1 font-medium">{group.topic} • {group.members} members</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
