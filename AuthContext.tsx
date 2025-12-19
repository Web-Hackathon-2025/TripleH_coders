'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '../lib/api';
import { jwtDecode } from 'jwt-decode';

interface User {
    id: number;
    email: string;
    role: 'CUSTOMER' | 'PROVIDER' | 'ADMIN';
    is_active: bool;
}

interface AuthContextType {
    user: User | null;
    login: (token: string) => void;
    logout: () => void;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const decoded: any = jwtDecode(token);
                // We can also fetch user details from /auth/me if needed
                api.get('/auth/me')
                    .then((res) => {
                        setUser(res.data);
                    })
                    .catch(() => {
                        localStorage.removeItem('token');
                        setUser(null);
                    })
                    .finally(() => setLoading(false));
            } catch (e) {
                localStorage.removeItem('token');
                setLoading(false);
            }
        } else {
            setLoading(false);
        }
    }, []);

    const login = (token: string) => {
        localStorage.setItem('token', token);
        const decoded: any = jwtDecode(token);
        // Fetch full user data
        api.get('/auth/me').then((res) => {
            setUser(res.data);
            if (res.data.role === 'PROVIDER') {
                router.push('/provider/dashboard');
            } else {
                router.push('/');
            }
        });
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);
