import React, { useState,useEffect } from "react";
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
import img3 from '../../../../../assets/CommandCenterImage/info-icon.svg';
import SupplierShrinkageChart from "./ChartData/SupplierShrinkageChart";

import ChartDataComp from "./ChartData/ChartDataComp";
import DashboardGraphsService from "../../../../../services/dashboardGraphsService";



const DashboardLeaderBoard = () => {
  const { chartData } = useDashboard();
  const [selectedCategory, setSelectedCategory] = useState("Produce (Fresh)");

  // inside DashboardLeaderBoard component (replace the current BarChartCard)
  const BarChartCard = ({ title,data }) => {
// console.log(data,"hello")

    return (
      <div className="flex-1 bg-white shadow-md rounded-lg p-4 relative ">
      <h3 className="text-lg font-semibold mb-4 titleTextChart">{title}</h3>
      {/* pass full filters object so chart can use all filters */}
      <BarChartDashboard filters={filters} data={data} />
    </div>
    )
  };

  const SupplierShrinkageCard = ({ title, ChartComponent, filters,data }) => (
    <div className="flex-1 bg-white shadow-md rounded-lg p-4 relative">
      <h3 className="text-lg font-semibold mb-4 titleTextChart">{title}</h3>
      <ChartComponent filters={filters} data={data}/>
    </div>
  );

  const DoughnutChartCard = ({ title, filters,data }) => (
  <div className="flex-1 bg-white shadow-md rounded-lg p-4 relative doughnutChartBOx min-h-[290px]">
    <h3 className="text-lg font-semibold mb-4 titleTextChart">{title}</h3>
    <DoughnutChartDashboard filters={filters} data={data} /> 
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

  const [dashboardData, setDashboardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadDashboards = async () => {
      try {
        const response = await DashboardGraphsService.fetchDashboardGraphs(filters);
        setDashboardData(response);
        console.log(response)
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadDashboards();
  }, [filters]); 

  // re-fetch when filters change
  if (loading) return <div>Loading KPIs...</div>;
  if (error) return <div>Error: {error}</div>;


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
            {/* <div className="w-4 h-4 bg-green-500 rounded-full mr-3"></div> */}
            <img src={img3} alt="info-icon" className="inline-block h-3.5 w-3.5 mr-1" />
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
            <BarChartCard title="Wastage By Merch Category" data={dashboardData?.wastage_by_month_cat}/>
            <DoughnutChartCard title="Waste % of COGS" filters={filters} data={dashboardData["Waste_%_of_Net_Sales"]}/>

            <SupplierShrinkageCard
              title="Suppliers with highest Shrinkage % of Net Sales"
              ChartComponent={TopSupplierShrinkageChart}
              filters={filters}
              data={dashboardData["Top_Suppliers_By_Shrinkage"]}
            />
          </div>
        </div>

        {/* Bottom Section (Shuffled) */}
        <div className="mt-4">
          <div className="flex flex-col lg:flex-row gap-6 min-h-[290px] items-stretch">
            <DoughnutChartCard
              title="Non Sellable Inventory Overview"
              filters={filters}
              data={dashboardData["Non_Sellable_Units"]}
            />
            <BarChartCard title="Sales($) vs Shrinkage % vs Salvage % " 
              // data={dashboardData["Sales_Shrinkage_Salvage"]}
              data={dashboardData?.wastage_by_month_cat}
            />
            <SupplierShrinkageCard
              title="Top 10 SKU's Shrinkage % by Sales"
              ChartComponent={BottomSupplierShrinkageChart}
              filters={filters}
              data={dashboardData["Top_SKUs_By_Shrinkage"]}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLeaderBoard;
