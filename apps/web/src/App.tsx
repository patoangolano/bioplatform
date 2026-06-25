import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, ProtectedRoute } from "./lib/auth";
import AppShell from "./components/AppShell";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Submit from "./pages/Submit";
import Sequences from "./pages/Sequences";
import SequenceDetail from "./pages/SequenceDetail";
import Blast from "./pages/Blast";
import Admin from "./pages/Admin";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route
            element={
              <ProtectedRoute>
                <AppShell />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<Dashboard />} />
            <Route path="/submit" element={<Submit />} />
            <Route path="/sequences" element={<Sequences />} />
            <Route path="/sequences/:id" element={<SequenceDetail />} />
            <Route path="/blast" element={<Blast />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/404" element={<NotFound />} />
            <Route path="*" element={<Navigate to="/404" replace />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
