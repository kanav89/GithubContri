// App.js (or your main component)
import React from "react";
import { useEffect,useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/login.jsx";
import Page from "./components/page.jsx";
import StreakHistory from "./components/streakHistory.jsx";
import "./App.css"
import Layout from "./components/Layout.jsx";
import Goal from "./components/goals.jsx"

function App() {

  const [username, setUsername] = useState(() => localStorage.getItem("username") || "");
  const [access_token, setAccessToken] = useState(() => localStorage.getItem("accessToken") || "");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const name = params.get("username");
    const token = params.get("access_token");

    if (name) {
      localStorage.setItem("username", name);
      localStorage.setItem("accessToken", token);
      setUsername(name);
      setAccessToken(token);
      // window.history.replaceState({}, document.title, "/page");
    }
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  
  return (

    <Router>
      <Layout username={username} accessToken={access_token}>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/page" element={<Page />} />
          <Route path="/streakHistory" element={<StreakHistory />} />
          <Route path="/goals" element={<Goal username={username}  />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
