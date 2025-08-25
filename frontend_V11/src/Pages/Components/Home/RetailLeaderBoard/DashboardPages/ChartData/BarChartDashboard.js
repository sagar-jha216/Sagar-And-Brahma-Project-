import React from "react";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend
);

// -----------------------
// Demo data: category -> region -> chart object
// (months + 4 datasets: netSales (bar), wasteCost, salvageCost, shrinkCost)
// -----------------------
const barChartDataByCategoryAndRegion = {
  "Produce (Fresh)": {
    North: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales: [42.5,39.8,44.2,41.7,45.6,47.3,49.1,48.3,44.5,46.1,50.4,52.0],
        wasteCost:[2.2,2.1,2.2,2.3,2.4,2.5,2.6,2.4,2.3,2.5,2.7,2.8],
        salvageCost:[1.0,1.1,1.0,1.2,1.3,1.4,1.5,1.3,1.2,1.4,1.6,1.7],
        shrinkCost:[0.5,0.6,0.5,0.7,0.8,0.9,1.0,0.9,0.8,0.9,1.1,1.2],
      }
    },
    South: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales: [38.2,37.0,39.5,40.1,41.8,42.7,43.6,44.0,42.1,41.5,45.3,46.8],
        wasteCost:[1.8,1.9,2.0,1.9,2.1,2.0,2.2,2.1,2.0,2.1,2.3,2.2],
        salvageCost:[0.9,1.0,0.8,0.9,1.0,1.1,1.0,0.9,0.8,0.9,1.0,1.1],
        shrinkCost:[0.4,0.5,0.4,0.5,0.6,0.5,0.6,0.5,0.4,0.5,0.6,0.6],
      }
    },
    East: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales: [40.5,39.2,41.1,41.0,43.0,44.5,46.0,45.2,43.8,44.9,47.8,49.1],
        wasteCost:[2.0,2.0,2.1,2.1,2.2,2.3,2.4,2.2,2.1,2.3,2.5,2.6],
        salvageCost:[0.95,1.05,0.95,1.1,1.15,1.2,1.3,1.15,1.05,1.2,1.4,1.5],
        shrinkCost:[0.45,0.55,0.5,0.6,0.7,0.8,0.9,0.8,0.75,0.85,1.0,1.05],
      }
    },
    West: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales: [39.0,38.3,40.8,40.2,42.2,43.8,45.5,45.0,42.9,44.0,46.7,48.2],
        wasteCost:[1.9,1.8,1.9,2.0,2.1,2.2,2.3,2.0,2.0,2.1,2.4,2.5],
        salvageCost:[0.9,1.0,0.95,1.05,1.1,1.15,1.2,1.05,1.0,1.1,1.25,1.3],
        shrinkCost:[0.5,0.6,0.55,0.65,0.75,0.85,0.95,0.85,0.8,0.9,1.05,1.1],
      }
    }
  },

  "Dry Goods": {
    North: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[30.5,31.0,32.5,31.2,33.0,34.8,36.0,35.7,34.0,35.2,37.5,38.1],
        wasteCost:[1.1,1.0,1.2,1.1,1.3,1.2,1.4,1.3,1.2,1.3,1.5,1.6],
        salvageCost:[0.6,0.7,0.6,0.7,0.75,0.8,0.9,0.8,0.75,0.85,0.95,1.0],
        shrinkCost:[0.3,0.35,0.32,0.36,0.4,0.45,0.5,0.47,0.44,0.46,0.5,0.55],
      }
    },
    South: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[28.5,29.2,30.1,29.8,30.9,31.4,32.6,32.0,31.1,31.9,33.8,34.6],
        wasteCost:[1.0,1.05,1.1,1.0,1.15,1.12,1.18,1.1,1.05,1.15,1.2,1.25],
        salvageCost:[0.55,0.6,0.58,0.6,0.62,0.65,0.68,0.65,0.6,0.66,0.72,0.75],
        shrinkCost:[0.28,0.3,0.29,0.31,0.34,0.36,0.38,0.36,0.35,0.37,0.4,0.42],
      }
    },
    East: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[31.0,30.7,32.0,31.5,33.3,34.2,35.4,35.0,33.9,34.5,36.7,37.3],
        wasteCost:[1.15,1.05,1.12,1.1,1.2,1.18,1.25,1.2,1.15,1.2,1.28,1.3],
        salvageCost:[0.6,0.62,0.61,0.65,0.66,0.68,0.72,0.7,0.66,0.7,0.78,0.8],
        shrinkCost:[0.32,0.33,0.31,0.34,0.36,0.38,0.4,0.39,0.37,0.39,0.42,0.44],
      }
    },
    West: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[29.8,29.5,30.6,30.0,31.2,32.0,33.3,33.0,31.8,32.5,34.3,35.0],
        wasteCost:[1.05,1.0,1.05,1.08,1.1,1.12,1.15,1.1,1.07,1.12,1.18,1.2],
        salvageCost:[0.58,0.6,0.59,0.6,0.63,0.66,0.68,0.66,0.64,0.68,0.72,0.75],
        shrinkCost:[0.29,0.3,0.3,0.32,0.34,0.35,0.37,0.36,0.35,0.36,0.39,0.41],
      }
    }
  },

  "General Merchandising": {
    North: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[22.5,23.8,24.2,23.7,24.6,25.3,26.1,25.8,24.5,25.1,26.4,27.0],
        wasteCost:[0.8,0.85,0.9,0.88,0.9,0.95,0.98,0.95,0.9,0.92,0.98,1.0],
        salvageCost:[0.45,0.5,0.48,0.5,0.52,0.55,0.58,0.56,0.53,0.55,0.6,0.62],
        shrinkCost:[0.25,0.27,0.26,0.28,0.3,0.31,0.33,0.32,0.3,0.31,0.34,0.35],
      }
    },
    South: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[21.8,22.4,23.1,22.9,24.0,24.6,25.5,25.2,24.1,24.7,25.9,26.5],
        wasteCost:[0.75,0.8,0.82,0.8,0.85,0.87,0.9,0.88,0.85,0.86,0.9,0.92],
        salvageCost:[0.42,0.45,0.44,0.46,0.47,0.5,0.52,0.5,0.48,0.5,0.53,0.55],
        shrinkCost:[0.24,0.25,0.24,0.26,0.28,0.29,0.31,0.3,0.29,0.3,0.32,0.33],
      }
    },
    East: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[22.9,23.3,24.0,23.8,24.9,25.6,26.4,26.0,25.0,25.6,26.8,27.4],
        wasteCost:[0.78,0.82,0.85,0.83,0.86,0.9,0.92,0.9,0.87,0.88,0.92,0.94],
        salvageCost:[0.44,0.46,0.47,0.49,0.5,0.52,0.55,0.53,0.5,0.52,0.55,0.57],
        shrinkCost:[0.26,0.27,0.26,0.28,0.3,0.31,0.33,0.32,0.31,0.32,0.34,0.35],
      }
    },
    West: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: {
        netSales:[23.8,24.2,24.9,24.5,25.4,26.1,26.9,26.6,25.6,26.2,27.5,28.0],
        wasteCost:[0.82,0.85,0.88,0.86,0.9,0.93,0.95,0.93,0.9,0.92,0.96,0.98],
        salvageCost:[0.46,0.48,0.49,0.51,0.52,0.55,0.57,0.56,0.53,0.55,0.58,0.6],
        shrinkCost:[0.27,0.28,0.27,0.29,0.31,0.32,0.34,0.33,0.32,0.33,0.35,0.36],
      }
    }
  }
};

// -----------------------
// BarChartDashboard component
// -----------------------
const BarChartDashboard = ({ filters = {} }) => {
  // destructure filters (defaults provided)
  const {
    category = "Produce (Fresh)",
    region = "North",
    selectedChannels = [],
    selectedStores = [],
    selectedDate,
    subCategory,
  } = filters;

  // 1) pick base dataset by category + region
  // Demo: if region specified, we pick region-specific; otherwise fallback to category->North
  const base =
    barChartDataByCategoryAndRegion[category]?.[region] ||
    barChartDataByCategoryAndRegion[category]?.North ||
    {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: { netSales: [], wasteCost: [], salvageCost: [], shrinkCost: [] }
    };

  // 2) clone arrays (don't mutate original demo data)
  const labels = [...base.labels];
  const netSales = [...(base.datasets.netSales || [])];
  const wasteCost = [...(base.datasets.wasteCost || [])];
  const salvageCost = [...(base.datasets.salvageCost || [])];
  const shrinkCost = [...(base.datasets.shrinkCost || [])];

  // 3) Demo modifications using other filters (so you can show multi-filter effect)
  // - Example: if user selected E-commerce channel, slightly increase netSales in summer months
  if (selectedChannels && selectedChannels.includes("E-commerce")) {
    for (let i = 5; i <= 7; i++) { // Jun-Jul-Aug indexes 5..7
      if (typeof netSales[i] === "number") netSales[i] = +(netSales[i] * 1.06).toFixed(2);
    }
  }

  // - Example: if a specific store is selected, reduce waste cost by 5% for that store (demo)
  if (selectedStores && selectedStores.length === 1) {
    for (let i = 0; i < wasteCost.length; i++) {
      if (typeof wasteCost[i] === "number") wasteCost[i] = +(wasteCost[i] * 0.95).toFixed(2);
    }
  }

  // - Example: if subCategory present, bump shrinkCost a bit to show subcategory effect
  if (subCategory) {
    for (let i = 0; i < shrinkCost.length; i++) {
      if (typeof shrinkCost[i] === "number") shrinkCost[i] = +(shrinkCost[i] * 1.05).toFixed(2);
    }
  }

  // Build Chart.js data object
  const barData = {
    labels,
    datasets: [
      {
        label: "Net Sales - Merchandise",
        data: netSales,
        backgroundColor: "#444744",
        type: "bar",
        yAxisID: "y",
        order: 1,
      },
      {
        label: "Total Waste Cost",
        data: wasteCost,
        type: "line",
        tension: 0.1,
        borderColor: "#EF4444",
        backgroundColor: "#EF4444",
        borderWidth: 1,
        pointRadius: 0,
        fill: false,
        yAxisID: "y1",
      },
      {
        label: "Net Salvage Cost",
        data: salvageCost,
        type: "line",
        tension: 0.4,
        borderColor: "#F59E0B",
        backgroundColor: "#F59E0B",
        borderWidth: 1,
        pointRadius: 0,
        fill: false,
        yAxisID: "y1",
      },
      {
        label: "Shrink Cost",
        data: shrinkCost,
        type: "line",
        tension: 0.4,
        borderColor: "#9CA3AF",
        backgroundColor: "#9CA3AF",
        borderWidth: 1,
        pointRadius: 0,
        fill: false,
        yAxisID: "y1",
      },
    ]
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          usePointStyle: true,
          pointStyle: "circle",
          boxWidth: 8,
          font: { size: 8, weight: "bold" },
          color: "black",
          padding: 15,
        },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            return `${context.dataset.label}: $${context.parsed.y}M`;
          },
        },
      },
      datalabels: {
        display: function (context) {
          return context.dataset.type === "bar";
        },
        anchor: "end",
        align: "end",
        offset: -4,
        formatter: function (value) {
          return `$${value}M`;
        },
        color: "#000",
        font: {
          weight: "bold",
          size: 6,
        },
      },
    },
    scales: {
      y: {
        type: "linear",
        position: "left",
        min: 0,
        max: 75,
        title: {
          display: true,
          text: "Net Sales ($M)",
          font: { size: 12 },
        },
        ticks: {
          callback: (value) => `$${value}M`,
          font: { size: 10 },
        },
        grid: {
          drawBorder: false,
          color: "#E5E7EB",
        },
      },
      y1: {
        type: "linear",
        position: "right",
        min: 0,
        max: 3,
        title: {
          display: true,
          text: "Cost Metrics ($M)",
          font: { size: 12 },
        },
        ticks: {
          callback: (value) => `$${value}M`,
          font: { size: 10 },
        },
        grid: {
          drawOnChartArea: false,
        },
      },
      x: {
        grid: { display: false },
        ticks: {
          font: { size: 10 },
        },
      },
    },
  };

  return <Bar data={barData} options={barOptions} plugins={[ChartDataLabels]} />;
};

export default BarChartDashboard;
