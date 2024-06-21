import React, { useState } from 'react';
import { Button, TextInput, Progress,Label } from 'flowbite-react';
import { GoogleLogin } from '@react-oauth/google';
import {LineChart} from '@mui/x-charts';
// import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { Datepicker,Checkbox } from 'flowbite-react';

//import { parseISO} from 'date-fns';

import "./App.css";
//import { colors } from '@mui/material';

function App() {
  const [data, setData] = useState([]);
  const [name, setName] = useState('');
  const [token, setToken] = useState('');
  const [sd, setSd] = useState('');
  const [ed, setEd] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [authorized,setAuthorized] = useState(false)
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
}
  const formatDate = (date) => {
    return date.toISOString().split('T')[0] ;
  }
  const newList = makeList(sd,ed);
  const handleSubmit = async () => {
    

    console.log(newList);
    console.log('Submitting...');
    setLoading(true);
    setError(null);
    setData([]);
    setProgress(0);

    const apiUrl = `/contributions?username=${name}&token=${token}&start_date=${sd}&end_date=${ed}`;
    console.log('API URL:', apiUrl);
    

    try {
      const res = await fetch(apiUrl);
      console.log('Response:', res);
      if (!res.ok) {
        alert(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      console.log('Data:', data);

      setData(data);
      // setListofDates(newList);
      
    } catch (error) {
      setError(error.message);
      console.error('Error fetching data:', error);
      console.log('error');
    } finally {
      setLoading(false);
      console.log('Finished submitting');
      
    }
  };

  // React.useEffect(() => {
  //   document.title = 'Github!';
  // }, []);

  return (
    <>
      <div className='full-page-container'>
      <h1 style={{fontsize:'small',textShadow: '2px 2px 2.5px blue',textAlign:"center", fontFamily:'cursive',fontWeight:'bolder'}}>Welcome to Github Contribution Tracker</h1>
        
        {authorized?(
          
          <div className='second' style={{ justifyContent: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h1 >Enter Information!</h1>

                      <form className="flex max-w-md flex-col gap-4">
                        <TextInput className="i1" type="text" name="name" placeholder="Enter Name" value={name} onChange={(e) => { setName(e.target.value); handleInputChange(); }} />
                        {showToken && (
                                        <TextInput className="i2" type="text" name="token" placeholder="Enter token" value={token} onChange={(e) => { setToken(e.target.value); handleInputChange(); }} />
                                      )}    
                <div className='labelb'>                    
                <Label className='label' style={{color:'white'}}>Show Token</Label>
                        <Checkbox
                          className='check'
                          id="check"
                          type="Checkbox"
                          checked={showToken}
                          onChange={() => setShowToken((prev) => !prev)}
                        />
                  </div>
                        <Datepicker
                          value={sd}
                          onSelectedDateChanged={(date) => {setSd(formatDate(date)); handleInputChange();}}
                          placeholder="Select start date"
                          dateformat="yyyy-MM-dd"
                        />
                        <Datepicker
                          value={ed}
                          onSelectedDateChanged={(date) => {setEd(formatDate(date)); handleInputChange();}}
                          placeholder="Select end date"
                          dateformat="yyyy-MM-dd"
                        />
                        <Button gradientMonochrome="info" onClick={handleSubmit}>Submit</Button>
                        <Progress progress={progress} />
                        {loading && <p>Loading...</p>}
                        {error && <p style={{ color: 'red', fontSize: 'x-large', fontFamily: 'sans-serif' }}>{error}</p>}
                        {data.length > 0 && (
                          <div className="ouput">
                            <h2>Data:</h2>
                            <h2>{JSON.stringify(data, null, 2)}</h2>
                            <div className='chart' >
                            <LineChart 
                              xAxis={[{ data: newList ,color: '#e15759'}]}
                              series={[
                                {
                                  data: data,color: '#e15759'
                                }
                              ]}
                              width={500}
                              height={300}
                              sx={{
                            //change left yAxis label styles
                          "& .MuiChartsAxis-left .MuiChartsAxis-tickLabel":{
                            strokeWidth:"0.4",
                            fill:"#e15759"
                          },
                          // change all labels fontFamily shown on both xAxis and yAxis
                          "& .MuiChartsAxis-tickContainer .MuiChartsAxis-tickLabel":{
                              fontFamily: "Roboto",
                            },
                            // change bottom label styles
                            "& .MuiChartsAxis-bottom .MuiChartsAxis-tickLabel":{
                                strokeWidth:"0.5",
                                fill:"#e15759"
                            },
                              // bottomAxis Line Styles
                            "& .MuiChartsAxis-bottom .MuiChartsAxis-line":{
                              stroke:"#e15759",
                              strokeWidth:2
                            },
                            // leftAxis Line Styles
                            "& .MuiChartsAxis-left .MuiChartsAxis-line":{
                              stroke:"#e15759",
                              strokeWidth:2
                            }
                          }}
                            />
                          </div>
                          </div>
                        )}
                      </form>
            </div>
        ):(
   
            <div style={{ display: 'flex', justifyContent: 'center',paddingTop:'100px' }}>
              <form className="flex max-w-md flex-col gap-4">
                <div>
                  <div className="mb-2 block">
                    <Label htmlFor="email2" value="Your email" style={{color:'white'}}/>
                  </div>
                  <TextInput id="email2" type="email" placeholder="name@flowbite.com" required shadow />
                </div>
                <div>
                  <div className="mb-2 block">
                    <Label htmlFor="password2" value="Your password" style={{color:'white'}}/>
                  </div>
                  <TextInput id="password2" type="password" required shadow />
                </div>
                <div>
                  <div className="mb-2 block">
                    <Label htmlFor="repeat-password" value="Repeat password" style={{color:'white'}}/>
                  </div>
                  <TextInput id="repeat-password" type="password" required shadow />
                </div>
                <div className="flex items-center gap-2">
                  <Checkbox id="agree" />
                  <Label htmlFor="agree" className="flex" style={{color:'white'}}>
                    I agree with the&nbsp; <p className="text-cyan-600 hover:underline dark:text-cyan-500"> terms and conditions</p>
                    
                  </Label>
                </div>
                <Button type="submit" >Register new account</Button>
              </form>
            <p style={{color:'white',fontWeight:'bold',paddingLeft:'75px',paddingTop:'115px',fontSize:'x-large'}}>Or</p>
            <div style={{paddingLeft:'115px',paddingTop:'100px'}}>
              <GoogleLogin
                onSuccess={credentialResponse => {
                  console.log(credentialResponse);
                  setAuthorized(true);
                }}
                theme="filled_blue"
                shape='circle'
                onError={() => {
                  console.log('Login Failed');
                }}
              />
            </div>
            </div>
        )}
        
      </div>
    </>
  );
}

export default App;
