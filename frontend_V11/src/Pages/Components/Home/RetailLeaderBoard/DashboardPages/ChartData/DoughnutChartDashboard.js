import React from "react";
import { Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend
);

// Dummy data for each region
const doughnutDataByRegion = {
  north: { wastage: 1.4, total: 21.2 },
  south: { wastage: 50, total: 100 },
  east: { wastage: 25, total: 100 },
  west: { wastage: 75, total: 100 },
};

const DoughnutChartDashboard = ({ filters,data }) => {
  const {
    category = "Produce (Fresh)",
    region = "north",
    selectedDate,
    selectedChannels,
    selectedStores,
    subCategory,
  } = filters;


const wastage=data;
const total=100;

  const doughnutData = {
    labels: ["Wastage", "Remaining"],
    datasets: [
      {
        data: [wastage, total - wastage],
        backgroundColor: ["#FFAD28", "#707070"],
        borderWidth: 0,
      },
    ],
  };

  const doughnutOptions = {
    plugins: {
      legend: { display: false },
    },
  };

  return <Doughnut data={doughnutData} options={doughnutOptions} />;
};

export default DoughnutChartDashboard;
