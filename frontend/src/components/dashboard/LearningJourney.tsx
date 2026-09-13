/**
 * LearningJourney — 6-step autonomous pipeline matching reference image:
 * Analyze -> Identify -> Select -> Create -> Learn -> Adapt -> Achieve Your Goals! (Light theme)
 */

import { motion } from "framer-motion";
import {
  BarChart3,
  Search,
  BookOpen,
  CalendarDays,
  Target,
  RefreshCw,
  Rocket,
  Check,
} from "lucide-react";
import { journeySteps } from "@/data/mockData";

const iconMap = [
  BarChart3,
  Search,
  BookOpen,
  CalendarDays,
  Target,
  RefreshCw,
];

interface LearningJourneyProps {
  onStepClick?: (stepIndex: number) => void;
}

export function LearningJourney({ onStepClick }: LearningJourneyProps) {
  return (
    <div className="card-3d p-6 shadow-xs">
      {/* Title */}
      <div className="flex items-center justify-between pb-6 border-b border-slate-100">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-primary shadow-xs">
            <Target className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">
              Your Learning Journey
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              From where you are to where you want to be.
            </p>
          </div>
        </div>

        <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-bold text-primary shadow-2xs">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
          Continuous Autonomous Loop
        </span>
      </div>

      {/* Horizontal Pipeline Steps */}
      <div className="relative flex flex-col md:flex-row items-center justify-between gap-4 pt-6">
        {/* Connecting line (Desktop) */}
        <div className="absolute top-[52px] left-[5%] right-[15%] h-[2px] bg-gradient-to-r from-emerald-200 via-indigo-300 to-purple-300 hidden md:block z-0" />

        {journeySteps.map((item, index) => {
          const Icon = iconMap[index] || Target;
          const isCompleted = item.completed;
          const isActive = item.active;

          return (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
              whileHover={{ y: -4, scale: 1.05 }}
              onClick={() => onStepClick?.(index)}
              className="relative z-10 flex flex-col items-center text-center cursor-pointer group"
            >
              {/* Node Icon Circle */}
              <div
                className={`relative flex h-14 w-14 items-center justify-center rounded-2xl border transition-all duration-300 ${
                  isActive
                    ? "border-primary bg-primary text-white shadow-lg shadow-primary/35 scale-105"
                    : isCompleted
                    ? "border-emerald-300 bg-emerald-50 text-emerald-600 group-hover:border-emerald-400 shadow-sm"
                    : "border-slate-200/90 bg-white text-slate-400 group-hover:border-slate-300 shadow-2xs"
                }`}
              >
                {isCompleted ? (
                  <Check className="h-6 w-6 stroke-[2.5]" />
                ) : (
                  <Icon className="h-6 w-6" />
                )}

                {/* Step badge */}
                <span className="absolute -top-1.5 -right-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-white border border-slate-200 text-[10px] font-bold text-slate-700 shadow-xs">
                  {item.step}
                </span>
              </div>

              {/* Labels */}
              <div className="mt-2.5">
                <p className="text-xs font-bold text-slate-800 group-hover:text-primary transition-colors">
                  {item.step}. {item.title}
                </p>
                <p className="text-[10px] text-slate-500 font-medium">{item.subtitle}</p>
              </div>
            </motion.div>
          );
        })}

        {/* Goal Achievement End 3D Trophy */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          whileHover={{ scale: 1.08, y: -2 }}
          className="relative z-10 flex flex-col items-center text-center group cursor-pointer"
        >
          <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl border-2 border-purple-300 overflow-hidden shadow-xl shadow-purple-500/25 bg-slate-950">
            <img
              src="/badge-streak-3d.jpg"
              alt="3D Goal Trophy"
              className="h-full w-full object-cover object-center group-hover:scale-115 transition-transform duration-300"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent pointer-events-none" />
            <Rocket className="absolute bottom-1 right-1 h-3.5 w-3.5 text-amber-300" />
          </div>
          <div className="mt-2">
            <p className="text-xs font-extrabold text-slate-900 group-hover:text-primary transition-colors">
              Achieve Your Goals
            </p>
            <p className="text-[10px] text-primary font-bold">Target Nov 2025</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

