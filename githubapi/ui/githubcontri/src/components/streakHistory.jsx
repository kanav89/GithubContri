import React, { useState, useEffect } from 'react';
import { BarChart } from "@mui/x-charts/BarChart";

function StreakHistory() {
  const [streakData, setStreakData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStreakHistory = async () => {
      const params = new URLSearchParams(window.location.search);
      const username = params.get("username");
      const apiUrl = `http://localhost:8000/streak-history?username=${username}`;

      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setStreakData(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStreakHistory();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!streakData) return null;

  const {
    Streak_for_which_data_is_shown,
    current_streak,
    longest_streak_between_selected_dates,
    last_contribution_date,
    longest_streak_since_joining
  } = streakData;

  // Convert the object to an array of objects
  const chartData = Object.entries(Streak_for_which_data_is_shown).map(([date, contribution]) => ({
    date,
    contribution
  }));

  return (
    <div className="container mx-auto px-4 py-8 bg-gray-100 min-h-screen">
      <h2 className="text-4xl font-bold mb-4 text-center text-gray-800">Streak History</h2>
      
      <div className="bg-white shadow-lg rounded-lg p-8 mb-8">
        <h3 className="text-2xl font-semibold mb-4 text-center text-gray-700">Current Streak</h3>
        <p className="text-6xl font-bold text-center text-blue-600">{current_streak} days</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard title="Longest Streak (Selected Dates)" value={`${longest_streak_between_selected_dates} days`} />
        <StatCard title="Last Contribution (Selected Dates)" value={last_contribution_date || 'N/A'} />
        <StatCard title="Longest Streak Since Joining" value={`${longest_streak_since_joining} days`} />
      </div>

      {chartData.length > 0 && (
        <div className="mt-12 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">Most Recent Selected Dates</h2>
          <div className="overflow-auto max-h-60 mb-8">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contribution</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {chartData.map((item, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap">{item.date}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{item.contribution}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-8">
            <h3 className="text-xl font-semibold mb-4">Contribution Chart</h3>
            <BarChart
              series={[{ data: chartData.map(item => item.contribution) }]}
              height={300}
              xAxis={[{ data: chartData.map(item => item.date), scaleType: "band" }]}
              yAxis={[{ label: "Contributions" }]}
              colors={["#3b82f6"]}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ title, value }) {
  return (
    <div className="bg-white shadow-lg rounded-lg p-6 transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-2 text-gray-700">{title}</h3>
      <p className="text-3xl font-bold text-blue-600">{value}</p>
    </div>
  );
}

function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="loader">
        <svg className="animate-spin h-12 w-12 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span className="ml-3 text-xl font-semibold text-gray-700"></span>
      </div>
    </div>
  );
}

function ErrorMessage({ error }) {
  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow-md" role="alert">
        <p className="font-bold">Error</p>
        <p>{error}</p>
      </div>
    </div>
  );
}

export default StreakHistory;