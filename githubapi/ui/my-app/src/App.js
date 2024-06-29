// App.js (or your main component)
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/login";
import Main from "./components/main";

function App() {
  return (
    <Router>
      <div className="App">
        {/* Your routes go inside Routes */}
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/main" element={<Main />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
