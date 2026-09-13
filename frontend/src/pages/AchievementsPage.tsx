/**
 * AchievementsPage — Gamified rewards, streak trophies, and certificates. (Light Theme)
 */

import { motion } from "framer-motion";
import { Trophy } from "lucide-react";

export function AchievementsPage() {
  const badges = [
    {
      title: "12-Day Streak Master",
      desc: "Maintained unbroken daily study habit",
      image: "/badge-streak-3d.jpg",
      unlocked: true,
      tag: "Habit Pioneer",
    },
    {
      title: "Zero Gaps Hero",
      desc: "Closed 5 critical algorithmic knowledge gaps",
      image: "/badge-shield-3d.jpg",
      unlocked: true,
      tag: "Shield Master",
    },
    {
      title: "DP Architect",
      desc: "Completed 20 Dynamic Programming challenges",
      image: "/badge-dp-3d.jpg",
      unlocked: true,
      tag: "Optimal Substructure",
    },
    {
      title: "Graph Conqueror",
      desc: "Solved 15 shortest-path and DAG problems",
      image: "/res-graph-video.jpg",
      unlocked: true,
      tag: "Dijkstra Specialist",
    },
    {
      title: "Night Owl Scholar",
      desc: "Completed 3 intensive study sessions after 8:00 PM",
      image: "/night-peaks-3d.jpg",
      unlocked: true,
      tag: "Focus Champion",
    },
    {
      title: "Interview Ready",
      desc: "Achieve 85% overall topic mastery across all domains",
      image: "/hero-student-3d.jpg",
      unlocked: false,
      tag: "Grandmaster",
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="card-3d flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 shadow-xs">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary mb-2 shadow-2xs">
            <Trophy className="h-3.5 w-3.5" />
            Milestones & Mastery
          </div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Achievements & 3D Badges</h2>
          <p className="text-xs text-slate-500 mt-1">
            Celebrate consistent learning momentum and algorithmic breakthroughs with rendered 3D awards.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-xl border border-amber-200 bg-amber-50/80 px-4 py-2 text-center shadow-2xs">
            <span className="text-xs text-amber-700 font-bold">Unlocked</span>
            <p className="text-base font-extrabold text-slate-900">5 of 6 Badges</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {badges.map((b, i) => {
          return (
            <motion.div
              key={b.title}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              whileHover={{ y: -4, scale: 1.01 }}
              className={`card-3d p-5 flex items-start gap-4 transition-all shadow-xs overflow-hidden ${
                b.unlocked ? "border-slate-200/90" : "opacity-60 bg-slate-50/50"
              }`}
            >
              {/* 3D Visual Badge Thumbnail */}
              <div className="relative flex h-16 w-16 flex-shrink-0 items-center justify-center rounded-2xl overflow-hidden border border-slate-200/90 shadow-md bg-slate-950">
                <img
                  src={b.image}
                  alt={b.title}
                  className="h-full w-full object-cover object-center transition-transform hover:scale-115 duration-300"
                />
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-1">
                  <h4 className="text-sm font-bold text-slate-900 truncate">{b.title}</h4>
                </div>
                <p className="text-xs text-slate-500 mt-1 leading-snug">{b.desc}</p>
                <div className="mt-3 flex items-center gap-2">
                  <span
                    className={`rounded px-2 py-0.5 text-[10px] font-bold ${
                      b.unlocked
                        ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                        : "bg-slate-100 text-slate-600 border border-slate-200"
                    }`}
                  >
                    {b.unlocked ? "Unlocked" : "In Progress"}
                  </span>
                  <span className="text-[10px] text-slate-400 font-medium">
                    {b.tag}
                  </span>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
