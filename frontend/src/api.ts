import axios, { AxiosResponse } from 'axios';

const API_URL = '/api'

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface LoginResponse {
    access_token: string;
}

export interface Customer {
    id: number;
    name: string;
    email: string;
    order_count?: number;
}

export interface InventoryItem {
    id: number;
    name: string;
    order_count?: number;
    price: number;
    quantity: number;
    reorder_level: number;
}

export interface Order {
    id: number;
    customer: string;
    date: string;
    total: number;
    items: { name: string; quantity: number }[];
}

export interface DashboardData {
    message: string;
    stats: {
        customer_count: number;
        inventory_count: number;
        order_count: number;
    };
    recent_orders: Array<{
        id: number;
        customer: string;
        date: string;
        total: number;
    }>;
}

const ApiService = {
    async login(username: string, password: string): Promise<string> {
        const response = await api.post<LoginResponse>('/login', { username, password });
        const token = response.data.access_token;
        this.setAuthToken(token);
        localStorage.setItem('token', token);
        return token;
    },

    setAuthToken(token: string): void {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },

    async register(username: string, password: string): Promise<AxiosResponse> {
        return await api.post('/register', { username, password });
    },

    logout(): void {
        this.clearAuthToken();
        localStorage.removeItem('token');
    },

    clearAuthToken(): void {
        delete api.defaults.headers.common['Authorization'];
    },

    async getDashboardData(): Promise<DashboardData> {
        const response = await api.get<DashboardData>('/dashboard');
        return response.data;
    },

    // Customer methods
    async getCustomers(): Promise<Customer[]> {
        const response = await api.get<Customer[]>('/customers');
        return response.data;
    },

    async createCustomer(customer: Omit<Customer, 'id'>): Promise<Customer> {
        const response = await api.post<Customer>('/customers', customer);
        return response.data;
    },

    async updateCustomer(id: number, customer: Partial<Customer>): Promise<void> {
        await api.put(`/customers/${id}`, customer);
    },

    async deleteCustomer(id: number): Promise<void> {
        await api.delete(`/customers/${id}`);
    },

    // Inventory methods
    async getInventory(): Promise<InventoryItem[]> {
        const response = await api.get<InventoryItem[]>('/inventory');
        return response.data;
    },

    async createInventoryItem(item: Omit<InventoryItem, 'id'>): Promise<InventoryItem> {
        const response = await api.post<InventoryItem>('/inventory', item);
        return response.data;
    },

    async updateInventoryItem(id: number, item: Partial<InventoryItem>): Promise<void> {
        await api.put(`/inventory/${id}`, item);
    },

    async deleteInventoryItem(id: number): Promise<void> {
        await api.delete(`/inventory/${id}`);
    },

    // Order methods
    async getOrders(): Promise<Order[]> {
        const response = await api.get<Order[]>('/orders');
        return response.data;
    },

    async createOrder(order: { customer_id: number, items: { id: number, quantity: number }[] }): Promise<Order> {
        const response = await api.post<Order>('/orders', order);
        return response.data;
    },

    async deleteOrder(id: number): Promise<void> {
        await api.delete(`/orders/${id}`);
    },
};

export default ApiService;