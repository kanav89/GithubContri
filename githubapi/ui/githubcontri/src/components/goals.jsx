import React, { useState, useEffect } from 'react';

function Goal({ username }) {
  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-100 rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-center mb-8 text-indigo-700">GitHub Contribution Goals</h1>
      <div className="grid md:grid-cols-2 gap-8">
        <GoalSetter username={username}  />
        <GoalProgress username={username} />
      </div>
    </div>
  );
}

function GoalSetter({ username }) {
  const [goalType, setGoalType] = useState('daily');
  const [target, setTarget] = useState(1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/set-goal`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ username, goal_type: goalType, target: parseInt(target) })
      });
      if (response.ok) {
        alert('Goal set successfully!');
      } else {
        const errorData = await response.json();
        alert(`Failed to set goal: ${errorData.detail}`);
      }
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4 text-indigo-600">Set New Goal</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="goalType" className="block text-sm font-medium text-gray-700">Goal Type</label>
          <select 
            id="goalType"
            value={goalType} 
            onChange={(e) => setGoalType(e.target.value)}
            className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
        <div>
          <label htmlFor="target" className="block text-sm font-medium text-gray-700">Target Contributions</label>
          <input 
            id="target"
            type="number" 
            value={target} 
            onChange={(e) => setTarget(parseInt(e.target.value))} 
            min="1"
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <button 
          type="submit"
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Set Goal
        </button>
      </form>
    </div>
  );
}

function GoalProgress({ username }) {
  const [progress, setProgress] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      if (!username) {
        setIsLoading(true);
        return;
      }

      try {
        const response = await fetch(`http://localhost:8000/check-goal-progress?username=${username}`);
        if (response.ok) {
          const data = await response.json();
          setProgress(data);
        } else {
          console.error('Failed to fetch progress');
        }
      } catch (error) {
        console.error('Error fetching progress:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProgress();
  }, [username]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4 text-indigo-600">Goal Progress</h2>
      {progress.length === 0 ? (
        <p className="text-gray-500">No goals set yet.</p>
      ) : (
        <div className="space-y-4">
          {progress.map((goal, index) => (
            <div key={index} className="border rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900 capitalize">{goal.goal_type} Goal</h3>
              <p className="text-sm text-gray-500">
                Target: {goal.target} contributions
              </p>
              <div className="mt-2">
                <div className="flex items-center">
                  <span className="text-sm font-medium text-gray-700">
                    Progress: {goal.current}/{goal.target}
                  </span>
                  <span className="ml-auto text-sm font-medium text-gray-700">
                    {Math.round((goal.current / goal.target) * 100)}%
                  </span>
                </div>
                <div className="mt-1 w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className="bg-indigo-600 h-2.5 rounded-full" 
                    style={{ width: `${Math.min((goal.current / goal.target) * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
              <p className="mt-2 text-sm text-gray-500">
                {goal.is_completed 
                  ? goal.is_achieved 
                    ? "Goal achieved!" 
                    : "Goal period ended" 
                  : `Ends on ${new Date(goal.end_date).toLocaleDateString()}`
                }
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Goal;