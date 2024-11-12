import {  useNavigate } from 'react-router-dom';

const Dashboard = () => {
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
          <h2 className="text-4xl text-white mb-12 text-center">Dashboard</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <button
              onClick={() => navigate('/submit')}
              className="p-8 bg-green-400 rounded-lg hover:bg-green-500 transition duration-200 text-xl font-semibold"
            >
              Submit Footage
            </button>
            <button
              className="p-8 bg-green-400 rounded-lg hover:bg-green-500 transition duration-200 text-xl font-semibold"
            >
              Query DB
            </button>
          </div>
        </main>
      </div>
    );
  };
export default Dashboard;