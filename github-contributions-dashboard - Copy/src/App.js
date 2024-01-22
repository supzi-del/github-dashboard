import React, { useEffect, useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { ResponsiveContainer, PieChart, Pie, Tooltip } from 'recharts';
import './App.css';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const App = () => {
  const [contributions, setContributions] = useState(null);

  useEffect(() => {
    // Fetch data from your Flask backend or API endpoint
    fetch('http://127.0.0.1:5000/get_contributions/sample-collab')
      .then(response => response.json())
      .then(data => setContributions(data));
  }, []);

  return (
    <div className="App">
      <h1>Github Contributions Dashboard</h1>

      {/* Display Table */}
      {contributions && (
        <div className="section table-section">
          <h2>Individual Code Contributions</h2>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow className="table-header">
                  <TableCell>User</TableCell>
                  <TableCell>No. of Line Changes</TableCell>
                  <TableCell>No. of File Changes</TableCell>
                  <TableCell>PRs Merged</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Object.keys(contributions.users).map(user => (
                  <TableRow key={user}>
                    <TableCell>{user}</TableCell>
                    <TableCell>{contributions.users[user].line_changes}</TableCell>
                    <TableCell>{contributions.users[user].file_changes}</TableCell>
                    <TableCell>{contributions.users[user].prs}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      )}

      {/* Display Pie Charts */}
      {contributions && (
        <div className="section pie-chart-section">
          <h2>Pie Chart: Distribution of PRs Created</h2>
          <div className="pie-chart">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  dataKey="value"
                  data={Object.entries(contributions.created_prs).map(([user, value], index) => ({
                    user,
                    value,
                    fill: COLORS[index % COLORS.length],
                  }))}
                  outerRadius={80}
                  label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>

            <div className="legend">
              {Object.entries(contributions.created_prs).map(([user, value], index) => (
                <div key={user} style={{ marginRight: '10px' }}>
                  <span
                    style={{
                      display: 'inline-block',
                      width: '10px',
                      height: '10px',
                      backgroundColor: COLORS[index % COLORS.length],
                      marginRight: '5px',
                    }}
                  ></span>
                  {user}
                </div>
              ))}
            </div>
          </div>

          <h2>Pie Chart: Distribution of PRs Reviewed</h2>
          <div className="pie-chart">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  dataKey="value"
                  data={Object.entries(contributions.reviewed_prs).map(([user, value], index) => ({
                    user,
                    value,
                    fill: COLORS[index % COLORS.length],
                  }))}
                  outerRadius={80}
                  label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>

            <div className="legend">
              {Object.entries(contributions.reviewed_prs).map(([user, value], index) => (
                <div key={user} style={{ marginRight: '10px' }}>
                  <span
                    style={{
                      display: 'inline-block',
                      width: '10px',
                      height: '10px',
                      backgroundColor: COLORS[index % COLORS.length],
                      marginRight: '5px',
                    }}
                  ></span>
                  {user}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
