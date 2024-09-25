import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default {
    async login(username, password) {
        const response = await api.post('/login', { username, password });
        const token = response.data.access_token;
        this.setAuthToken(token);
        localStorage.setItem('token', token);
        return token;
    },

    setAuthToken(token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },

    async register(username, password) {
        return await api.post('/register', { username, password });
    },

    logout() {
        this.clearAuthToken();
        localStorage.removeItem('token');
    },

    clearAuthToken() {
        delete api.defaults.headers.common['Authorization'];
    },

    async getDashboardData() {
        try {
            const response = await api.get('/dashboard');
            return response.data;
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            throw error;
        }
    },
};