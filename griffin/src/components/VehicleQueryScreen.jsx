import React from 'react';
import { useNavigate } from 'react-router-dom';

const VehicleQueryScreen = () => {
    const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800">
      {/* Header */}
      <div className="bg-green-400 p-4 ">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold text-white tracking-wide">
            Welcome User1
          </h1>
          <button className="px-4 py-2 text-white border border-white rounded-lg 
            hover:bg-white hover:text-green-400 transition-all duration-300 shadow-lg">
            Logout
          </button>
        </div>
      </div>

      {/* Main Content - Centered */}
      <div className="container mx-auto px-4 h-[calc(100vh-5rem)] flex items-center justify-center">
        <div className="w-full max-w-md transform hover:scale-102 transition-all duration-300">
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 shadow-2xl border border-white/10">
            <h2 className="text-2xl font-semibold text-white mb-8 text-center">
              Nature of query
            </h2>
            <div className="space-y-4">
              <button onClick={()=> navigate("/VechileScreen")} className="w-full py-4 px-6 bg-white/90 rounded-lg text-gray-800 
                hover:bg-white hover:shadow-lg transform hover:-translate-y-0.5 
                transition-all duration-300 font-medium">
                Vehicle related
              </button>
              <button  onClick={()=> navigate("/VehicleTracker")} className="w-full py-4 px-6 bg-white/90 rounded-lg text-gray-800 
                hover:bg-white hover:shadow-lg transform hover:-translate-y-0.5 
                transition-all duration-300 font-medium">
                Specific period
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehicleQueryScreen;