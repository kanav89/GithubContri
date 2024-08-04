import React, { useState } from "react";
import { Button, Label } from "flowbite-react";
import { BarChart } from "@mui/x-charts/BarChart";
import "react-datepicker/dist/react-datepicker.css";
import { Datepicker } from "flowbite-react";

function Main() {
  const [data, setData] = useState([]);
  const [sd, setSd] = useState("");
  const [ed, setEd] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
    const access_token = params.get("access_token");
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
    <div className="min-h-full">
      <header className="bg-black text-white text-primary-foreground px-4 py-3 font-bold">
        Main Header
      </header>
      <div className="flex flex-col justify-center items-center h-screen">
        <div className="mt-36">
          <header className="bg-black text-white text-primary-foreground px-4 py-3 font-bold">
            Date Picker
          </header>
          <div className="grid gap-4 w-full max-w-md p-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="start-date">Start Date</Label>
                <div className="relative">
                  <Datepicker
                    value={sd}
                    onSelectedDateChanged={(date) => {
                      setSd(formatDate(date));
                    }}
                    placeholder="Select start date"
                    dateFormat="yyyy-MM-dd"
                  />
                </div>
              </div>
              <div className="space-y-1">
                <Label htmlFor="end-date">End Date</Label>
                <div className="relative">
                  <Datepicker
                    value={ed}
                    onSelectedDateChanged={(date) => {
                      setEd(formatDate(date));
                    }}
                    placeholder="Select end date"
                    dateFormat="yyyy-MM-dd"
                  />
                </div>
              </div>
            </div>
            <div className="grid gap-2">
              <p className="text-muted-foreground">
                Select a start and end date to filter your data.
              </p>
              <Button onClick={handleSubmit} className="w-full">
                Apply
              </Button>
            </div>
            {loading && <div>Loading...</div>}
            {error && <div className="text-red-500">{error}</div>}
          </div>
          {data.length > 0 && (
            <div className="mt-8 w-full">
              <h2 className="font-bold mt-4">Contributions</h2>
              <div className="overflow-auto max-h-60">
                <table className="bg-white w-full">
                  <thead className="sticky top-0 bg-white">
                    <tr>
                      <th className="py-2 border">Date</th>
                      <th className="py-2 border">Contribution</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.map((item, index) => (
                      <tr key={index} className="text-center">
                        <td className="py-2 border">{item.date}</td>
                        <td className="py-2 border">{item.contribution}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="">
                <BarChart
                  series={[{ data: barChartData }]}
                  height={290}
                  xAxis={[{ data: barChartLabels, scaleType: "band" }]}
                  // margin={{ top: 10, bottom: 30, left: 40, right: 10 }}
                />
              </div>
            </div>
          )}
        </div>
        <footer className="bg-muted text-muted-foreground  text-sm ">
          This will return a list of contributions between any selected dates.
        </footer>
      </div>
    </div>
  );
}

export default Main;
