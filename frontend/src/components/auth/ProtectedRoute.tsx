import React, { useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { Brain, Loader2 } from "lucide-react";

interface ProtectedRouteProps {
  children: React.ReactNode;
  onNavigate?: (page: string) => void;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, onNavigate }) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        if (onNavigate) {
          onNavigate("login");
        } else if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      } else if (user && user.onboarding_completed === false) {
        if (onNavigate) {
          onNavigate("onboarding");
        } else if (typeof window !== "undefined") {
          window.location.href = "/onboarding";
        }
      }
    }
  }, [isLoading, isAuthenticated, user, onNavigate]);

  if (isLoading) {
    return (
      <div className="flex h-screen w-screen flex-col items-center justify-center bg-slate-950 text-white font-sans">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl gradient-primary mb-4 shadow-lg shadow-primary/30 animate-pulse">
          <Brain className="h-6 w-6 text-white" />
        </div>
        <div className="flex items-center gap-2 text-sm font-medium text-slate-300">
          <Loader2 className="h-4 w-4 animate-spin text-primary" />
          <span>Verifying LearnMate session...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || (user && user.onboarding_completed === false)) {
    return null;
  }

  return <>{children}</>;
};
