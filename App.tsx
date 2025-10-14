import React, { useState } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ProfessorDashboard from './pages/professor/ProfessorDashboard';
import AlunoDashboard from './pages/aluno/AlunoDashboard';

export interface User {
  role: 'aluno' | 'professor';
  name: string;
}

function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  const handleLogin = (user: User) => {
    setCurrentUser(user);
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={
          currentUser?.role === 'professor' ? <Navigate to="/professor" /> :
          currentUser?.role === 'aluno' ? <Navigate to="/aluno" /> :
          <LandingPage onLogin={handleLogin} />
        } />
        
        <Route path="/professor/*" element={
          currentUser?.role === 'professor' ? <ProfessorDashboard user={currentUser} onLogout={handleLogout} /> : <Navigate to="/" />
        } />

        <Route path="/aluno/*" element={
          currentUser?.role === 'aluno' ? <AlunoDashboard user={currentUser} onLogout={handleLogout} /> : <Navigate to="/" />
        } />

      </Routes>
    </HashRouter>
  );
}

export default App;