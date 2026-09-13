import { useState } from "react";
import { motion } from "framer-motion";
import {
  GraduationCap,
  Play,
  ChevronRight,
  Sparkles,
} from "lucide-react";
import { useResources, type ResourceData } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";
import { VideoPlayerModal, type VideoResourceData } from "@/components/ui/VideoPlayerModal";

interface RecommendedResourcesProps {
  onViewAll?: () => void;
  onOpenResource?: (id: string) => void;
}

// Map resource topics/types to dedicated 3D high-resolution picture assets
const getResourceThumbnail = (res: ResourceData) => {
  const type = (res.type || "").toLowerCase();
  const topic = (res.topic || "").toLowerCase();

  if (type.includes("video") || topic.includes("graph")) {
    return "/res-graph-video.jpg";
  }
  if (type.includes("pdf") || topic.includes("dynamic programming") || topic.includes("dp")) {
    return "/res-dp-notes.jpg";
  }
  if (type.includes("coding") || type.includes("practice")) {
    return "/res-code-drill.jpg";
  }
  return "/res-visualizer.jpg";
};

export function RecommendedResources({
  onViewAll,
  onOpenResource,
}: RecommendedResourcesProps) {
  const { data: resources, isLoading, isError, error, refetch } = useResources();
  const [selectedVideo, setSelectedVideo] = useState<VideoResourceData | null>(null);

  if (isLoading) {
    return (
      <div className="card-3d p-5 shadow-xs">
        <LoadingState message="Loading recommended resources from API..." className="p-4" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="card-3d p-5 shadow-xs">
        <ErrorState
          message={error instanceof Error ? error.message : "Failed to load resources"}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  const items = resources || [];

  if (items.length === 0) {
    return (
      <div className="card-3d p-5 shadow-xs">
        <EmptyState title="No Resources Found" description="No study materials currently recommended." />
      </div>
    );
  }

  const handleCardClick = (res: ResourceData) => {
    const isVideo = (res.type || "").toLowerCase().includes("video");
    if (isVideo) {
      setSelectedVideo({
        id: res.id,
        title: res.title,
        source: res.source,
        topic: res.topic,
        duration_minutes: res.duration_minutes,
        url: res.url,
      });
    } else if (res.url && res.url.startsWith("http")) {
      window.open(res.url, "_blank", "noopener,noreferrer");
    } else {
      onOpenResource?.(res.id);
    }
  };

  return (
    <>
      <div className="card-3d p-5 shadow-xs">
        {/* Header */}
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-100">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-primary shadow-xs">
              <GraduationCap className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-800">
                Recommended for You
              </h3>
              <p className="text-[11px] text-slate-500 font-medium">
                Curated dynamically for your active knowledge gaps
              </p>
            </div>
          </div>

          <button
            onClick={onViewAll}
            className="flex items-center gap-1 text-xs font-medium text-slate-500 hover:text-slate-800 transition-colors cursor-pointer"
          >
            <span>View All</span>
            <ChevronRight className="h-3 w-3 opacity-60" />
          </button>
        </div>

        {/* Grid of Resources with Rich 3D Visual Artwork Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-3.5">
          {items.slice(0, 4).map((res, index) => {
            const resType = (res.type || "").toLowerCase();
            const matchScore = res.match_score ?? 88;
            const matchLabel = res.match_label || "Top Pick";
            const thumbnailSrc = getResourceThumbnail(res);
            const isVideo = resType.includes("video");

            return (
              <motion.div
                key={res.id}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.08 }}
                whileHover={{ y: -4, transition: { duration: 0.2 } }}
                onClick={() => handleCardClick(res)}
                className="cursor-pointer group flex flex-col justify-between rounded-xl border border-slate-200/90 bg-white p-2 sm:p-2.5 hover:border-primary/60 hover:shadow-lg transition-all shadow-xs overflow-hidden"
              >
                <div>
                  {/* Visual Picture Thumbnail Area */}
                  <div className="relative h-24 sm:h-26 w-full rounded-lg overflow-hidden mb-2.5 border border-slate-200/80 bg-slate-950">
                    <img
                      src={thumbnailSrc}
                      alt={res.title}
                      className="h-full w-full object-cover object-center transition-transform duration-500 group-hover:scale-108 brightness-95 group-hover:brightness-105"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent pointer-events-none" />

                    {isVideo ? (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/30 backdrop-blur-md group-hover:bg-primary group-hover:scale-110 transition-all shadow-lg border border-white/40">
                          <Play className="h-4 w-4 text-white fill-white ml-0.5" />
                        </div>
                        <span className="absolute bottom-1.5 right-1.5 rounded bg-black/80 backdrop-blur-xs px-1.5 py-0.5 text-[9px] font-mono font-medium text-white/95 border border-white/10">
                          {res.detail || `${res.duration_minutes}m`}
                        </span>
                      </div>
                    ) : (
                      <div className="absolute top-1.5 left-1.5">
                        <span className="rounded bg-black/60 backdrop-blur-md px-1.5 py-0.5 text-[8.5px] font-bold tracking-wide uppercase text-white/90 border border-white/10">
                          {resType.includes("pdf") ? "PDF Guide" : resType.includes("coding") ? "Practice" : "Tool"}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Title and Source */}
                  <h4 className="text-xs font-bold text-slate-800 line-clamp-1 group-hover:text-primary transition-colors">
                    {res.title}
                  </h4>
                  <p className="text-[11px] text-slate-500 mt-0.5 truncate">
                    {res.source || res.topic}
                  </p>
                </div>

                {/* Bottom area: Match Score & Action Button */}
                <div className="mt-2.5 pt-2 border-t border-slate-100 flex flex-col gap-1.5">
                  <div className="flex items-center justify-between px-0.5">
                    <span className="text-[10px] font-medium text-slate-400">
                      Match
                    </span>
                    <span className="text-[11px] font-extrabold text-emerald-600 bg-emerald-50/90 px-1.5 py-0.2 rounded border border-emerald-200/70">
                      {matchScore}%
                    </span>
                  </div>

                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCardClick(res);
                    }}
                    className="w-full flex items-center justify-center gap-1 rounded-lg bg-indigo-50 hover:bg-primary hover:text-white border border-indigo-200/80 py-1.5 px-1 text-[10px] font-semibold text-primary transition-all shadow-2xs group/btn cursor-pointer"
                  >
                    {isVideo ? (
                      <>
                        <Play className="h-2.5 w-2.5 fill-current flex-shrink-0" />
                        <span>Watch Video</span>
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-2.5 w-2.5 flex-shrink-0 text-primary group-hover/btn:text-white" />
                        <span className="truncate">{matchLabel}</span>
                      </>
                    )}
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Video Player Modal */}
      <VideoPlayerModal
        isOpen={Boolean(selectedVideo)}
        resource={selectedVideo}
        onClose={() => setSelectedVideo(null)}
      />
    </>
  );
}

