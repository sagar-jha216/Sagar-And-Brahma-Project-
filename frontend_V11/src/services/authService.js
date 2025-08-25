const API_BASE_URL = 'http://localhost:8000';

class AuthService {
  static getToken() {
    return localStorage.getItem('authToken');
  }

  static getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  static isAuthenticated() {
    return !!this.getToken();
  }

  static logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }

  static async verifyToken() {
    const token = this.getToken();
    if (!token) return false;

    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  static getAuthHeaders() {
    const token = this.getToken();
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  }

  static async fetchShrinkageMetrics() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/retail-leaderboard/shrinkage-metrics`, {
        headers: {
          'Content-Type': 'application/json',
          ...this.getAuthHeaders(),
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch shrinkage metrics');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching shrinkage metrics:', error);
      throw error;
    }
  }

  static async fetchDashboardSummary() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/retail-leaderboard/dashboard-summary`, {
        headers: {
          'Content-Type': 'application/json',
          ...this.getAuthHeaders(),
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch dashboard summary');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching dashboard summary:', error);
      throw error;
    }
  }
}

export default AuthService;
