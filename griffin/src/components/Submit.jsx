import { useNavigate } from 'react-router-dom';

const Submit = () => {
    const navigate = useNavigate();
  
    return (
      <div className="min-h-screen bg-gray-900">
        <header className="bg-green-400 p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold">Welcome User1</h1>
            <button
              onClick={() => navigate('/')}
              className="text-gray-900 hover:text-gray-700 font-semibold"
            >
              Logout
            </button>
          </div>
        </header>
        <main className="container mx-auto p-8">
          <h2 className="text-4xl text-white mb-12 text-center">Submit Footage</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <button
              className="p-8 bg-green-400 rounded-lg hover:bg-green-500 transition duration-200"
            >
              <div className="flex flex-col items-center space-y-4">
                <span className="text-xl font-semibold">Use Live Feed</span>
                <svg className="w-12 h-12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </div>
            </button>
            <button
              className="p-8 bg-green-400 rounded-lg hover:bg-green-500 transition duration-200"
            >
              <div className="flex flex-col items-center space-y-4">
                <span className="text-xl font-semibold">Upload sample video</span>
                <svg className="w-12 h-12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
            </button>
          </div>
        </main>
      </div>
    );
  };
  export default Submit;
  