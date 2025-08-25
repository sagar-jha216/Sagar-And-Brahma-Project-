import React,{useEffect,useState} from "react";
import "./salesProjection.css";
import { Doughnut, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";
import DashboardService from "../../../../../../services/dashboardService";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

// Dummy KPI data (same as your original)
// ✅ Full KPI Data for All Categories & Regions
export const kpiDataByCategory = {
  "Produce (Fresh)": {
    North: [
      {
        title: "Stock Inventory Accuracy %",
        value: 98.2,
        doughnutchartData: [98.2, 1.8],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.5,
        doughnutchartData: [1.5, 98.5],
        vs: -0.5,
      },
      { title: "Dump %", value: 3.8, doughnutchartData: [3.8, 96.2], vs: -1.1 },
      {
        title: "Aged Inventory %",
        value: 3.5,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [150, 200, 180, 220] }],
        },
        vs: 3.1,
      },
      {
        title: "% Of Products Expired",
        value: 6,
        doughnutchartData: [6, 94],
        vs: 2.8,
      },
      {
        title: "Shrinkage% to SKU",
        value: 80,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 80,
      },
      {
        title: "Return %",
        value: 1.0,
        doughnutchartData: [1.0, 99.0],
        vs: 2.9,
      },
    ],
    South: [
      {
        title: "Stock Inventory Accuracy %",
        value: 96.4,
        doughnutchartData: [96.4, 3.6],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 2.1,
        doughnutchartData: [2.1, 97.9],
        vs: -0.8,
      },
      { title: "Dump %", value: 4.5, doughnutchartData: [4.5, 95.5], vs: -1.3 },
      {
        title: "Aged Inventory %",
        value: 4.0,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [160, 210, 175, 230] }],
        },
        vs: 2.9,
      },
      {
        title: "% Of Products Expired",
        value: 5.5,
        doughnutchartData: [5.5, 94.5],
        vs: 2.6,
      },
      {
        title: "Shrinkage% to SKU",
        value: 78,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 78,
      },
      {
        title: "Return %",
        value: 1.2,
        doughnutchartData: [1.2, 98.8],
        vs: 2.7,
      },
    ],
    East: [
      {
        title: "Stock Inventory Accuracy %",
        value: 97.1,
        doughnutchartData: [97.1, 2.9],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.8,
        doughnutchartData: [1.8, 98.2],
        vs: -0.6,
      },
      { title: "Dump %", value: 3.2, doughnutchartData: [3.2, 96.8], vs: -1.0 },
      {
        title: "Aged Inventory %",
        value: 3.9,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [140, 195, 185, 210] }],
        },
        vs: 3.0,
      },
      {
        title: "% Of Products Expired",
        value: 4.9,
        doughnutchartData: [4.9, 95.1],
        vs: 2.5,
      },
      {
        title: "Shrinkage% to SKU",
        value: 79,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 79,
      },
      {
        title: "Return %",
        value: 1.1,
        doughnutchartData: [1.1, 98.9],
        vs: 2.8,
      },
    ],
    West: [
      {
        title: "Stock Inventory Accuracy %",
        value: 95.8,
        doughnutchartData: [95.8, 4.2],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 2.4,
        doughnutchartData: [2.4, 97.6],
        vs: -0.9,
      },
      { title: "Dump %", value: 4.0, doughnutchartData: [4.0, 96.0], vs: -1.2 },
      {
        title: "Aged Inventory %",
        value: 4.3,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [155, 205, 190, 225] }],
        },
        vs: 3.2,
      },
      {
        title: "% Of Products Expired",
        value: 5.2,
        doughnutchartData: [5.2, 94.8],
        vs: 2.6,
      },
      {
        title: "Shrinkage% to SKU",
        value: 81,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 81,
      },
      {
        title: "Return %",
        value: 1.3,
        doughnutchartData: [1.3, 98.7],
        vs: 2.9,
      },
    ],
  },

  "Dry Goods": {
    North: [
      {
        title: "Stock Inventory Accuracy %",
        value: 97.5,
        doughnutchartData: [97.5, 2.5],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.2,
        doughnutchartData: [1.2, 98.8],
        vs: -0.4,
      },
      { title: "Dump %", value: 2.9, doughnutchartData: [2.9, 97.1], vs: -1.0 },
      {
        title: "Aged Inventory %",
        value: 2.8,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [180, 220, 210, 250] }],
        },
        vs: 2.2,
      },
      {
        title: "% Of Products Expired",
        value: 3.2,
        doughnutchartData: [3.2, 96.8],
        vs: 2.0,
      },
      {
        title: "Shrinkage% to SKU",
        value: 77,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 77,
      },
      {
        title: "Return %",
        value: 0.8,
        doughnutchartData: [0.8, 99.2],
        vs: 1.9,
      },
    ],
    South: [
      {
        title: "Stock Inventory Accuracy %",
        value: 96.8,
        doughnutchartData: [96.8, 3.2],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.5,
        doughnutchartData: [1.5, 98.5],
        vs: -0.6,
      },
      { title: "Dump %", value: 3.5, doughnutchartData: [3.5, 96.5], vs: -1.1 },
      {
        title: "Aged Inventory %",
        value: 3.0,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [190, 230, 215, 260] }],
        },
        vs: 2.3,
      },
      {
        title: "% Of Products Expired",
        value: 3.8,
        doughnutchartData: [3.8, 96.2],
        vs: 2.1,
      },
      {
        title: "Shrinkage% to SKU",
        value: 76,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 76,
      },
      {
        title: "Return %",
        value: 0.9,
        doughnutchartData: [0.9, 99.1],
        vs: 1.8,
      },
    ],
    East: [
      {
        title: "Stock Inventory Accuracy %",
        value: 97.0,
        doughnutchartData: [97.0, 3.0],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.3,
        doughnutchartData: [1.3, 98.7],
        vs: -0.5,
      },
      { title: "Dump %", value: 3.1, doughnutchartData: [3.1, 96.9], vs: -1.0 },
      {
        title: "Aged Inventory %",
        value: 2.9,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [185, 225, 205, 255] }],
        },
        vs: 2.1,
      },
      {
        title: "% Of Products Expired",
        value: 3.5,
        doughnutchartData: [3.5, 96.5],
        vs: 2.0,
      },
      {
        title: "Shrinkage% to SKU",
        value: 75,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 75,
      },
      {
        title: "Return %",
        value: 0.85,
        doughnutchartData: [0.85, 99.15],
        vs: 1.85,
      },
    ],
    West: [
      {
        title: "Stock Inventory Accuracy %",
        value: 96.5,
        doughnutchartData: [96.5, 3.5],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.6,
        doughnutchartData: [1.6, 98.4],
        vs: -0.7,
      },
      { title: "Dump %", value: 3.6, doughnutchartData: [3.6, 96.4], vs: -1.2 },
      {
        title: "Aged Inventory %",
        value: 3.2,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [192, 235, 220, 265] }],
        },
        vs: 2.4,
      },
      {
        title: "% Of Products Expired",
        value: 4.0,
        doughnutchartData: [4.0, 96.0],
        vs: 2.2,
      },
      {
        title: "Shrinkage% to SKU",
        value: 74,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 74,
      },
      {
        title: "Return %",
        value: 0.95,
        doughnutchartData: [0.95, 99.05],
        vs: 1.9,
      },
    ],
  },

  "General Merchandising": {
    North: [
      {
        title: "Stock Inventory Accuracy %",
        value: 98.0,
        doughnutchartData: [98.0, 2.0],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.0,
        doughnutchartData: [1.0, 99.0],
        vs: -0.3,
      },
      { title: "Dump %", value: 2.5, doughnutchartData: [2.5, 97.5], vs: -0.8 },
      {
        title: "Aged Inventory %",
        value: 2.2,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [210, 260, 240, 280] }],
        },
        vs: 1.9,
      },
      {
        title: "% Of Products Expired",
        value: 2.8,
        doughnutchartData: [2.8, 97.2],
        vs: 1.7,
      },
      {
        title: "Shrinkage% to SKU",
        value: 72,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 72,
      },
      {
        title: "Return %",
        value: 0.6,
        doughnutchartData: [0.6, 99.4],
        vs: 1.5,
      },
    ],
    South: [
      {
        title: "Stock Inventory Accuracy %",
        value: 97.2,
        doughnutchartData: [97.2, 2.8],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.2,
        doughnutchartData: [1.2, 98.8],
        vs: -0.4,
      },
      { title: "Dump %", value: 2.9, doughnutchartData: [2.9, 97.1], vs: -0.9 },
      {
        title: "Aged Inventory %",
        value: 2.5,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [215, 265, 250, 290] }],
        },
        vs: 2.0,
      },
      {
        title: "% Of Products Expired",
        value: 3.0,
        doughnutchartData: [3.0, 97.0],
        vs: 1.8,
      },
      {
        title: "Shrinkage% to SKU",
        value: 73,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 73,
      },
      {
        title: "Return %",
        value: 0.7,
        doughnutchartData: [0.7, 99.3],
        vs: 1.6,
      },
    ],
    East: [
      {
        title: "Stock Inventory Accuracy %",
        value: 97.5,
        doughnutchartData: [97.5, 2.5],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.1,
        doughnutchartData: [1.1, 98.9],
        vs: -0.35,
      },
      {
        title: "Dump %",
        value: 2.7,
        doughnutchartData: [2.7, 97.3],
        vs: -0.85,
      },
      {
        title: "Aged Inventory %",
        value: 2.3,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [205, 255, 235, 275] }],
        },
        vs: 1.95,
      },
      {
        title: "% Of Products Expired",
        value: 2.9,
        doughnutchartData: [2.9, 97.1],
        vs: 1.75,
      },
      {
        title: "Shrinkage% to SKU",
        value: 71,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 71,
      },
      {
        title: "Return %",
        value: 0.65,
        doughnutchartData: [0.65, 99.35],
        vs: 1.55,
      },
    ],
    West: [
      {
        title: "Stock Inventory Accuracy %",
        value: 97.0,
        doughnutchartData: [97.0, 3.0],
        date: "15 Jul ‘25",
      },
      {
        title: "Damaged",
        value: 1.3,
        doughnutchartData: [1.3, 98.7],
        vs: -0.45,
      },
      { title: "Dump %", value: 2.8, doughnutchartData: [2.8, 97.2], vs: -0.9 },
      {
        title: "Aged Inventory %",
        value: 2.4,
        BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [208, 258, 245, 285] }],
        },
        vs: 2.0,
      },
      {
        title: "% Of Products Expired",
        value: 3.1,
        doughnutchartData: [3.1, 96.9],
        vs: 1.8,
      },
      {
        title: "Shrinkage% to SKU",
        value: 70,
        shrinkageText: "Shrinkage",
        labelSKUDetails: 70,
      },
      {
        title: "Return %",
        value: 0.75,
        doughnutchartData: [0.75, 99.25],
        vs: 1.6,
      },
    ],
  },
};

const SalesProjection = ({ filters }) => {
  const {
    category = "Produce (Fresh)",
    region,
    selectedDate,
    selectedChannels,
    selectedStores,
    subCategory,
  } = filters;

  const options = {
    cutout: "60%",
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  };

  // let kpiData = [];

  // if (category && region) {
  //   kpiData = kpiDataByCategory[category]?.[region] || [];
  // } else if (category) {
  //   // Default region if not selected
  //   kpiData = kpiDataByCategory[category]?.North || [];
  // } else {
  //   kpiData = [];
  // }



    const [kpiData, setKpiData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      const loadKPIs = async () => {
        try {
          const response = await DashboardService.fetchDashboardKPIs(filters);
          setKpiData(response.kpis);
          console.log(response.kpis)
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };
  
      loadKPIs();
    }, [filters]); 
    // re-fetch when filters change
  
    if (loading) return <div>Loading KPIs...</div>;
    if (error) return <div>Error: {error}</div>;



  return (
    <div className="flex flex-row flex-wrap gap-2 justify-between">
      {kpiData.map((item, index) => {
        const doughnutData = item.doughnutchartData
          ? {
              labels: ["Value", "Remaining"],
              datasets: [
                {
                  data: item.doughnutchartData,
                  backgroundColor: ["#FFAD28", "#E5E7EB"],
                  borderWidth: 0,
                },
              ],
            }
          : null;

        const hasTrend = item.vs !== undefined;
        const isUp = item.vs >= 0;

        return (
          <div
            key={index}
            className="card-box bg-white p-2 rounded shadow border kPICard"
            style={{
              display: "grid",
              gridTemplateRows: "25px 30px 17px 1fr",
              gap: "1px",
            }}
          >
            {/* Title */}
            <h3 className="overflow-hidden leading-tight text-[12px] font-semibold text-gray-800 m-0 kpiTitle">
              {item?.title}
            </h3>

            {/* Value & Chart Row */}
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              {/* Value */}
              <div className="text-2xl font-bold text-black leading-snug">
                {item.value !== undefined ? `${item.value}%` : "NA"}
                {item.shrinkageText && (
                  <span className="text-sm font-normal ml-1 text-black">
                    {item.shrinkageText}
                  </span>
                )}
              </div>

              {/* Chart */}
              <div
                className={`${
                  item.BarChartdata ? "w-16 h-15 mt-2" : "w-12 h-12 mt-2 "
                }`}
              >
                {doughnutData && (
                  <Doughnut data={doughnutData} options={options} />
                )}
                {item.BarChartdata && (
                  <Bar
                    data={{
                      ...item.BarChartdata,
                      datasets: item.BarChartdata.datasets.map((ds) => ({
                        ...ds,
                        backgroundColor: "#FFAD28", // same color for all bars
                      })),
                    }}
                    options={{
                      plugins: {
                        legend: { display: false },
                        tooltip: { enabled: true },
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          ticks: { display: false },
                          grid: { display: false },
                        },
                        x: {
                          display: true,
                          ticks: {
                            font: { size: 8 },
                            maxRotation: 45,
                            minRotation: 45,
                            autoSkip: false,
                          },
                          grid: { display: false, drawBorder: false },
                        },
                      },
                      elements: {
                        bar: {
                          barPercentage: 0.5,
                          maxBarThickness: 10,
                          borderRadius: 2,
                        },
                      },
                      maintainAspectRatio: false,
                    }}
                    height={80}
                    width={80}
                  />
                )}
              </div>
            </div>

            {/* Trend comparison */}
            {/* Trend comparison and Bottom info in one line */}
            <div className="flex items-center text-[9px] text-gray-600 mt-3">
              {/* Trend comparison */}
              <div>
                {hasTrend && (
                  <span
                    className={`font-semibold flex items-center ${
                      isUp ? "text-green-600" : "text-red-600"
                    }`}
                  >
                    {Math.abs(item.vs)}%{" "}
                    <span className="ml-1 mr-1">{isUp ? "▲" : "▼"}</span> vs LW
                  </span>
                )}
              </div>

              {/* Bottom info on same line */}
              <div className="text-[9px] text-gray-600 flex space-x-2 items-center bottomText">
                {item.date && (
                  <div>
                    <span className="font-medium text-black">
                      Adjustment Date:{" "}
                    </span>
                    {item.date}
                  </div>
                )}
                {item.labelSKUDetails && (
                  <div className="text-black font-medium">
                    Due to {item.labelSKUDetails} SKU
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SalesProjection;
