/** Retail Leader Board **/


export const RetailLeaderBoardData = {
  LeaderBoardTopContent: {
    title: "Retail Leader Board",
    subtitle: "INVENTORY INBOUND TO STORE VIEW",
    description: "Offers visibility into shrinkage across stores, regions, and categories"
  },
  CommandCenterTopContent: {
    title: "Command Center",
  },
  shrinkageMetrics: [
    {
      id: 1,
      category: "Produce (Fresh)",
      percentage: "11.5%",
      value: 11.5,
      ranges: {
        low: "1%",
        medium: "7%",
        high: "15%"
      },
      distribution: {
        green: 15,
        yellow: 15,
        red: 70
      },
      icon: "Package"
    },
    {
      id: 2,
      category: "Dry Goods",
      percentage: "6.5%",
      value: 6.5,
      ranges: {
        low: "3.5%",
        medium: "6.5%",
        high: "12%"
      },
      distribution: {
        green: 45,
        yellow: 25,
        red: 30
      },
      icon: "Box"
    },
    {
      id: 3,
      category: "General Merchandise",
      percentage: "1%",
      value: 1.0,
      ranges: {
        low: "0%",
        medium: "1.8%",
        high: "5%"
      },
      distribution: {
        green: 80,
        yellow: 15,
        red: 5
      },
      icon: "ShoppingCart"
    }
  ],
  inTransit: {
    title: "In-Transit Loss Rate",
    percentage: "6%",
    value: 6.0,
    ranges: {
      low: "4%",
      medium: "7%",
      high: "15%"
    },
    distribution: {
      green: 35,
      yellow: 35,
      red: 30
    }
  },
  legend: [
    { color: "green", label: "Best in Class" },
    { color: "yellow", label: "Market" },
    { color: "red", label: "Laggard" }
  ],
  dataSource: "Benchmarking Source: AWP"
};

/***Select mockup data for Produce component select comp*/

export const selectOptions = [
  { label: "Option 1", value: "option1" },
  { label: "Option 2", value: "option2" },
  { label: "Option 3", value: "option3" },
];



export const filterOptions = {
  region: ["Region", "Northeast", "Southeast", "Midwest", "West"],
  store: ["Store", "Store 1", "Store 2", "Store 3"],
  timePeriod: ["Time Period", "This Month", "Last Month", "Last Quarter"],
  subCategory: ["Sub Category", "Apples", "Bananas", "Oranges"],
  storeChannel: ["Store Channel", "Online", "Physical"]
};

