// data.js
export const shrinkageData = [
  { category: "Produce (Fresh)", percentage: 11.5, status: "laggard", trend: "down" },
  { category: "Dry Goods", percentage: 6.5, status: "median", trend: "up" },
  { category: "General Merchandise", percentage: 1.0, status: "best", trend: "up" },
  { category: "In-Transit Loss Rate", percentage: 6.0, status: "median", trend: "down" },
];

export const statusGradients = {
  best: "bg-gradient-to-r from-green-400 to-green-600",
  median: "bg-gradient-to-r from-yellow-400 to-yellow-600",
  laggard: "bg-gradient-to-r from-red-400 to-red-600",
};

export const trendIcons = {
  up: "▲",
  down: "▼",
};
