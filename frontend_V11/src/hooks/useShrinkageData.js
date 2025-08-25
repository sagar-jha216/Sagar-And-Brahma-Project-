import { useState, useEffect, useCallback } from 'react';
import DashboardService from '../services/dashboardService';

export const useDashboardKPIs = (initialFilters = {}) => {
  const [kpis, setKpis] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState(initialFilters);
  const [appliedFilters, setAppliedFilters] = useState({});

  const fetchKPIs = useCallback(async (filterParams = {}) => {
    setLoading(true);
    setError(null);

    try {
      const apiFilters = DashboardService.validateAndTransformFilters(filterParams);
      const response = await DashboardService.fetchDashboardKPIs(apiFilters);

      setKpis(response.kpis || []);
      setAppliedFilters(response.filters_applied || {});
    } catch (err) {
      console.error('Failed to fetch dashboard KPIs:', err);
      setError(err.message);

      // Fallback to default KPI structure
      setKpis([
        { id: "stock-accuracy", title: "Stock Accuracy", value: 0, percentage: true },
        { id: "damaged", title: "Damaged Products", value: 0, percentage: true },
        { id: "dump", title: "Dumped Products", value: 0, percentage: true },
        { id: "aged-inventory", title: "Aged Inventory", value: 0, percentage: true },
        { id: "products-expired", title: "Expired Products", value: 0, percentage: true },
        { id: "return", title: "Return Rate", value: 0, percentage: true }
      ]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchKPIs(filters);
  }, [fetchKPIs, filters]);

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

  const refreshKPIs = useCallback(() => {
    fetchKPIs(filters);
  }, [fetchKPIs, filters]);

  return {
    kpis,
    loading,
    error,
    filters,
    appliedFilters,
    updateFilters,
    applyFilters,
    clearFilters,
    refreshKPIs
  };
};
