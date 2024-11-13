import React from 'react';
import { useNavigate } from 'react-router-dom';

const Submit = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800">
      {/* Header */}
      <div className="bg-green-400 p-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold text-white tracking-wide">
            Welcome User1
          </h1>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 text-white border border-white rounded-lg 
              hover:bg-white hover:text-green-400 transition-all duration-300 ease-in-out"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 h-[calc(100vh-5rem)] flex flex-col items-center justify-center">
        <h2 className="text-3xl font-bold text-white mb-12 tracking-wide">
          Submit Footage
        </h2>
        
        <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Live Feed Button */}
          <div className="transform  transition-all duration-300">
            <button className="w-full h-full bg-white/10 backdrop-blur-lg rounded-xl p-8 
              border border-white/10 shadow-2xl hover:bg-white/20 
              transition-all duration-300 group">
              <div className="flex flex-col items-center space-y-6">
                <span className="text-xl font-semibold text-white group-hover:scale-105 
                  transition-transform duration-300">
                  Use Live Feed
                </span>
                <svg className="w-16 h-16 text-white group-hover:scale-110 
                  transition-transform duration-300" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="1.5"
                >
                  <circle cx="12" cy="12" r="10"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </div>
            </button>
          </div>

          {/* Upload Video Button */}
          <div className="transform hover:scale-102 transition-all duration-300">
            <button 
              onClick={() => navigate('/VechileQuery')}
              className="w-full h-full bg-white/10 backdrop-blur-lg rounded-xl p-8 
                border border-white/10 shadow-2xl hover:bg-white/20 
                transition-all duration-300 group"
            >
              <div className="flex flex-col items-center space-y-6">
                <span className="text-xl font-semibold text-white group-hover:scale-105 
                  transition-transform duration-300">
                  Upload sample video
                </span>
                <svg className="w-16 h-16 text-white group-hover:scale-110 
                  transition-transform duration-300" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="1.5"
                >
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Submit;