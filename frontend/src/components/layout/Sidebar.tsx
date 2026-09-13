/**
 * Sidebar — Dark navy/purple gradient sidebar with navigation.
 */

import { motion } from "framer-motion";
import {
  LayoutDashboard,
  Target,
  CalendarDays,
  BookOpen,
  FlaskConical,
  BarChart3,
  Calendar,
  Bot,
  Trophy,
  Users,
  Settings,
  Brain,
  ChevronRight,
  Sparkles,
} from "lucide-react";
import { sidebarNavItems } from "@/data/mockData";
import type { LucideIcon } from "lucide-react";

interface SidebarProps {
  activePage: string;
  onNavigate: (page: string) => void;
}

const iconMap: Record<string, LucideIcon> = {
  LayoutDashboard,
  Target,
  CalendarDays,
  BookOpen,
  FlaskConical,
  BarChart3,
  Calendar,
  Bot,
  Trophy,
  Users,
  Settings,
  Sparkles,
};

const sidebarVariants = {
  hidden: { x: -20, opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: { staggerChildren: 0.04, delayChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { x: -10, opacity: 0 },
  visible: { x: 0, opacity: 1 },
};

export function Sidebar({ activePage, onNavigate }: SidebarProps) {
  return (
    <aside className="fixed left-0 top-0 z-50 flex h-screen w-[220px] flex-col gradient-sidebar border-r border-white/[0.06]">
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 py-5">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl gradient-primary glow-sm">
          <Brain className="h-5 w-5 text-white" />
        </div>
        <div>
          <h1 className="text-base font-bold text-white tracking-tight">
            LearnMate
          </h1>
          <p className="text-[10px] text-white/40 tracking-wide">
            Learn Smarter. Grow Bigger.
          </p>
        </div>
      </div>

      {/* Navigation */}
      <motion.nav
        className="flex-1 space-y-0.5 overflow-y-auto px-3 py-3 scrollbar-none"
        variants={sidebarVariants}
        initial="hidden"
        animate="visible"
      >
        {sidebarNavItems.map((item) => {
          const Icon = iconMap[item.iconName] || LayoutDashboard;
          const isActive = activePage === item.id;

          return (
            <motion.button
              key={item.id}
              variants={itemVariants}
              onClick={() => onNavigate(item.id)}
              className={`relative flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium transition-all duration-200 group ${
                isActive
                  ? "text-white"
                  : "text-white/50 hover:text-white/80 hover:bg-white/[0.04]"
              }`}
              whileTap={{ scale: 0.97 }}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active-bg"
                  className="absolute inset-0 rounded-xl gradient-primary opacity-90 glow-sm"
                  transition={{
                    type: "spring",
                    bounce: 0.15,
                    duration: 0.5,
                  }}
                />
              )}
              <Icon className="relative z-10 h-[18px] w-[18px]" />
              <span className="relative z-10">{item.label}</span>
              {isActive && (
                <ChevronRight className="relative z-10 ml-auto h-3.5 w-3.5 opacity-60" />
              )}
            </motion.button>
          );
        })}
      </motion.nav>

      {/* Motivational Quote with Night Mountain artwork */}
      <div className="border-t border-white/[0.06] p-3">
        <div className="relative overflow-hidden rounded-xl border border-white/[0.08] p-3 shadow-lg min-h-[90px] flex items-end">
          <img
            src="/night-mountain.jpg"
            alt="Mountain night sky"
            className="absolute inset-0 h-full w-full object-cover object-center opacity-40 brightness-90"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
          <p className="relative z-10 text-[11px] font-medium italic text-white/80 leading-snug drop-shadow">
            "Discipline today builds the freedom you want tomorrow."
          </p>
        </div>
      </div>
    </aside>
  );
}
