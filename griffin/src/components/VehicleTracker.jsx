import React, { useState } from 'react';
import { CalendarDays, Clock, Camera } from 'lucide-react';
import video from "../d72af08b.mp4"
const VehicleTracker = () => {
  const [vehicles, setVehicles] = useState([]);
  const [date, setDate] = useState('');
  const [inTime, setInTime] = useState('');
  const [outTime, setOutTime] = useState('');
  const [isVideoActive, setIsVideoActive] = useState(true);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-green-400 p-4 flex justify-between items-center">
        <h1 className="text-gray-800 text-xl font-semibold">Welcome User1</h1>
        <button className="text-gray-800 hover:text-gray-600">Logout</button>
      </header>

      <div className="container mx-auto p-6 flex flex-col md:flex-row gap-8">
        {/* Left side - Video Feed */}
        <div className="md:w-1/2">
          <div className="bg-gray-800 rounded-lg overflow-hidden shadow-lg border border-gray-700">
            {/* Video Container */}
            <div className="aspect-video relative bg-black rounded-lg overflow-hidden">
              {isVideoActive ? (
                <div className="absolute inset-0 flex items-center justify-center">
                  {/* Video element to play an mp4 file */}
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
            <div className="p-4 border-t border-gray-700 flex gap-4">
              <button
                onClick={() => setIsVideoActive(!isVideoActive)}
                className="px-4 py-2 bg-green-400 text-gray-800 rounded-lg 
                  hover:bg-green-500 transition-all duration-300 flex items-center gap-2"
              >
                <Camera size={20} />
                {isVideoActive ? 'Stop Feed' : 'Start Feed'}
              </button>
              
            </div>
          </div>
        </div>

        {/* Right side - Form */}
        <div className="md:w-1/2 space-y-6">
          {/* Date Input */}
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800 rounded-lg border border-gray-700 focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none text-white"
                />
                <CalendarDays className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          {/* Time Input Buttons */}
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <input
                  type="time"
                  value={inTime}
                  onChange={(e) => setInTime(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800 rounded-lg border border-gray-700 focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none text-white"
                  placeholder="Enter In-time"
                />
                <Clock className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
              </div>
            </div>
            <div className="flex-1">
              <div className="relative">
                <input
                  type="time"
                  value={outTime}
                  onChange={(e) => setOutTime(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800 rounded-lg border border-gray-700 focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none text-white"
                  placeholder="Enter Out-time"
                />
                <Clock className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          {/* Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="px-4 py-2 text-left">Vehicle Number</th>
                  <th className="px-4 py-2 text-left">In-time</th>
                  <th className="px-4 py-2 text-left">Out-time</th>
                </tr>
              </thead>
              <tbody>
                {vehicles.map((vehicle, index) => (
                  <tr key={index} className="border-b border-gray-700">
                    <td className="px-4 py-2">
                      <input
                        type="text"
                        className="w-full bg-gray-800 rounded px-2 py-1 border border-gray-700"
                        placeholder="Enter number"
                      />
                    </td>
                    <td className="px-4 py-2">
                      <input
                        type="time"
                        className="w-full bg-gray-800 rounded px-2 py-1 border border-gray-700"
                      />
                    </td>
                    <td className="px-4 py-2">
                      <input
                        type="time"
                        className="w-full bg-gray-800 rounded px-2 py-1 border border-gray-700"
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button
              className="mt-4 px-4 py-2 bg-green-400 text-gray-800 rounded-lg hover:bg-green-500 transition-all duration-300"
            >
              Search
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehicleTracker;
