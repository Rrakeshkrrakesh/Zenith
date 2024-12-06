import React, { useState } from "react";

function App() {
  const [qpResult, setQpResult] = useState(null);

  const optimizeQP = async () => {
    const response = await fetch(`/api/optimize_qp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ hours_available: 168 }),
    });
    const data = await response.json();
    if (data.success) {
      setQpResult(data);
    } else {
      alert("QP Optimization failed");
    }
  };

  return (
    <div>
      <h1>Zenith</h1>
      <button onClick={optimizeQP}>Optimize with QP</button>
      {qpResult && (
        <div>
          <h2>Optimal QP Allocation</h2>
          <ul>
            {Object.entries(qpResult.allocation).map(([activity, hours]) => (
              <li key={activity}>
                {activity}: {hours.toFixed(2)} hours
              </li>
            ))}
          </ul>
          <h3>Life Factor Scores</h3>
          <ul>
            {Object.entries(qpResult.scores).map(([factor, score]) => (
              <li key={factor}>
                {factor}: {score.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
