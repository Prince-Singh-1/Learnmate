/**
 * Footer — Platform footer matching reference image. (Light theme)
 */

import { Brain, Heart } from "lucide-react";

export function Footer() {
  return (
    <footer className="mt-12 border-t border-slate-200/80 pt-8 pb-10">
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Left branding */}
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl gradient-primary shadow-xs">
            <Brain className="h-4 w-4 text-white" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-slate-800 tracking-tight">
              LearnMate
            </h4>
            <p className="text-[10px] text-slate-500 font-medium">
              Learn Smarter. Grow Bigger.
            </p>
          </div>
        </div>

        {/* Center links & socials */}
        <div className="flex flex-col sm:flex-row items-center gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-4 font-medium">
            <a href="#about" className="hover:text-slate-900 transition-colors">
              About
            </a>
            <a href="#privacy" className="hover:text-slate-900 transition-colors">
              Privacy
            </a>
            <a href="#contact" className="hover:text-slate-900 transition-colors">
              Contact
            </a>
            <a href="#help" className="hover:text-slate-900 transition-colors">
              Help
            </a>
          </div>

          <div className="flex items-center gap-3 border-t sm:border-t-0 sm:border-l border-slate-200 pt-2 sm:pt-0 sm:pl-4">
            {/* GitHub */}
            <a href="#" className="text-slate-400 hover:text-slate-800 transition-colors" title="GitHub">
              <svg className="h-4 w-4 fill-currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
              </svg>
            </a>
            {/* LinkedIn */}
            <a href="#" className="text-slate-400 hover:text-slate-800 transition-colors" title="LinkedIn">
              <svg className="h-4 w-4 fill-currentColor" viewBox="0 0 24 24">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.64 1.64 0 1 0 0-3.28 1.64 1.64 0 0 0 0 3.28m1.39 9.74v-8.37H5.07v8.37h2.78z" />
              </svg>
            </a>
            {/* Twitter */}
            <a href="#" className="text-slate-400 hover:text-slate-800 transition-colors" title="Twitter">
              <svg className="h-4 w-4 fill-currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
              </svg>
            </a>
            {/* YouTube */}
            <a href="#" className="text-slate-400 hover:text-slate-800 transition-colors" title="YouTube">
              <svg className="h-4 w-4 fill-currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
              </svg>
            </a>
          </div>
        </div>

        {/* Right copyright */}
        <div className="flex items-center gap-1.5 text-xs text-slate-500">
          <span>Made with</span>
          <Heart className="h-3.5 w-3.5 text-red-500 fill-red-500 inline" />
          <span>for learners everywhere.</span>
        </div>
      </div>
    </footer>
  );
}
