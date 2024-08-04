// App.js (or your main component)
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/login.jsx";
import Page from "./components/page.jsx";
import StreakHistory from "./components/streakHistory.jsx";
import "./App.css"
import Layout from "./components/Layout.jsx";
import Goals from "./components/goals.jsx"
function App() {

  const [username, setUsername] = React.useState("");
  const [access_token,setAccessToken] = React.useState("");

  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const name = params.get("username");
    const access_token = params.get("access_token")
    setAccessToken(access_token);
    setUsername(name);
  }, []);
  return (

    <Router>
      <Layout username={username} accessToken={access_token}>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/page" element={<Page />} />
          <Route path="/streakHistory" element={<StreakHistory />} />
          <Route path="/goals" element={<Goals />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
