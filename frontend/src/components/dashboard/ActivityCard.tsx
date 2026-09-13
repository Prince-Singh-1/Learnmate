/**
 * ActivityCard — Shows a single learning activity from the plan.
 */

import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Clock, Video, FileText, Dumbbell, HelpCircle } from "lucide-react";
import type { PlanActivity } from "@/types";

interface ActivityCardProps {
  activity: PlanActivity;
  index: number;
}

const typeIcons: Record<string, typeof Video> = {
  video: Video,
  article: FileText,
  exercise: Dumbbell,
  quiz: HelpCircle,
};

const statusColors: Record<string, string> = {
  completed: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300",
  pending: "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300",
  missed: "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300",
  deferred: "bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300",
};

export function ActivityCard({ activity, index }: ActivityCardProps) {
  const TypeIcon = typeIcons[activity.resource_type] || FileText;
  const statusClass = statusColors[activity.status] || statusColors.pending;

  const startTime = new Date(activity.scheduled_start).toLocaleString(
    undefined,
    {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }
  );

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
    >
      <Card className="transition-shadow hover:shadow-md">
        <CardContent className="flex items-center gap-4 p-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-secondary">
            <TypeIcon className="h-5 w-5 text-secondary-foreground" />
          </div>

          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium">
              {activity.resource_title}
            </p>
            <p className="text-xs text-muted-foreground">{activity.topic}</p>
          </div>

          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Clock className="h-3 w-3" />
            {startTime}
          </div>

          <Badge variant="outline" className={statusClass}>
            {activity.status}
          </Badge>
        </CardContent>
      </Card>
    </motion.div>
  );
}
