import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Sparkles,
  Bell,
  ChevronDown,
  User,
  Settings,
  LogOut,
  CheckCircle2,
  Clock,
  Sparkle,
} from "lucide-react";
import { useStudent } from "@/hooks/useLearnMate";
import { useAuth } from "@/context/AuthContext";

interface TopBarProps {
  onOpenAi?: () => void;
  onNavigate?: (page: string) => void;
}

export function TopBar({ onOpenAi, onNavigate }: TopBarProps) {
  const { data: student } = useStudent();
  const { user, student: authStudent, logout } = useAuth();
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [notificationList, setNotificationList] = useState([
    {
      id: "n-1",
      title: "Autonomous Replan Activated",
      desc: "Plan v11 synthesized to recover 45m after missed Tree video.",
      time: "10 mins ago",
      type: "replan",
      unread: true,
    },
    {
      id: "n-2",
      title: "Knowledge Gap Resolved",
      desc: "Graphs mastery increased from 30% to 81%. Great job!",
      time: "1 hour ago",
      type: "achievement",
      unread: true,
    },
    {
      id: "n-3",
      title: "Upcoming Study Session",
      desc: "Dynamic Programming Memoization scheduled for 4:00 PM.",
      time: "3 hours ago",
      type: "reminder",
      unread: false,
    },
  ]);

  const displayName = user?.full_name || authStudent?.name || student?.name || "Prince Singh";
  const displayEmail = user?.email || authStudent?.email || student?.email || "prince.singh@university.edu";
  const displayRole = authStudent?.degree || student?.degree || student?.role || student?.level || "Computer Science Major";
  const unreadCount = notificationList.filter((n) => n.unread).length;

  const markAllRead = () => {
    setNotificationList((prev) => prev.map((n) => ({ ...n, unread: false })));
  };

  const handleLogout = async () => {
    setProfileOpen(false);
    await logout();
    onNavigate?.("login");
  };

  return (
    <motion.header
      initial={{ y: -10, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="sticky top-0 z-40 flex h-16 items-center justify-between gap-4 border-b border-slate-200/80 bg-white/85 px-6 backdrop-blur-xl shadow-xs"
    >
      {/* Search */}
      <div className="relative flex-1 max-w-xl">
        <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          placeholder="Search for topics, courses, questions or ask AI anything..."
          className="h-10 w-full rounded-xl border border-slate-200 bg-slate-50/80 pl-10 pr-20 text-xs text-slate-800 placeholder-slate-400 outline-none transition-all focus:border-primary/50 focus:bg-white focus:ring-2 focus:ring-primary/20"
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1">
          <kbd className="rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[10px] text-slate-400 shadow-xs">
            Ctrl
          </kbd>
          <kbd className="rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[10px] text-slate-400 shadow-xs">
            K
          </kbd>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3 relative">
        {/* Ask AI Button */}
        <motion.button
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          onClick={onOpenAi}
          className="flex items-center gap-2 rounded-xl gradient-primary px-4 py-2 text-xs font-semibold text-white shadow-md shadow-primary/20 transition-all hover:shadow-lg hover:shadow-primary/30 cursor-pointer"
        >
          <Sparkles className="h-4 w-4" />
          Ask AI
        </motion.button>

        {/* Notifications Bell Icon */}
        <div className="relative">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              setNotificationsOpen(!notificationsOpen);
              setProfileOpen(false);
            }}
            className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 hover:text-slate-900 shadow-xs cursor-pointer"
            aria-label="Notifications"
          >
            <Bell className="h-4 w-4" />
            {unreadCount > 0 && (
              <span className="absolute -right-1 -top-1 flex h-4.5 w-4.5 items-center justify-center rounded-full bg-red-500 text-[9px] font-bold text-white shadow-xs animate-pulse">
                {unreadCount}
              </span>
            )}
          </motion.button>

          {/* Notifications Dropdown Panel */}
          <AnimatePresence>
            {notificationsOpen && (
              <motion.div
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                transition={{ duration: 0.15 }}
                className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl border border-slate-200/90 bg-white shadow-2xl p-4 z-50 space-y-3"
              >
                <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
                  <div className="flex items-center gap-2">
                    <Bell className="h-4 w-4 text-primary" />
                    <h4 className="text-sm font-bold text-slate-900">Notifications</h4>
                    {unreadCount > 0 && (
                      <span className="rounded-full bg-indigo-50 border border-indigo-100 px-2 py-0.2 text-[10px] font-bold text-primary">
                        {unreadCount} new
                      </span>
                    )}
                  </div>
                  <button
                    onClick={markAllRead}
                    className="text-[11px] font-semibold text-primary hover:underline cursor-pointer"
                  >
                    Mark all read
                  </button>
                </div>

                <div className="space-y-2 max-h-72 overflow-y-auto">
                  {notificationList.map((n) => (
                    <div
                      key={n.id}
                      className={`p-3 rounded-xl border transition-all ${
                        n.unread
                          ? "bg-indigo-50/40 border-indigo-100"
                          : "bg-slate-50/50 border-slate-100"
                      }`}
                    >
                      <div className="flex items-start gap-2.5">
                        {n.type === "replan" ? (
                          <Sparkle className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                        ) : n.type === "achievement" ? (
                          <CheckCircle2 className="h-4 w-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                        ) : (
                          <Clock className="h-4 w-4 text-amber-500 mt-0.5 flex-shrink-0" />
                        )}
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-bold text-slate-900">{n.title}</p>
                          <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">{n.desc}</p>
                          <span className="text-[10px] text-slate-400 font-mono mt-1 block">{n.time}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="border-t border-slate-100 pt-2 text-center">
                  <button
                    onClick={() => {
                      setNotificationsOpen(false);
                      onNavigate?.("simulation");
                    }}
                    className="text-xs font-semibold text-primary hover:underline cursor-pointer"
                  >
                    View Autonomous Activity Log →
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Profile Card & Dropdown Menu */}
        <div className="relative">
          <motion.button
            whileHover={{ scale: 1.02 }}
            onClick={() => {
              setProfileOpen(!profileOpen);
              setNotificationsOpen(false);
            }}
            className="flex items-center gap-2.5 rounded-xl border border-slate-200 bg-white p-1.5 pr-3 transition-colors hover:bg-slate-50 shadow-xs cursor-pointer"
          >
            <img
              src={student?.avatar || "/prince-avatar.jpg"}
              alt={displayName}
              className="h-8 w-8 rounded-lg object-cover border border-slate-200"
            />
            <div className="text-left hidden sm:block">
              <p className="text-xs font-semibold text-slate-800">
                {displayName}
              </p>
              <p className="text-[10px] text-slate-500">{displayRole}</p>
            </div>
            <ChevronDown className="h-3.5 w-3.5 text-slate-400 ml-0.5" />
          </motion.button>

          {/* Profile Dropdown Menu */}
          <AnimatePresence>
            {profileOpen && (
              <motion.div
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                transition={{ duration: 0.15 }}
                className="absolute right-0 mt-2 w-56 rounded-2xl border border-slate-200/90 bg-white shadow-xl p-2 z-50 space-y-1"
              >
                <div className="px-3 py-2 border-b border-slate-100">
                  <p className="text-xs font-bold text-slate-900">{displayName}</p>
                  <p className="text-[10px] text-slate-400 truncate">{displayEmail}</p>
                </div>

                <button
                  onClick={() => {
                    setProfileOpen(false);
                    onNavigate?.("settings");
                  }}
                  className="w-full flex items-center gap-2 rounded-xl px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
                >
                  <User className="h-3.5 w-3.5 text-slate-400" />
                  Profile Details
                </button>

                <button
                  onClick={() => {
                    setProfileOpen(false);
                    onNavigate?.("settings");
                  }}
                  className="w-full flex items-center gap-2 rounded-xl px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
                >
                  <Settings className="h-3.5 w-3.5 text-slate-400" />
                  Preferences
                </button>

                <div className="border-t border-slate-100 pt-1">
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2 rounded-xl px-3 py-2 text-xs font-medium text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
                  >
                    <LogOut className="h-3.5 w-3.5 text-rose-500" />
                    Log Out
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </motion.header>
  );
}
