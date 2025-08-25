import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from 'recharts';


// 📌 All filter-based data stored here
const chartDataByFilters = {
  all: {
    topData: [
      { name: 'Dole Fresh', value: 18 },
      { name: 'Chiquita', value: 17 },
      { name: 'Fresh Express', value: 16 },
      { name: "Driscoll's", value: 15 },
      { name: 'Ready Pac', value: 14 },
      { name: 'Taylor Farms', value: 13.5 },
      { name: 'Taylor Farms Somon', value: 13 },
      { name: 'Fresh Gourmet', value: 12.5 },
      { name: 'Calavo Growers', value: 12 },
      { name: 'Mann Packing', value: 11.5 },
    ],
    bottomData: [
      { name: 'Strawberries (1 lb clamshell)', value: 23 },
      { name: 'Leafy Spinach (bagged)', value: 20 },
      { name: 'Fresh Herbs (e.g., cilantro)', value: 19 },
      { name: 'Blueberries', value: 17 },
      { name: 'Cut Pineapple Cups', value: 15 },
      { name: 'Avocados (ripe)', value: 15 },
      { name: 'Mixed Salad Kits', value: 14 },
      { name: 'Tomatoes on the vine', value: 13 },
      { name: 'Bagged Carrots', value: 12 },
      { name: 'Broccoli Crowns', value: 11 },
    ],
  },
  north: {
    topData: [
      { name: 'North Supplier 1', value: 20 },
      { name: 'North Supplier 2', value: 19 },
      { name: 'North Supplier 3', value: 18 },
      { name: 'North Supplier 4', value: 17 },
      { name: 'North Supplier 5', value: 11 },
      { name: 'North Supplier 6', value: 10 },
      { name: 'North Supplier 7', value: 9 },
      { name: 'North Supplier 8', value: 7 },
      { name: 'North Supplier 9', value: 5 },
    ],
    bottomData: [
      { name: 'North Product 1', value: 22 },
      { name: 'North Product 2', value: 21 },
      { name: 'North Product 3', value: 19 },
      { name: 'North Product 4', value: 18 },
      { name: 'North Product 5', value: 15 },
      { name: 'North Product 6', value: 13 },
      { name: 'North Product 7', value: 11 },
      { name: 'North Product 8', value: 9 },
    ],
  },
  south: {
    topData: [
      { name: 'South Supplier 1', value: 15 },
      { name: 'South Supplier 2', value: 14 },
      { name: 'South Supplier 3', value: 11 },
      { name: 'South Supplier 4', value: 17 },
      { name: 'South Supplier 5', value: 19 },
      { name: 'South Supplier 6', value: 10 },
      { name: 'South Supplier 7', value: 8 },
      { name: 'South Supplier 8', value: 6 },
      { name: 'South Supplier 9', value: 9 },

    ],
    bottomData: [
      { name: 'South Product 1', value: 18 },
      { name: 'South Product 2', value: 17 },
      { name: 'South Product 3', value: 11 },
      { name: 'South Product 4', value: 13 },
      { name: 'South Product 5', value: 15 },
      { name: 'South Product 6', value: 20 },
      { name: 'South Product 7', value: 17 },

    ],
  },
};

// 📌 Reusable chart template
const ChartTemplate = ({ data, maxDomain }) => (
  <ResponsiveContainer width="95%" height={200}>
    <BarChart
      layout="vertical"
      data={data}
      margin={{ top: 0, right: 0, left: -40, bottom: 0 }}
    >
      <XAxis
        type="number"
        domain={[0, maxDomain]}
        tickFormatter={(value) => `${value}%`}
        tick={false}
        axisLine={false}
        tickLine={false}
      />
      <YAxis
        type="category"
        dataKey="name"
        width={200}
        tick={{ fontSize: 10 }}
        axisLine={false}
        tickLine={false}
        interval={0}
      />
      <Tooltip formatter={(value) => `${value}%`} />
      <Bar dataKey="value" fill="#f59e0b">
        <LabelList
          dataKey="value"
          position="right"
          formatter={(value) => `${value}%`}
          style={{ fontSize: 10 }}
        />
      </Bar>
    </BarChart>
  </ResponsiveContainer>
);

// 📌 Top Supplier Shrinkage Chart
export const TopSupplierShrinkageChart = ({filters}) => {
  
  const regionKey = filters.region?.toLowerCase() || 'all';
const currentData = chartDataByFilters[regionKey]?.topData || chartDataByFilters.all.topData;


  return <ChartTemplate data={currentData} maxDomain={25} />;
};

// 📌 Bottom Supplier Shrinkage Chart
export const BottomSupplierShrinkageChart = ({filters}) => {
  
  const regionKey = filters.region?.toLowerCase() || 'all';
const currentData = chartDataByFilters[regionKey]?.bottomData || chartDataByFilters.all.bottomData;


  return <ChartTemplate data={currentData} maxDomain={25} />;
};
