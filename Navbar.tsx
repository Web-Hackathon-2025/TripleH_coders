'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';

export function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav className="border-b bg-white">
            <div className="flex h-16 items-center px-4 container mx-auto">
                <Link href="/" className="font-bold text-xl mr-6">
                    Karigar
                </Link>
                <div className="flex items-center space-x-4 lg:space-x-6 mx-6">
                    <Link href="/services" className="text-sm font-medium transition-colors hover:text-black text-gray-500">
                        Browse Services
                    </Link>
                    {user?.role === 'CUSTOMER' && (
                        <Link href="/my-bookings" className="text-sm font-medium transition-colors hover:text-black text-gray-500">
                            My Bookings
                        </Link>
                    )}
                    {user?.role === 'PROVIDER' && (
                        <Link href="/provider/dashboard" className="text-sm font-medium transition-colors hover:text-black text-gray-500">
                            Provider Dashboard
                        </Link>
                    )}
                </div>
                <div className="ml-auto flex items-center space-x-4">
                    {user ? (
                        <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-700">Hi, {user.email}</span>
                            <button onClick={logout} className="text-sm font-medium text-red-500 hover:text-red-600">
                                Logout
                            </button>
                        </div>
                    ) : (
                        <div className="space-x-2">
                            <Link href="/login" className="text-sm font-medium text-gray-700 hover:text-black">
                                Login
                            </Link>
                            <Link href="/register" className="text-sm font-medium text-white bg-black px-4 py-2 rounded-md hover:bg-gray-800">
                                Register
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
}
