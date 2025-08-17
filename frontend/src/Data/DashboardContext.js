import { createContext, useContext, useState } from 'react';

const DashboardContext = createContext(undefined);

export const useDashboard = () => {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
};

const initialFilters = {
  region: 'Region',
  store: 'Store',
  timePeriod: 'Time Period',
  subCategory: 'Sub Category',
  storeChannel: 'Store Channel'
};

const metricsData = [
  {
    id: 'stock-accuracy',
    title: 'Stock Inventory Accuracy %',
    value: '94.8%',
    percentage: 94.8,
    achieved: '94.8'
  },
  {
    id: 'damaged',
    title: 'Damaged %',
    value: 'NA',
    percentage: 0
  },
  {
    id: 'surge',
    title: 'Surge %',
    value: '3.8%',
    percentage: 3.8,
    comparison: 'vs PY: 15.2%'
  },
  {
    id: 'aged-inventory',
    title: 'Aged Inventory %',
    value: '3.5%',
    percentage: 3.5,
    comparison: 'vs PY: 15.2%',
    hasChart: true
  },
  {
    id: 'products-expired',
    title: '% Of Products Expired',
    value: '6%',
    percentage: 6,
    comparison: 'vs PY: 15.2%'
  },
  {
    id: 'shrinkage-sku',
    title: 'Shrinkage to SKU',
    value: '80%',
    percentage: 80,
    comparison: 'Due to 30 SKU'
  },
  {
    id: 'return',
    title: 'Return %',
    value: '1.0%',
    percentage: 10,
    comparison: 'vs PY: 15.2%'
  }
];

const chartData = {
  wastageByCategory: [
    { name: 'Jan', value: 120 },
    { name: 'Feb', value: 150 },
    { name: 'Mar', value: 180 },
    { name: 'Apr', value: 200 },
    { name: 'May', value: 160 },
    { name: 'Jun', value: 140 },
    { name: 'Jul', value: 190 },
    { name: 'Aug', value: 210 },
    { name: 'Sep', value: 180 },
    { name: 'Oct', value: 160 },
    { name: 'Nov', value: 140 },
    { name: 'Dec', value: 120 }
  ],
  wasteOfCogs: {
    value: 2996,
    total: 40845
  },
  suppliers: [
    { name: 'BIG RIVER', percentage: 18 },
    { name: 'CHELAN', percentage: 14 },
    { name: 'DOLE SUPREME', percentage: 13 },
    { name: 'NORTH BAY', percentage: 12 },
    { name: 'NATIVE SUN', percentage: 11 }
  ],
  inventoryOverview: {
    damaged: 38,
    expired: 62,
    total: 5265
  },
  salesVsShrinkage: [
    { month: 'Jan', sales: 280, shrinkage: 20, salvage: 15 },
    { month: 'Feb', sales: 320, shrinkage: 25, salvage: 18 },
    { month: 'Mar', sales: 360, shrinkage: 30, salvage: 22 },
    { month: 'Apr', sales: 400, shrinkage: 35, salvage: 25 },
    { month: 'May', sales: 320, shrinkage: 25, salvage: 18 },
    { month: 'Jun', sales: 280, shrinkage: 20, salvage: 15 },
    { month: 'Jul', sales: 380, shrinkage: 30, salvage: 22 },
    { month: 'Aug', sales: 420, shrinkage: 35, salvage: 25 },
    { month: 'Sep', sales: 360, shrinkage: 30, salvage: 22 },
    { month: 'Oct', sales: 320, shrinkage: 25, salvage: 18 },
    { month: 'Nov', sales: 280, shrinkage: 20, salvage: 15 },
    { month: 'Dec', sales: 240, shrinkage: 15, salvage: 12 }
  ],
  topSkus: [
    { name: 'Organic Fuji Apple (1 lb bag)', percentage: 23 },
    { name: 'Large Banana/Mango', percentage: 20 },
    { name: 'Fresh Strawberry', percentage: 19 },
    { name: 'Organic Grapes', percentage: 18 },
    { name: 'Cut Pineapple Cups', percentage: 17 },
    { name: 'Conventional Apples', percentage: 16 },
    { name: 'Avocado Organic', percentage: 15 }
  ]
};

export const DashboardProvider = ({ children }) => {
  const [filters, setFilters] = useState(initialFilters);
  const lastRefresh = "22/06/2020 8:01:43 AM CT";

  const updateFilter = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const clearFilters = () => {
    setFilters(initialFilters);
  };

  const value = {
    filters,
    updateFilter,
    clearFilters,
    metrics: metricsData,
    chartData,
    lastRefresh
  };

  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  );
};
