import React, { useState, useRef } from "react";
import { Button, TextInput, Progress, Label } from "flowbite-react";
// import { LineChart } from "@mui/x-charts";
// import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { Datepicker, Checkbox } from "flowbite-react";
import Login from "./login.js";
//import { parseISO} from 'date-fns';
function Main() {
  const [data, setData] = useState([]);
  const [name, setName] = useState("");
  const [token, setToken] = useState("");
  const [sd, setSd] = useState("");
  const [ed, setEd] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [authorized, setAuthorized] = useState(false);
  const [showToken, setShowToken] = useState(false);

  //const [newList, setListofDates] = useState([]);
  // const [d,setd] = useState();

  const handleInputChange = () => {
    setProgress((prevProgress) => prevProgress + 25);
  };

  const makeList = (startDate, endDate) => {
    const dlist = [];
    const d = new Date(startDate);
    const l = new Date(endDate);

    while (d <= l) {
      dlist.push(d);
      d.setDate(d.getDate() + 1);
    }

    return dlist;
  };
  const formatDate = (date) => {
    return date.toISOString().split("T")[0];
  };
  const newList = makeList(sd, ed);

  const handleSubmit = async () => {
    console.log(newList);
    console.log("Submitting...");
    setLoading(true);
    setError(null);
    setData([]);
    setProgress(0);
    const params = new URLSearchParams(window.location.search);
    const token = params.get("access_token");
    const name = params.get("username");
    const apiUrl = `/contributions?username=${name}&token=${token}&start_date=${sd}&end_date=${ed}`;
    console.log("API URL:", apiUrl);

    try {
      const res = await fetch(apiUrl);
      console.log("Response:", res);
      if (!res.ok) {
        alert(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      console.log("Data:", data);

      setData(data);
      // setListofDates(newList);
    } catch (error) {
      setError(error.message);
      console.error("Error fetching data:", error);
      console.log("error");
    } finally {
      setLoading(false);
      console.log("Finished submitting");
    }
  };
  return (
    <div className="overflow-none">
      <header className=" bg-black text-white text-primary-foreground px-4 py-3 font-bold">
        Main Header
      </header>
      <div className="flex justify-center items-center h-screen">
        <div>
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
                      handleInputChange();
                    }}
                    placeholder="Select start date"
                    dateformat="yyyy-MM-dd"
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
                      handleInputChange();
                    }}
                    placeholder="Select end date"
                    dateformat="yyyy-MM-dd"
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
              <div className="grid grid-cols-5 sm:grid-cols-10 gap-2">
                {data.length > 0 &&
                  data.map((date, index) => (
                    <div
                      key={index}
                      className="bg-muted rounded px-2 py-1 text-center"
                    >
                      {date}
                    </div>
                  ))}
              </div>
            </div>
          </div>
          <footer className="bg-muted text-muted-foreground px-4 py-3 text-sm">
            This will return a List of Contribution between any selected dates.
          </footer>
        </div>
      </div>
    </div>
  );
}

export default Main;
