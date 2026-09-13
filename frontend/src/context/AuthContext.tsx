import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { api, setAuthToken, getAuthToken } from "@/lib/api";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  onboarding_completed: boolean;
  avatar_url?: string | null;
  created_at?: string;
}

export interface StudentProfile {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  degree?: string;
  current_term?: string;
  current_goal?: string;
  target_deadline?: string;
  weekly_target_hours?: number;
  learning_style?: string;
  gpa?: number;
  preferences?: Record<string, unknown>;
}

interface AuthContextType {
  user: User | null;
  student: StudentProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string, rememberMe?: boolean) => Promise<{ onboarding_completed: boolean }>;
  demoLoginPrince: () => Promise<{ onboarding_completed: boolean }>;
  register: (payload: {
    full_name: string;
    email: string;
    password: string;
    confirm_password: string;
    terms?: boolean;
  }) => Promise<{ onboarding_completed: boolean }>;
  googleLogin: (payload: {
    email: string;
    full_name?: string;
    avatar_url?: string;
    google_id?: string;
    id_token?: string;
  }) => Promise<{ onboarding_completed: boolean }>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  completeOnboarding: (payload: {
    current_goal?: string;
    target_deadline?: string;
    weekly_target_hours?: number;
    subjects?: string[];
  }) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [student, setStudent] = useState<StudentProfile | null>(null);
  const [token, setToken] = useState<string | null>(getAuthToken());
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const checkSession = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await api.getMe<any>();
      if (data && data.user) {
        setUser(data.user);
        setStudent(data.student);
      } else {
        setUser(null);
        setStudent(null);
        setAuthToken(null);
        setToken(null);
      }
    } catch {
      // Unauthenticated or expired session
      setUser(null);
      setStudent(null);
      setAuthToken(null);
      setToken(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkSession();
  }, [checkSession]);

  const login = async (email: string, password: string, rememberMe: boolean = true) => {
    setIsLoading(true);
    try {
      const res = await api.login<any>({ email, password, remember_me: rememberMe });
      if (res.token) {
        setAuthToken(res.token, rememberMe);
        setToken(res.token);
      }
      setUser(res.user);
      setStudent(res.student);
      return { onboarding_completed: Boolean(res.onboarding_completed) };
    } finally {
      setIsLoading(false);
    }
  };

  const demoLoginPrince = async () => {
    return login("prince.singh@university.edu", "LearnMate2025!", true);
  };

  const register = async (payload: {
    full_name: string;
    email: string;
    password: string;
    confirm_password: string;
    terms?: boolean;
  }) => {
    setIsLoading(true);
    try {
      const res = await api.register<any>(payload);
      if (res.token) {
        setAuthToken(res.token, true);
        setToken(res.token);
      }
      setUser(res.user);
      setStudent(res.student);
      return { onboarding_completed: Boolean(res.onboarding_completed) };
    } finally {
      setIsLoading(false);
    }
  };

  const googleLogin = async (payload: {
    email: string;
    full_name?: string;
    avatar_url?: string;
    google_id?: string;
    id_token?: string;
  }) => {
    setIsLoading(true);
    try {
      const res = await api.googleAuth<any>(payload);
      if (res.token) {
        setAuthToken(res.token, true);
        setToken(res.token);
      }
      setUser(res.user);
      setStudent(res.student);
      return { onboarding_completed: Boolean(res.onboarding_completed) };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch {
      // Ignore network errors on logout
    } finally {
      setAuthToken(null);
      setToken(null);
      setUser(null);
      setStudent(null);
    }
  };

  const completeOnboarding = async (payload: {
    current_goal?: string;
    target_deadline?: string;
    weekly_target_hours?: number;
    subjects?: string[];
  }) => {
    const res = await api.completeOnboarding<any>(payload);
    if (res.user) {
      setUser(res.user);
    }
    if (res.student) {
      setStudent(res.student);
    }
  };

  const refreshUser = async () => {
    await checkSession();
  };

  const value: AuthContextType = {
    user,
    student,
    token,
    isAuthenticated: Boolean(user),
    isLoading,
    login,
    demoLoginPrince,
    register,
    googleLogin,
    logout,
    refreshUser,
    completeOnboarding,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
