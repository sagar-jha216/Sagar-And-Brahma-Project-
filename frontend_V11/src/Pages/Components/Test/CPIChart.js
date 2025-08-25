// import React from 'react';
// import {
//   LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
// } from 'recharts';

// const data = [
//   { name: 'Product A', CPI: 95 },
//   { name: 'Product B', CPI: 110 },
//   { name: 'Product C', CPI: 150 },
//   { name: 'Product D', CPI: 200 },
// ];

// const CPIChart = () => (
//   <ResponsiveContainer width="100%" height={400}>
//     <LineChart data={data}
//       margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
//       <CartesianGrid strokeDasharray="3 3" />
//       <XAxis dataKey="name" />
//       <YAxis domain={[0, 'dataMax + 20']} tickFormatter={(value) => `${value}%`} />
//       <Tooltip formatter={(value) => `${value}%`} />
//       <Legend />
//       <Line type="monotone" dataKey="CPI" stroke="#8884d8" activeDot={{ r: 8 }} />
//     </LineChart>
//   </ResponsiveContainer>
// );

// export default CPIChart;
