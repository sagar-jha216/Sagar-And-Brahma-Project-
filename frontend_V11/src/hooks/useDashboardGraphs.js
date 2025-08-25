// src/hooks/useDashboardGraphs.js
import { useState, useEffect, useCallback } from 'react';
import DashboardGraphsService from '../services/dashboardGraphsService';

export const useDashboardGraphs = (initialFilters = {}) => {
  const [graphs, setGraphs] = useState({
    wastageByCategory: null,
    wasteOfCogs: null,
    supplierShrinkage: null,
    nonSellableInventory: null,
    salesVsShrinkage: null,
    skuShrinkage: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState(initialFilters);

  const fetchGraphs = useCallback(async (filterParams = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const apiFilters = DashboardGraphsService.transformFilters(filterParams);
      const response = await DashboardGraphsService.fetchDashboardGraphs(apiFilters);
      
      // Transform the raw API data into chart-ready formats
      setGraphs({
        wastageByCategory: DashboardGraphsService.transformWastageByCategory(
          response.wastage_by_merch_category
        ),
        wasteOfCogs: DashboardGraphsService.formatWasteOfCogs(
          response.waste_pct_of_cogs
        ),
        supplierShrinkage: DashboardGraphsService.transformSupplierShrinkage(
          response.suppliers_highest_shrinkage
        ),
        nonSellableInventory: DashboardGraphsService.formatNonSellableInventory(
          response.non_sellable_inventory
        ),
        salesVsShrinkage: DashboardGraphsService.transformSalesVsShrinkage(
          response.sales_vs_shrinkage_vs_salvage
        ),
        skuShrinkage: DashboardGraphsService.transformSkuShrinkage(
          response.top_10_sku_shrinkage
        )
      });
    } catch (err) {
      console.error('Failed to fetch dashboard graphs:', err);
      setError(err.message);
      
      // Set empty state on error
      setGraphs({
        wastageByCategory: { labels: [], datasets: [] },
        wasteOfCogs: { percentage: 0, value: 0, totalCogs: 0 },
        supplierShrinkage: { labels: [], datasets: [] },
        nonSellableInventory: { total: 0, breakdown: {} },
        salesVsShrinkage: { labels: [], datasets: [] },
        skuShrinkage: { labels: [], datasets: [] }
      });
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch graphs when filters change
  useEffect(() => {
    fetchGraphs(filters);
  }, [fetchGraphs, filters]);

  const updateFilters = useCallback((newFilters) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      ...newFilters
    }));
  }, []);

  const applyFilters = useCallback((filterParams) => {
    setFilters(filterParams);
  }, []);

  const clearFilters = useCallback(() => {
    setFilters({});
  }, []);

  const refreshGraphs = useCallback(() => {
    fetchGraphs(filters);
  }, [fetchGraphs, filters]);

  return {
    graphs,
    loading,
    error,
    filters,
    updateFilters,
    applyFilters,
    clearFilters,
    refreshGraphs
  };
};