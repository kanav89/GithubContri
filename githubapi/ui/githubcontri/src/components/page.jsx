import React, { useState,useEffect } from "react";
import {Button} from "@nextui-org/button";
import { BarChart } from "@mui/x-charts/BarChart";
import "react-datepicker/dist/react-datepicker.css";
import { Datepicker } from "flowbite-react"; 
import { FormLabel } from '@mui/material';
import "./page.css"
import StreakHistory from "./streakHistory";
// import { Link } from 'react-router-dom';

function Page() {
  const [data, setData] = useState([]);
  const [sd, setSd] = useState("");
  const [ed, setEd] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [username,setUsername] = useState("");

  // useEffect(() => {
  //   const params = new URLSearchParams(window.location.search);
  //   const name = params.get("username");
  //   setUsername(name)
  // })

  const makeList = (startDate, endDate) => {
    const dlist = [];
    const d = new Date(startDate);
    const l = new Date(endDate);

    while (d <= l) {
      dlist.push(new Date(d));
      d.setDate(d.getDate() + 1);
    }

    return dlist;
  };

  const formatDate = (date) => {
    return date.toISOString().split("T")[0];
  };

  const handleSubmit = async () => {
    console.log("Submitting...");
    setLoading(true);
    setError(null);
    setData([]);
    const params = new URLSearchParams(window.location.search);
    const name = params.get("username");
    setUsername(name)
    const access_token = params.get("access_token");
    localStorage.setItem("github_access_token", access_token);
    const apiUrl = `http://localhost:8000/contributions?username=${name}&start_date=${sd}&end_date=${ed}&access_token=${access_token}`;
    console.log("API URL:", apiUrl);

    try {
      const res = await fetch(apiUrl);
      console.log("Response:", res);
      if (!res.ok) {
        alert(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      console.log("Data:", data);

      const datesList = makeList(sd, ed);
      const dataWithDates = datesList.map((date, index) => ({
        date: formatDate(date),
        contribution: data[index] || 0,
      }));

      setData(dataWithDates);
    } catch (error) {
      setError(error.message);
      console.error("Error fetching data:", error);
      console.log("error");
    } finally {
      setLoading(false);
      console.log("Finished submitting");
    }
  };

  const barChartData = data.map((item) => item.contribution);
  const barChartLabels = data.map((item) => item.date);

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">Contribution Analysis</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Description Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">How It Works</h2>
            <p className="text-gray-700 mb-4">
              This tool allows you to analyze your GitHub contributions over a specific time period. 
              Follow these steps to get started:
            </p>
            <ol className="list-decimal list-inside space-y-2 text-gray-700">
              <li>Select a start date and end date using the date pickers on the right.</li>
              <li>Click the "Apply" button to fetch your contribution data.</li>
              <li>View your contributions in a table and a bar chart below.</li>
            </ol>
            <p className="mt-4 text-gray-700">
              This analysis will help you track your coding activity and identify trends in your GitHub contributions.
            </p>
          </div>

          {/* Date Picker Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Select Date Range</h2>
            <div className="space-y-4">
              <div>
                <FormLabel htmlFor="start-date" className="block text-sm font-medium text-gray-700 mb-1">Start Date</FormLabel>
                <Datepicker
                  value={sd}
                  onSelectedDateChanged={(date) => setSd(formatDate(date))}
                  placeholder="Select start date"
                  dateFormat="yyyy-MM-dd"
                  className="w-full"
                />
              </div>
              <div>
                <FormLabel htmlFor="end-date" className="block text-sm font-medium text-gray-700 mb-1">End Date</FormLabel>
                <Datepicker
                  value={ed}
                  onSelectedDateChanged={(date) => setEd(formatDate(date))}
                  placeholder="Select end date"
                  dateFormat="yyyy-MM-dd"
                  className="w-full"
                />
              </div>
              <Button color="primary" onClick={handleSubmit} className="w-full">
                Apply
              </Button>
            </div>
          </div>
        </div>

        {/* Loading and Error States */}
        {loading && (
          <div className="flex flex-col justify-center items-center mt-8">
          <button disabled="" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center">
          <svg aria-hidden="true" role="status" class="inline w-4 h-4 mr-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"></path>
          <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"></path>
          </svg>
          Loading...
          </button>
          </div>
        )}
        {error && <div className="text-red-500 mt-4">{error}</div>}

        {/* Results Section */}
        {data.length > 0 && (
          <div className="mt-12 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Contribution Results</h2>
            <div className="overflow-auto max-h-60 mb-8">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contribution</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {data.map((item, index) => (
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
                series={[{ data: data.map(item => item.contribution) }]}
                height={300}
                xAxis={[{ data: data.map(item => item.date), scaleType: "band" }]}
                yAxis={[{ label: "Contributions" }]}
                colors={["#3b82f6"]}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Page;