import { useState } from "react";
import { motion } from "framer-motion";
import {
  BookOpen,
  Search,
  Play,
  Sparkles,
  ExternalLink,
} from "lucide-react";
import { useResources, type ResourceData } from "@/hooks/useLearnMate";
import { LoadingState, ErrorState, EmptyState } from "@/components/ui/states";
import { VideoPlayerModal, type VideoResourceData } from "@/components/ui/VideoPlayerModal";

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

export function ResourcesPage() {
  const [activeTab, setActiveTab] = useState("all");
  const [search, setSearch] = useState("");
  const [selectedVideo, setSelectedVideo] = useState<VideoResourceData | null>(null);
  const { data: resources, isLoading, isError, error, refetch } = useResources();

  if (isLoading) {
    return (
      <div className="card-3d p-8 shadow-xs">
        <LoadingState message="Connecting to Resources API..." />
      </div>
    );
  }

  if (isError) {
    return (
      <ErrorState
        message={error instanceof Error ? error.message : "Failed to load resources"}
        onRetry={() => refetch()}
      />
    );
  }

  const items = resources || [];

  const filtered = items.filter((r) => {
    const rType = (r.type || "").toLowerCase();
    const matchesTab =
      activeTab === "all" ||
      (activeTab === "video" && rType.includes("video")) ||
      (activeTab === "pdf" && (rType.includes("pdf") || rType.includes("article"))) ||
      (activeTab === "practice" && (rType.includes("practice") || rType.includes("quiz") || rType.includes("code"))) ||
      (activeTab === "tool" && rType.includes("interactive"));
    const matchesSearch =
      r.title.toLowerCase().includes(search.toLowerCase()) ||
      (r.topic || "").toLowerCase().includes(search.toLowerCase());
    return matchesTab && matchesSearch;
  });

  const handleResourceClick = (res: ResourceData) => {
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
    }
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        {/* Header */}
        <div className="card-3d flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 shadow-xs">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-xs font-semibold text-primary mb-2 shadow-2xs">
              <BookOpen className="h-3.5 w-3.5" />
              AI Matched Learning Materials
            </div>
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Curated Resources</h2>
            <p className="text-xs text-slate-500 mt-1">
              Hand-picked video lectures, problem sets, and cheat sheets matched to your gaps. Click any video to play instantly.
            </p>
          </div>

          {/* Search */}
          <div className="relative w-full sm:w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search topic or format..."
              className="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 pl-9 pr-3 text-xs text-slate-800 placeholder-slate-400 outline-none focus:bg-white focus:border-primary transition-colors shadow-2xs"
            />
          </div>
        </div>

        {/* Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {["all", "video", "pdf", "practice", "tool"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`rounded-xl px-4 py-2 text-xs font-semibold capitalize transition-all cursor-pointer ${
                activeTab === tab
                  ? "gradient-primary text-white shadow-md shadow-primary/20"
                  : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900 shadow-2xs"
              }`}
            >
              {tab === "all" ? "All Formats" : tab}
            </button>
          ))}
        </div>

        {/* Resources Grid */}
        {filtered.length === 0 ? (
          <EmptyState title="No matching resources" description="Try clearing your search query or choosing another format filter." />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {filtered.map((res, index) => {
              const rType = (res.type || "").toLowerCase();
              const matchScore = res.match_score ?? 90;
              const thumbnailSrc = getResourceThumbnail(res);
              const isVideo = rType.includes("video");

              return (
                <motion.div
                  key={res.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ y: -4, transition: { duration: 0.2 } }}
                  onClick={() => handleResourceClick(res)}
                  className="card-3d p-4 flex flex-col justify-between hover:border-indigo-300 hover:shadow-lg transition-all group cursor-pointer shadow-xs overflow-hidden"
                >
                  <div>
                    {/* Visual Picture Thumbnail */}
                    <div className="relative h-36 w-full rounded-xl overflow-hidden mb-3 border border-slate-200/80 bg-slate-950 flex items-center justify-center">
                      <img
                        src={thumbnailSrc}
                        alt={res.title}
                        className="h-full w-full object-cover object-center transition-transform duration-500 group-hover:scale-108 brightness-95 group-hover:brightness-105"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/25 to-transparent pointer-events-none" />

                      {isVideo && (
                        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/30 backdrop-blur-md text-white shadow-xl group-hover:bg-primary group-hover:scale-110 transition-all border border-white/50">
                          <Play className="h-5 w-5 fill-white ml-0.5" />
                        </div>
                      )}

                      <span className="absolute bottom-2 right-2 rounded bg-black/80 backdrop-blur-xs px-2 py-0.5 text-[10px] font-mono text-white/95 border border-white/10">
                        {res.detail || `${res.duration_minutes}m`}
                      </span>
                    </div>

                    <h4 className="text-sm font-bold text-slate-900 group-hover:text-primary transition-colors line-clamp-2">
                      {res.title}
                    </h4>
                    <p className="text-xs text-slate-500 mt-1">{res.source || res.topic}</p>
                  </div>

                  <div className="pt-3 mt-3 border-t border-slate-100 flex items-center justify-between">
                    <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-md border border-indigo-100">
                      <Sparkles className="h-3 w-3 text-primary" />
                      <span>{matchScore}% Match</span>
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleResourceClick(res);
                      }}
                      className="flex items-center gap-1 text-xs font-bold text-primary hover:underline cursor-pointer"
                    >
                      {isVideo ? "Play Video" : "Open"} <ExternalLink className="h-3 w-3" />
                    </button>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </motion.div>

      {/* Embedded Video Player Modal */}
      <VideoPlayerModal
        isOpen={Boolean(selectedVideo)}
        resource={selectedVideo}
        onClose={() => setSelectedVideo(null)}
      />
    </>
  );
}


