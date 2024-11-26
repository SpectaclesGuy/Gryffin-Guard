import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Login Component
const Login = () => {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({ username: 'Arindam', password: 'sharma' });

  const handleLogin = (e) => {
    e.preventDefault();
    if (credentials.username && credentials.password) {
      navigate('/Submit');
    }
  };

  return (
    <div className="relative h-screen w-full bg-gray-900 flex items-center justify-center p-8">
  {/* Blurred Background Layer */}
  <div
    style={{
      backgroundImage: 'url(https://images.unsplash.com/photo-1668711495033-2aceccc63054?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      filter: 'blur(7px)',
    }}
    className="absolute inset-0 z-0"
  ></div>

  
  <div className="relative z-10 w-full max-w-3xl space-y-8 bg-opacity-70 p-8 rounded-lg">
    <div className="text-center max-w-3xl">
      <h2 className="text-9xl max-w-3xl font-cursive text-accent text-white mb-8 head">
        Griffin Guard
      </h2>
      <p className="text-white text-xl mb-8">Please enter your credentials</p>
    </div>
    <form onSubmit={handleLogin} className="flex flex-col justify-center items-center space-y-6">
      <div className="w-full max-w-sm">
        <input
          type="text"
          placeholder="User Name"
          className="w-full px-4 py-3 rounded-lg bg-dark border border-muted text-muted focus:outline-none focus:border-primary"
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
        />
      </div>
      <div className="w-full max-w-sm">
        <input
          type="password"
          placeholder="Password"
          className="w-full px-4 py-3 rounded-lg bg-dark border border-muted text-muted focus:outline-none focus:border-primary"
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        />
      </div>
      <button
        type="submit"
        className="w-full max-w-sm bg-primary hover:bg-accent text-white font-bold py-3 px-4 rounded-lg transition duration-200">
        Login
      </button>
    </form>
  </div>
</div>
  );
};

export default Login;