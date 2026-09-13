/**
 * Reusable Loading, Error, and Empty state components with rich aesthetics.
 */

import React from "react";
import { AlertCircle, RefreshCw, Inbox, Loader2 } from "lucide-react";

interface LoadingStateProps {
  message?: string;
  className?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = "Loading data from LearnMate autonomous engine...",
  className = "p-8",
}) => (
  <div className={`flex flex-col items-center justify-center text-center space-y-3 ${className}`}>
    <div className="relative flex items-center justify-center h-10 w-10">
      <div className="absolute inset-0 rounded-full border-2 border-indigo-200 animate-ping opacity-25" />
      <Loader2 className="h-6 w-6 animate-spin text-primary" />
    </div>
    <p className="text-xs font-medium text-slate-500 animate-pulse">{message}</p>
  </div>
);

interface ErrorStateProps {
  title?: string;
  message?: string;
  error?: Error | unknown;
  onRetry?: () => void;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = "Connection Error",
  message,
  error,
  onRetry,
  className = "p-6",
}) => {
  const displayMessage =
    message ||
    (error instanceof Error ? error.message : "Failed to load telemetry from backend.");

  return (
    <div className={`rounded-xl border border-rose-200 bg-rose-50/60 p-4 text-center space-y-3 ${className}`}>
      <div className="flex justify-center">
        <div className="h-8 w-8 rounded-full bg-rose-100 flex items-center justify-center text-rose-600">
          <AlertCircle className="h-4 w-4" />
        </div>
      </div>
      <div className="space-y-1">
        <h4 className="text-xs font-bold text-rose-800">{title}</h4>
        <p className="text-xs text-rose-600 max-w-sm mx-auto">{displayMessage}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold bg-rose-600 text-white hover:bg-rose-700 transition-colors shadow-xs cursor-pointer"
        >
          <RefreshCw className="h-3 w-3" />
          Retry Connection
        </button>
      )}
    </div>
  );
};

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = "No records found",
  description = "There are currently no items matching your criteria.",
  actionLabel,
  onAction,
  className = "p-8",
}) => (
  <div className={`flex flex-col items-center justify-center text-center space-y-3 rounded-xl border border-dashed border-slate-200 bg-slate-50/50 p-6 ${className}`}>
    <div className="h-10 w-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-400">
      <Inbox className="h-5 w-5" />
    </div>
    <div className="space-y-1">
      <h4 className="text-xs font-bold text-slate-800">{title}</h4>
      <p className="text-xs text-slate-500 max-w-xs">{description}</p>
    </div>
    {actionLabel && onAction && (
      <button
        onClick={onAction}
        className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors shadow-2xs cursor-pointer"
      >
        {actionLabel}
      </button>
    )}
  </div>
);

/**
 * SkeletonCard — Premium shimmering placeholder for loading cards
 */
export const SkeletonCard: React.FC<{ height?: string; className?: string }> = ({
  height = "h-40",
  className = "",
}) => (
  <div className={`rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs space-y-3 ${className}`}>
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2.5">
        <div className="h-8 w-8 rounded-lg skeleton-shimmer" />
        <div className="space-y-1.5">
          <div className="h-3 w-28 rounded skeleton-shimmer" />
          <div className="h-2 w-16 rounded skeleton-shimmer" />
        </div>
      </div>
      <div className="h-4 w-12 rounded-full skeleton-shimmer" />
    </div>
    <div className={`w-full rounded-xl skeleton-shimmer ${height}`} />
    <div className="flex justify-between items-center pt-2">
      <div className="h-2.5 w-24 rounded skeleton-shimmer" />
      <div className="h-2.5 w-16 rounded skeleton-shimmer" />
    </div>
  </div>
);

