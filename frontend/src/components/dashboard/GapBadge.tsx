/**
 * GapBadge — Shows a knowledge gap with severity indicator.
 */

import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

interface GapBadgeProps {
  topic: string;
  mastery: number;
  index: number;
}

export function GapBadge({ topic, mastery, index }: GapBadgeProps) {
  const severity = mastery < 0.3 ? "critical" : mastery < 0.5 ? "warning" : "mild";

  const severityColors = {
    critical: "border-red-300 bg-red-50 text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-300",
    warning: "border-amber-300 bg-amber-50 text-amber-700 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-300",
    mild: "border-blue-300 bg-blue-50 text-blue-700 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-300",
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2, delay: index * 0.08 }}
      className={`inline-flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-medium ${severityColors[severity]}`}
    >
      <AlertTriangle className="h-3.5 w-3.5" />
      <span>{topic}</span>
      <span className="text-xs opacity-70">
        {(mastery * 100).toFixed(0)}%
      </span>
    </motion.div>
  );
}
