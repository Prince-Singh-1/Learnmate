/**
 * SettingsPage — Student study preferences, daily study hours configuration,
 * notification settings, and AI autonomous sensitivity controls. (Light Theme)
 */

import { useState } from "react";
import { motion } from "framer-motion";
import { Settings, Sliders, Bell, User, LogOut, ShieldCheck } from "lucide-react";
import { useStudent } from "@/hooks/useLearnMate";
import { useAuth } from "@/context/AuthContext";

interface SettingsPageProps {
  onNavigate?: (page: string) => void;
}

export function SettingsPage({ onNavigate }: SettingsPageProps) {
  const { data: student } = useStudent();
  const { user, student: authStudent, logout } = useAuth();
  const [dailyHours, setDailyHours] = useState(2.5);
  const [autoReplan, setAutoReplan] = useState(true);
  const [notifications, setNotifications] = useState(true);

  const displayName = user?.full_name || authStudent?.name || student?.name || "Prince Singh";
  const displayEmail = user?.email || authStudent?.email || student?.email || "prince.singh@university.edu";
  const displayRole = authStudent?.degree || student?.degree || student?.role || student?.level || "Computer Science Major";

  const handleLogout = async () => {
    await logout();
    onNavigate?.("login");
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary mb-2">
            <Settings className="h-3.5 w-3.5" />
            Preferences & Engine Configuration
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Platform Settings</h2>
          <p className="text-xs text-slate-500 mt-1">
            Configure autonomous replanning thresholds, daily availability, and account details.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Profile Card */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 space-y-4 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 pb-2 border-b border-slate-100">
            <User className="h-4 w-4 text-primary" />
            Student Profile
          </h3>

          <div className="flex items-center gap-4">
            <img
              src={student?.avatar || "/prince-avatar.jpg"}
              alt={displayName}
              className="h-16 w-16 rounded-2xl object-cover border border-slate-200 shadow-sm"
            />
            <div>
              <h4 className="text-base font-bold text-slate-900">{displayName}</h4>
              <p className="text-xs text-slate-500">{displayEmail}</p>
              <p className="text-xs text-primary font-semibold mt-0.5">{displayRole}</p>
            </div>
          </div>
        </div>

        {/* Autonomous Engine Sensitivity */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 space-y-4 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 pb-2 border-b border-slate-100">
            <Sliders className="h-4 w-4 text-cyan-600" />
            Autonomous Replanning Behavior
          </h3>

          <div className="space-y-4 pt-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-800">Instant Reschedule on Missed Activity</p>
                <p className="text-[11px] text-slate-500">Auto-shift tasks into upcoming available study slots</p>
              </div>
              <button
                onClick={() => setAutoReplan(!autoReplan)}
                className={`w-11 h-6 flex items-center rounded-full p-1 transition-colors ${
                  autoReplan ? "bg-primary" : "bg-slate-200"
                }`}
              >
                <div
                  className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                    autoReplan ? "translate-x-5" : "translate-x-0"
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2">
                <Bell className="h-4 w-4 text-indigo-500" />
                <div>
                  <p className="text-xs font-semibold text-slate-800">Study Reminders & Alerts</p>
                  <p className="text-[11px] text-slate-500">Push notifications before scheduled study windows</p>
                </div>
              </div>
              <button
                onClick={() => setNotifications(!notifications)}
                className={`w-11 h-6 flex items-center rounded-full p-1 transition-colors ${
                  notifications ? "bg-primary" : "bg-slate-200"
                }`}
              >
                <div
                  className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                    notifications ? "translate-x-5" : "translate-x-0"
                  }`}
                />
              </button>
            </div>

            <div className="space-y-2 pt-2 border-t border-slate-100">
              <div className="flex justify-between text-xs font-medium">
                <span className="text-slate-700">Daily Target Study Time</span>
                <span className="text-primary font-bold">{dailyHours} hrs / day</span>
              </div>
              <input
                type="range"
                min="1"
                max="6"
                step="0.5"
                value={dailyHours}
                onChange={(e) => setDailyHours(parseFloat(e.target.value))}
                className="w-full accent-primary cursor-pointer"
              />
            </div>
          </div>
        </div>

        {/* Security & Session Card */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 space-y-4 shadow-xs lg:col-span-2">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-2 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <ShieldCheck className="h-4 w-4 text-emerald-600" />
                Security & Session Management
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Active session authenticated as <strong className="text-slate-700">{displayEmail}</strong>.
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 rounded-xl border border-rose-200 bg-rose-50 px-4 py-2 text-xs font-bold text-rose-600 hover:bg-rose-100 transition-colors cursor-pointer"
            >
              <LogOut className="h-4 w-4" />
              Sign Out of LearnMate
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
