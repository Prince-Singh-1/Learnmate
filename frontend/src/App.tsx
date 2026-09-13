/**
 * LearnMate — Root Application Component
 *
 * Full authentication flow, session management, URL synchronization,
 * protected routes, onboarding flow, and AI tutor modal integration.
 */

import { useState, useEffect, useCallback } from "react";
import { PageShell } from "@/components/layout";
import { AiChatModal } from "@/components/dashboard";
import { ToastProvider } from "@/components/ui/Toast";
import { AuthProvider, useAuth } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import {
  DashboardPage,
  GoalsPage,
  PlanPage,
  ResourcesPage,
  PracticePage,
  PerformancePage,
  CalendarPage,
  AiTutorPage,
  AchievementsPage,
  CommunityPage,
  SettingsPage,
  SimulationPage,
  LoginPage,
  RegisterPage,
  ForgotPasswordPage,
  LandingPage,
  OnboardingPage,
} from "@/pages";

function getPageFromPath(path: string): string {
  const clean = path.replace(/^\/+|\/+$/g, "");
  if (!clean) return "landing";
  if (clean === "login") return "login";
  if (clean === "register") return "register";
  if (clean === "forgot-password") return "forgot-password";
  if (clean === "onboarding") return "onboarding";
  if (clean === "agent" || clean === "demo") return "simulation";
  return clean;
}

function getPathForPage(page: string): string {
  if (page === "landing") return "/";
  return `/${page}`;
}

function AppRouter() {
  const { isAuthenticated, isLoading, user } = useAuth();
  const [activePage, setActivePage] = useState<string>(() => {
    if (typeof window !== "undefined") {
      return getPageFromPath(window.location.pathname);
    }
    return "landing";
  });
  const [aiModalOpen, setAiModalOpen] = useState(false);

  const navigate = useCallback((page: string) => {
    setActivePage(page);
    if (typeof window !== "undefined") {
      const newPath = getPathForPage(page);
      if (window.location.pathname !== newPath) {
        window.history.pushState(null, "", newPath);
      }
    }
  }, []);

  // Handle browser forward/back buttons
  useEffect(() => {
    const handlePopState = () => {
      const page = getPageFromPath(window.location.pathname);
      setActivePage(page);
    };
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  // Auto-redirect from login/register if already authenticated
  useEffect(() => {
    if (!isLoading && isAuthenticated && (activePage === "login" || activePage === "register")) {
      if (user?.onboarding_completed === false) {
        navigate("onboarding");
      } else {
        navigate("dashboard");
      }
    }
  }, [isAuthenticated, isLoading, activePage, user, navigate]);

  // Render Public Auth & Landing Pages
  if (activePage === "landing") {
    return <LandingPage onNavigate={navigate} />;
  }
  if (activePage === "login") {
    return <LoginPage onNavigate={navigate} />;
  }
  if (activePage === "register") {
    return <RegisterPage onNavigate={navigate} />;
  }
  if (activePage === "forgot-password") {
    return <ForgotPasswordPage onNavigate={navigate} />;
  }
  if (activePage === "onboarding") {
    return (
      <ProtectedRoute onNavigate={navigate}>
        <OnboardingPage onNavigate={navigate} />
      </ProtectedRoute>
    );
  }

  // Render Protected Application Pages
  return (
    <ProtectedRoute onNavigate={navigate}>
      <PageShell
        activePage={activePage}
        onNavigate={navigate}
        onOpenAi={() => setAiModalOpen(true)}
      >
        {activePage === "dashboard" && <DashboardPage onNavigate={navigate} />}
        {activePage === "goals" && <GoalsPage />}
        {activePage === "plan" && <PlanPage />}
        {activePage === "resources" && <ResourcesPage />}
        {activePage === "practice" && <PracticePage />}
        {activePage === "progress" && <PerformancePage />}
        {activePage === "calendar" && <CalendarPage />}
        {activePage === "ai-tutor" && <AiTutorPage />}
        {activePage === "achievements" && <AchievementsPage />}
        {activePage === "community" && <CommunityPage />}
        {activePage === "simulation" && <SimulationPage />}
        {activePage === "settings" && <SettingsPage onNavigate={navigate} />}

        <AiChatModal
          isOpen={aiModalOpen}
          onClose={() => setAiModalOpen(false)}
          initialPrompt="Help me plan my study schedule"
        />
      </PageShell>
    </ProtectedRoute>
  );
}

export function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <AppRouter />
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
