
import './index.css';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Submit from './components/Submit';
import VehicleQueryScreen from "./components/VehicleQueryScreen";
import VehicleEntryScreen from './components/VehicleEntryScreen';
import VehicleTracker from './components/VehicleTracker';
function App() {
  return (
    <div className="App">
       <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/submit" element={<Submit />} />
        <Route path = "/VechileQuery" element ={<VehicleQueryScreen />} />
        <Route path = "/VechileScreen" element ={<VehicleEntryScreen />} />
        <Route path = "/VehicleTracker" element ={<VehicleTracker />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
