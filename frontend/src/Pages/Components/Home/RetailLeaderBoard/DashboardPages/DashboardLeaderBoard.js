import React, { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../../../CommonComponents/ui/select";
import { useDashboard } from "../../../../../Data/DashboardContext";
import "../LeaderBoard.css";
import SalesProjection from "./SalesProjections";
import { Filters } from "./Filters";

import DoughnutChartDashboard from "./ChartData/DoughnutChartDashboard";

import {
  TopSupplierShrinkageChart,
  BottomSupplierShrinkageChart,
} from "./ChartData/SupplierShrinkageChart";
import BarChartDashboard from "./ChartData/BarChartDashboard";
import SupplierShrinkageChart from "./ChartData/SupplierShrinkageChart";

import ChartDataComp from "./ChartData/ChartDataComp";
// import { MetricCard } from '@/components/dashboard/MetricCard';
// import { DashboardBarChart } from '@/components/dashboard/BarChart';
// import { DonutChart } from '@/components/dashboard/DonutChart';
// import { HorizontalBarChart } from '@/components/dashboard/HorizontalBarChart';
// import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, LineChart, Line } from 'recharts';
// import { Card, CardContent } from '@/components/ui/card';

const DashboardLeaderBoard = () => {
  const { chartData } = useDashboard();
  const [selectedCategory, setSelectedCategory] = useState("Produce (Fresh)");

  // inside DashboardLeaderBoard component (replace the current BarChartCard)
  const BarChartCard = ({ title }) => (
    <div className="flex-1 bg-white shadow-md rounded-lg p-4 relative ">
      <h3 className="text-lg font-semibold mb-4 titleTextChart">{title}</h3>
      {/* pass full filters object so chart can use all filters */}
      <BarChartDashboard filters={filters} />
    </div>
  );

  const SupplierShrinkageCard = ({ title, ChartComponent, filters }) => (
    <div className="flex-1 bg-white shadow-md rounded-lg p-4 relative">
      <h3 className="text-lg font-semibold mb-4 titleTextChart">{title}</h3>
      <ChartComponent filters={filters} />
    </div>
  );

  const DoughnutChartCard = ({ title, filters }) => (
  <div className="flex-1 bg-white shadow-md rounded-lg p-4 relative doughnutChartBOx min-h-[290px]">
    <h3 className="text-lg font-semibold mb-4 titleTextChart">{title}</h3>
    <DoughnutChartDashboard filters={filters} /> 
    <div className="absolute bottom-2 right-2 text-sm text-gray-600 bottomTitle">
      Total COGS ($) = $26.4M
    </div>
  </div>
);




  const [filters, setFilters] = useState({
    region: "North",
    selectedStores: [],
    selectedChannels: [],
    selectedDate: null,
    category: "Produce (Fresh)",
  });

  const getFilteredData = ({ region, selectedChannels }) => {
    // Temporary demo logic — to be replaced with actual data handling
    if (region === "South") {
      return chartData.south;
    } else if (region === "East") {
      return chartData.east;
    } else if (region === "West") {
      return chartData.west;
    }
    return chartData.default || chartData;
  };

  const [data, setData] = useState(chartData);

  const handleApplyFilters = (selectedFilters) => {
    setFilters(selectedFilters);
    const filteredData = getFilteredData(selectedFilters);
    setData(filteredData);
  };

  const cogsData = [
    { name: "Waste", value: 7.3 },
    { name: "Other", value: 92.7 },
  ];

  const inventoryData = [
    { name: "Damaged", value: chartData.inventoryOverview.damaged },
    { name: "Products Expired", value: chartData.inventoryOverview.expired },
  ];
  return (
    <div className="">
      {/* Filter Controls */}
      <Filters
        onApply={handleApplyFilters}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
      />

      <div className="p-4 contentSecdasboard">
        {/* Alert Banner */}
        <div className="bg-success border-l-4 border-success px-2 py-2 addSection ">
          <div className="flex items-center ">
            <div className="w-4 h-4 bg-green-500 rounded-full mr-3"></div>
            <span className="text-sm text-green-800 addText">
              <strong>Green Giant</strong> is outperforming mixed greens in the
              Northeast region leading to a <strong>19% shrink</strong>. Sales
              down in Fresh-cut Fruit Salads by <strong>8.2%</strong>. Organic
              Fuji Apples (1 lb) is now the top selling SKU
            </span>
          </div>
        </div>

        <div className="mt-2 ">
          <SalesProjection filters={filters} />
        </div>
        {/* Top Section */}
        <div className="mt-4">
          <div className="flex flex-col lg:flex-row gap-6 min-h-[290px] ">
            <BarChartCard title="Wastage By Merch Category" />
            <DoughnutChartCard title="Waste % of COGS" filters={filters} />

            <SupplierShrinkageCard
              title="Suppliers with highest Shrinkage % of Net Sales"
              ChartComponent={TopSupplierShrinkageChart}
              filters={filters}
            />
          </div>
        </div>

        {/* Bottom Section (Shuffled) */}
        <div className="mt-4">
          <div className="flex flex-col lg:flex-row gap-6 min-h-[290px] items-stretch">
            <DoughnutChartCard
              title="Non Sellable Inventory Overview"
              filters={filters}
            />
            <BarChartCard title="Sales($) vs Shrinkage % vs Salvage % " />
            <SupplierShrinkageCard
              title="Top 10 SKU's Shrinkage % by Sales"
              ChartComponent={BottomSupplierShrinkageChart}
              filters={filters}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLeaderBoard;
