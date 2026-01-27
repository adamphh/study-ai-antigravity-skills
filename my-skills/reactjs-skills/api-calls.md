---
name: API Calls and Data Fetching
description: Hướng dẫn gọi API trong React (Class và Function Component)
---

# API Calls và Data Fetching

## Class Component - Fetch Data

```jsx
import React, { Component } from 'react';

class UserList extends Component {
    state = {
        users: [],
        loading: true,
        error: null
    };

    componentDidMount() {
        this.fetchUsers();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.filter !== this.props.filter) {
            this.fetchUsers();
        }
    }

    fetchUsers = async () => {
        this.setState({ loading: true, error: null });
        try {
            const response = await fetch('/api/users');
            if (!response.ok) throw new Error('Failed to fetch');
            const users = await response.json();
            this.setState({ users, loading: false });
        } catch (error) {
            this.setState({ error: error.message, loading: false });
        }
    };

    render() {
        const { users, loading, error } = this.state;

        if (loading) return <div>Loading...</div>;
        if (error) return <div>Error: {error}</div>;

        return (
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.name}</li>
                ))}
            </ul>
        );
    }
}
```

## Function Component - useEffect

```jsx
import { useState, useEffect } from 'react';

const UserList = ({ filter }) => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();

        const fetchUsers = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await fetch(`/api/users?filter=${filter}`, {
                    signal: controller.signal
                });
                if (!response.ok) throw new Error('Failed to fetch');
                const data = await response.json();
                setUsers(data);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError(err.message);
                }
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();

        return () => controller.abort();
    }, [filter]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <ul>
            {users.map(user => <li key={user.id}>{user.name}</li>)}
        </ul>
    );
};
```

## Custom useFetch Hook

```jsx
const useFetch = (url) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();

        const fetchData = async () => {
            try {
                const response = await fetch(url, { signal: controller.signal });
                if (!response.ok) throw new Error('Failed');
                const result = await response.json();
                setData(result);
            } catch (err) {
                if (err.name !== 'AbortError') setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        return () => controller.abort();
    }, [url]);

    return { data, loading, error };
};

// Usage
const Users = () => {
    const { data: users, loading, error } = useFetch('/api/users');
    if (loading) return <span>Loading...</span>;
    if (error) return <span>Error: {error}</span>;
    return users.map(u => <div key={u.id}>{u.name}</div>);
};
```

## POST/PUT/DELETE Requests

```jsx
const useApi = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const request = async (url, options = {}) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(url, {
                headers: { 'Content-Type': 'application/json' },
                ...options,
                body: options.body ? JSON.stringify(options.body) : undefined
            });
            if (!response.ok) throw new Error('Request failed');
            return await response.json();
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const get = (url) => request(url);
    const post = (url, body) => request(url, { method: 'POST', body });
    const put = (url, body) => request(url, { method: 'PUT', body });
    const del = (url) => request(url, { method: 'DELETE' });

    return { get, post, put, del, loading, error };
};

// Usage
const CreateUser = () => {
    const { post, loading, error } = useApi();

    const handleSubmit = async (formData) => {
        try {
            const newUser = await post('/api/users', formData);
            console.log('Created:', newUser);
        } catch (err) {
            // Error handled in hook
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            {error && <div>Error: {error}</div>}
            <button disabled={loading}>
                {loading ? 'Creating...' : 'Create User'}
            </button>
        </form>
    );
};
```

## Axios Example

```jsx
import axios from 'axios';

// Create instance
const api = axios.create({
    baseURL: '/api',
    timeout: 10000,
    headers: { 'Content-Type': 'application/json' }
});

// Interceptors
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

api.interceptors.response.use(
    response => response.data,
    error => {
        if (error.response?.status === 401) {
            // Handle unauthorized
        }
        return Promise.reject(error);
    }
);

// Usage in component
const Users = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const source = axios.CancelToken.source();
        
        api.get('/users', { cancelToken: source.token })
            .then(setUsers)
            .catch(err => {
                if (!axios.isCancel(err)) console.error(err);
            });

        return () => source.cancel();
    }, []);

    return <div>{users.map(u => <span key={u.id}>{u.name}</span>)}</div>;
};
```
