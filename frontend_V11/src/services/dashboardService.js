// Frontend\src\services\dashboardService.js
const API_BASE_URL = process.env.REACT_APP_BASE_URL || 'http://localhost:8000';

class DashboardService {
  /**
   * Fetch dashboard KPIs with filters and enhanced error handling
   */
  static async fetchDashboardKPIs(filters = {}) {
    try {
      const queryParams = new URLSearchParams();
      const validFilters = this.validateAndTransformFilters(filters);

      Object.entries(validFilters).forEach(([key, value]) => {
        if (value && value !== '' && value !== 'All' && value !== null) {
          queryParams.append(key, value);
        }
      });

      // const url = `${API_BASE_URL}/analytics/kpis/formatted${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
      const url = `${API_BASE_URL}/analytics/kpis/formatted`;

      console.log('🚀 Dashboard KPI Request:', {
        url,
        filters: validFilters,
        queryParams: queryParams.toString()
      });

const category=filters?.category==="Produce (Fresh)" ? "Fresh Produce" :filters?.category=== "General Merchandising" ? "General Merchandise":"Dry Goods" ;// For Mapping of name with DB
// const subCategory=filters?.subCategory==="Fruits & Vegetables" ? "Fruits & Vegetable" :filters?.subCategory
      
const validFilters1 = {
        Category: category || "Fresh Produce",
        Sub_Category:filters?.subCategory,
        Region_Historical:filters?.region || "North",
        // Store_ID: ["STR_025", "STR_017"],
        Store_Channel: filters?.selectedChannels,
        // Start_Date: "2023-01-01",    // -> will use in future 
        // End_Date: "2023-01-31"      // -> will use in future 
      };

      console.log(filters)

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
      // ✅ Transform flat KPI response into array format for UI
      const kpis = [
        { id: 'stock-accuracy', title: 'Stock Inventory Accuracy %', value: data["Inventory_Accuracy"], percentage: true,       doughnutchartData: [data["Inventory_Accuracy"],100-data["Inventory_Accuracy"]],
        date: "15 Jul ‘25", },
        { id: 'damaged', title: 'Damaged', value: data["Damage_%"], percentage: true,  doughnutchartData: [data["Damage_%"], 100 - data["Damage_%"]],
        vs: -0.3, },
        { id: 'dump', title: 'Dumped %', value: data["Dump_%"], percentage: true, doughnutchartData: [data["Dump_%"], 100 - data["Dump_%"]], vs: -0.8  },
        { id: 'aged-inventory', title: 'Aged Inventory %', value: data["Aged_%"], percentage: true,      BarChartdata: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [{ label: "Sales", data: [210, 260, 240, 280] }],
        },
        vs: 1.9, },
        { id: 'products-expired', title: '% Of Products Expired', value: data["Expired_%"], percentage: true ,   doughnutchartData: [data["Expired_%"], 100- data["Expired_%"]],
        vs: 1.7,},
        { id: 'shrinkage%-to-sku', title: 'Shrinkage% to SKU', value: data["Shrinkage_%"], percentage: true,   shrinkageText: "Shrinkage",
        labelSKUDetails: 72, },
        { id: 'return', title: 'Return %', value: data["Return_%"], percentage: true ,      doughnutchartData: [data["Return_%"], 100 - data["Return_%"]],
        vs: 1.5,}
      ];

      console.log('✅ Dashboard KPI Response:', {
        status: data.status,
        kpisCount: kpis.length,
        filtersApplied: data.filters_applied,
        debugInfo: data.debug_info
      });

      return {
        status: 'success',
        kpis,
        filters_applied: data.filters_applied || {},
        debug_info: data.debug_info || {}
      };
    } catch (error) {
      console.error('❌ Error fetching dashboard KPIs:', error);
      throw error;
    }
  }

  /**
   * Validate and transform filters from frontend format to API format
   */
  static validateAndTransformFilters(frontendFilters) {
    const apiFilters = {};

    const filterMapping = {
      category: {
        apiKey: 'category',
        validator: (value) => ['Produce (Fresh)', 'Dry Goods', 'General Merchandise'].includes(value),
        description: 'Product category filter'
      },
      region: {
        apiKey: 'region',
        validator: (value) => ['North', 'South', 'East', 'West'].includes(value),
        description: 'Store region filter'
      },
      selectedStores: {
        apiKey: 'store_id',
        validator: (value) => Array.isArray(value) && value.length > 0,
        transform: (value) => value.join(','), // assuming multiple store IDs are allowed
        description: 'Store ID filter'
      }, 
      timePeriod: {
        apiKey: 'time_period',
        validator: (value) => {
          if (!value) return false;
          const date = new Date(value);
          return !isNaN(date.getTime());
        },
        transform: (value) => {
          const date = new Date(value);
          return date.toISOString().split('T')[0];
        },
        description: 'Filter by Received_Date in inventory'
      },
      subCategory: {
        apiKey: 'sub_category',
        validator: (value) => value && value.length > 0,
        description: 'Sub category filter'
      },
      selectedChannels: {
        apiKey: 'store_channel',
        validator: (value) => Array.isArray(value) && value.length > 0,
        transform: (value) => value.join(','), // assuming API accepts comma-separated string
        description: 'Store channel filter'
      }
    };


    Object.entries(frontendFilters).forEach(([key, value]) => {
      const mapping = filterMapping[key];
      if (mapping && value && value !== '' && value !== 'All') {
        if (mapping.validator && !mapping.validator(value)) {
          console.warn(`Invalid filter value for ${key}: ${value}. ${mapping.description}`);
          return;
        }

        const finalValue = mapping.transform ? mapping.transform(value) : value;
        apiFilters[mapping.apiKey] = finalValue;

        console.log(`✅ Filter mapped: ${key} -> ${mapping.apiKey} = ${finalValue}`);
      }
    });

    return apiFilters;
  }

  /**
   * Debug API endpoint for troubleshooting
   */
  static async debugKpiData(filters = {}) {
    try {
      const queryParams = new URLSearchParams();
      const validFilters = this.validateAndTransformFilters(filters);

      Object.entries(validFilters).forEach(([key, value]) => {
        if (value) queryParams.append(key, value);
      });

      const url = `${API_BASE_URL}/analytics/kpis/debug${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;

      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`Debug API error! status: ${response.status}`);
      }

      const debugData = await response.json();
      console.log('Debug KPI Data:', debugData);

      return debugData;
    } catch (error) {
      console.error('Debug API request failed:', error);
      throw error;
    }
  }

  /**
   * Get filter descriptions for UI help text
   */
  static getFilterDescriptions() {
    return {
      category: "Product category: Fresh Produce, Dry Goods, or General Merchandise",
      region: "Store region: North, South, East, or West",
      subCategory: "Sub category like 'Fruits & Vegetables' - filters product names",
      timePeriod: "Date filter for when products were received",
      store: "Specific store ID to filter data",
      storeChannel: "Store channel: Online or Physical (future use)"
    };
  }
}

export default DashboardService;
