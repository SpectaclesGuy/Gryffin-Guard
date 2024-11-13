import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Search } from 'lucide-react';
import video from "../d72af08b.mp4"
const VehicleEntryScreen = () => {
  const navigate = useNavigate();
  const [isVideoActive, setIsVideoActive] = useState(true);
  
  // Sample data - replace with your actual data
  const vehicleRecords = [
    { number: 'ABC123', inTime: '09:00 AM', outTime: '--' },
    { number: 'XYZ789', inTime: '10:30 AM', outTime: '02:15 PM' },
  ];

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
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Video Box */}
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 shadow-2xl border border-white/10">
            <div className="aspect-video relative bg-black rounded-lg overflow-hidden">
              {isVideoActive ? (
                <div className="absolute inset-0 flex items-center justify-center">
                  {/* Video placeholder - replace with actual video component */}
                  <video
                    src={video} // replace with your video file path
                    controls
                    autoPlay
                    loop
                    muted
                    className="w-full h-full object-cover"
                  />
                </div>
              ) : (
                <div className="absolute inset-0 flex items-center justify-center text-gray-500">
                  No video feed available
                </div>
              )}
            </div>
            
            {/* Video Controls */}
            <div className="mt-4 flex gap-4">
              <button
                onClick={() => setIsVideoActive(!isVideoActive)}
                className="px-4 py-2 bg-green-400 text-white rounded-lg 
                  hover:bg-green-500 transition-all duration-300 flex items-center gap-2"
              >
                <Camera size={20} />
                {isVideoActive ? 'Stop Feed' : 'Start Feed'}
              </button>
              
            </div>
          </div>

          {/* Vehicle Entry Form */}
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 shadow-2xl border border-white/10">
            <h2 className="text-2xl font-semibold text-white mb-8 text-center">
              Enter Vehicle Number
            </h2>
            
            <div className="space-y-8">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Enter Vehicle Number"
                  className="w-full px-6 py-4 bg-white/90 rounded-lg text-gray-800 
                    placeholder-gray-400 focus:outline-none focus:ring-2 
                    focus:ring-green-400 transition-all duration-300"
                />
                <button
                  className="absolute right-2 top-2 px-4 py-2 bg-green-400 
                    text-white rounded-lg hover:bg-green-500 
                    transition-all duration-300 flex items-center gap-2"
                >
                  <Search size={20} />
                  Search
                </button>
              </div>

              {/* Vehicle Records Table */}
              <div className="overflow-hidden rounded-lg">
                <table className="w-full">
                  <thead>
                    <tr className="bg-white/20">
                      <th className="px-6 py-4 text-left text-sm font-semibold text-white">
                        Vehicle Number
                      </th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-white">
                        In-time
                      </th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-white">
                        Out-time
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {vehicleRecords.map((record, index) => (
                      <tr 
                        key={index}
                        className="border-t border-white/10 hover:bg-white/5 transition-colors duration-200"
                      >
                        <td className="px-6 py-4 text-sm text-white">
                          {record.number}
                        </td>
                        <td className="px-6 py-4 text-sm text-white">
                          {record.inTime}
                        </td>
                        <td className="px-6 py-4 text-sm text-white">
                          {record.outTime}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehicleEntryScreen;