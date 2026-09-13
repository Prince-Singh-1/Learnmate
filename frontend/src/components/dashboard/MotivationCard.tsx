/**
 * MotivationCard — Goal forecast and daily motivational card with night mountain
 * artwork, achievement badges, and inspirational quote. (Light theme)
 */

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";
import { goalForecast } from "@/data/mockData";

export function MotivationCard() {
  return (
    <div className="space-y-4">
      {/* Top Card: You're on the right path with 3D night peaks */}
      <motion.div
        whileHover={{ y: -3, scale: 1.01 }}
        transition={{ duration: 0.2 }}
        className="relative overflow-hidden rounded-2xl border border-slate-200/90 p-5 shadow-md min-h-[150px] flex flex-col justify-between group"
      >
        {/* Background Image with 3D Depth */}
        <img
          src="/night-peaks-3d.jpg"
          alt="3D Night mountain peaks with aurora"
          className="absolute inset-0 h-full w-full object-cover object-center brightness-90 group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/40 to-transparent" />

        {/* Content */}
        <div className="relative z-10">
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-white/90 drop-shadow">
            <Sparkles className="h-3.5 w-3.5 text-amber-300 animate-pulse" />
            <span>Goal Forecast</span>
          </div>
          <h4 className="text-base font-bold text-white mt-1 drop-shadow-md">
            "{goalForecast.message}"
          </h4>
        </div>

        {/* Badges */}
        <div className="relative z-10 flex flex-wrap gap-1.5 pt-2">
          {goalForecast.badges.map((badge, idx) => (
            <span
              key={idx}
              className="rounded-lg border border-white/30 bg-white/20 px-2.5 py-0.5 text-[10px] font-bold text-white backdrop-blur-md shadow-xs"
            >
              {badge}
            </span>
          ))}
        </div>
      </motion.div>

      {/* Bottom Card: A better you is a brighter tomorrow */}
      <motion.div
        whileHover={{ y: -2 }}
        className="card-3d p-5 flex items-center justify-between gap-4 shadow-xs"
      >
        <div className="space-y-1">
          <p className="text-sm font-bold italic text-slate-800 leading-snug">
            {goalForecast.quote}
          </p>
          <p className="text-[11px] text-slate-500 font-medium">Keep showing up everyday</p>
        </div>

        {/* Aesthetic potted plant illustration / graphic */}
        <div className="flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-xl bg-emerald-50 border border-emerald-100 text-2xl shadow-2xs">
          🪴
        </div>
      </motion.div>
    </div>
  );
}
