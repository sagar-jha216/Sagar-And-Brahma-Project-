// src/services/dashboardGraphsService.js
const API_BASE_URL = process.env.REACT_APP_BASE_URL || 'http://localhost:8000';

class DashboardGraphsService {
  /**
   * Fetch dashboard graphs with filters
   */
  static async fetchDashboardGraphs(filters = {}) {
    try {
      const queryParams = new URLSearchParams();
      
      // Add non-empty filters to query params
      Object.entries(filters).forEach(([key, value]) => {
        if (value && value !== '' && value !== 'All' && value !== null) {
          queryParams.append(key, value);
        }
      });
      const category=filters?.category==="Produce (Fresh)" ? "Fresh Produce" :filters?.category=== "General Merchandising" ? "General Merchandise":"Dry Goods" ;// For Mapping of name with DB

      const validFilters1 = {
        Category: category || "Fresh Produce",
        Sub_Category:filters?.subCategory,
        Region_Historical:filters?.region || "North",
        // Store_ID: ["STR_025", "STR_017"],
        Store_Channel: filters?.selectedChannels,
        // Start_Date: "2023-01-01",    // -> will use in future 
        // End_Date: "2023-01-31"      // -> will use in future 
      };

      const url = `${API_BASE_URL}/analytics/dashboard`;
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(validFilters1), // 👈 This sends the actual data
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching dashboard graphs:', error);
      throw error;
    }
  }

  /**
   * Transform filters from frontend format to API format
   */
  static transformFilters(frontendFilters) {
    const apiFilters = {};

    // Map frontend filter names to API parameter names
    const filterMapping = {
      category: 'category',
      region: 'region', 
      store: 'store_id',
      timePeriod: 'time_period',
      subCategory: 'sub_category'
    };

    Object.entries(frontendFilters).forEach(([key, value]) => {
      const apiKey = filterMapping[key];
      if (apiKey && value && value !== '' && value !== 'All') {
        apiFilters[apiKey] = value;
      }
    });

    return apiFilters;
  }

  /**
   * Transform wastage by merch category data for chart consumption
   */
  static transformWastageByCategory(data) {
    if (!data || !Array.isArray(data)) return { labels: [], datasets: [] };

    return {
      labels: data.map(item => item.Category),
      datasets: [{
        label: 'Wastage Percentage',
        data: data.map(item => item.Wastage_Percentage || 0),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
          '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
        ],
        borderWidth: 1
      }]
    };
  }

  /**
   * Transform supplier shrinkage data for chart consumption
   */
  static transformSupplierShrinkage(data) {
    if (!data || !Array.isArray(data)) return { labels: [], datasets: [] };

    return {
      labels: data.map(item => item.Supplier_Name),
      datasets: [{
        label: 'Shrinkage Percentage',
        data: data.map(item => item.Shrinkage_Percentage || 0),
        backgroundColor: '#FF6384',
        borderColor: '#FF6384',
        borderWidth: 1
      }]
    };
  }

  /**
   * Transform SKU shrinkage data for chart consumption
   */
  static transformSkuShrinkage(data) {
    if (!data || !Array.isArray(data)) return { labels: [], datasets: [] };

    return {
      labels: data.map(item => item.Product_Name),
      datasets: [{
        label: 'Shrinkage Percentage',
        data: data.map(item => item.Shrinkage_Percentage || 0),
        backgroundColor: '#36A2EB',
        borderColor: '#36A2EB',
        borderWidth: 1
      }]
    };
  }

  /**
   * Transform sales vs shrinkage vs salvage data for pie chart
   */
  static transformSalesVsShrinkage(data) {
    if (!data) return { labels: [], datasets: [] };

    return {
      labels: ['Sales', 'Shrinkage', 'Salvage'],
      datasets: [{
        data: [
          data.sales_percentage || 0,
          data.shrinkage_percentage || 0,
          data.salvage_percentage || 0
        ],
        backgroundColor: ['#4BC0C0', '#FF6384', '#FFCE56'],
        borderWidth: 1
      }]
    };
  }

  /**
   * Format non-sellable inventory data
   */
  static formatNonSellableInventory(data) {
    if (!data) return { total: 0, breakdown: {} };

    return {
      total: data.total_non_sellable || 0,
      breakdown: {
        damaged: data.damaged_units || 0,
        dumped: data.dump_units || 0,
        expired: data.expired_units || 0
      }
    };
  }

  /**
   * Format waste percentage of COGS
   */
  static formatWasteOfCogs(data) {
    if (!data) return { percentage: 0, value: 0, totalCogs: 0 };

    return {
      percentage: data.waste_percentage || 0,
      value: data.waste_value || 0,
      totalCogs: data.total_cogs || 0
    };
  }
}

export default DashboardGraphsService;