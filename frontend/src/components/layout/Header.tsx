'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">G</span>
              </div>
              <span className="text-xl font-bold text-gray-900">
                Green Guru Sports
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link 
              href="/predictions" 
              className="text-gray-600 hover:text-gray-900 font-medium"
            >
              Predictions
            </Link>
            <Link 
              href="/performance" 
              className="text-gray-600 hover:text-gray-900 font-medium"
            >
              Performance
            </Link>
            <Link 
              href="/about" 
              className="text-gray-600 hover:text-gray-900 font-medium"
            >
              About
            </Link>
            <Link 
              href="/subscribe" 
              className="bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              Subscribe
            </Link>
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600 hover:text-gray-900"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t">
              <Link 
                href="/predictions" 
                className="block px-3 py-2 text-gray-600 hover:text-gray-900 font-medium"
              >
                Predictions
              </Link>
              <Link 
                href="/performance" 
                className="block px-3 py-2 text-gray-600 hover:text-gray-900 font-medium"
              >
                Performance
              </Link>
              <Link 
                href="/about" 
                className="block px-3 py-2 text-gray-600 hover:text-gray-900 font-medium"
              >
                About
              </Link>
              <Link 
                href="/subscribe" 
                className="block px-3 py-2 bg-green-600 text-white rounded-lg font-medium mt-2"
              >
                Subscribe
              </Link>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}