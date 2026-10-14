---
name: Context API and State Management
description: Hướng dẫn quản lý state với Context API
---

# Context API và State Management

## Class Component với Context

```jsx
import React, { Component, createContext } from 'react';

// Create Context
const UserContext = createContext();

// Provider as Class Component
class UserProvider extends Component {
    state = {
        user: null,
        loading: false
    };

    login = async (credentials) => {
        this.setState({ loading: true });
        const user = await authService.login(credentials);
        this.setState({ user, loading: false });
    };

    logout = () => {
        this.setState({ user: null });
    };

    render() {
        return (
            <UserContext.Provider value={{
                user: this.state.user,
                loading: this.state.loading,
                login: this.login,
                logout: this.logout
            }}>
                {this.props.children}
            </UserContext.Provider>
        );
    }
}

// Consumer as Class Component
class Profile extends Component {
    static contextType = UserContext;

    render() {
        const { user, logout } = this.context;
        return (
            <div>
                <p>Welcome, {user?.name}</p>
                <button onClick={logout}>Logout</button>
            </div>
        );
    }
}

// Or using Consumer
class ProfileWithConsumer extends Component {
    render() {
        return (
            <UserContext.Consumer>
                {({ user, logout }) => (
                    <div>
                        <p>Welcome, {user?.name}</p>
                        <button onClick={logout}>Logout</button>
                    </div>
                )}
            </UserContext.Consumer>
        );
    }
}
```

## Function Component với Context

```jsx
import { createContext, useContext, useState, useCallback } from 'react';

// Create Context
const AuthContext = createContext(null);

// Provider Component
const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(false);

    const login = useCallback(async (credentials) => {
        setLoading(true);
        try {
            const userData = await authService.login(credentials);
            setUser(userData);
        } finally {
            setLoading(false);
        }
    }, []);

    const logout = useCallback(() => {
        setUser(null);
        authService.logout();
    }, []);

    const value = { user, loading, login, logout, isAuthenticated: !!user };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom Hook
const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

// Usage
const Profile = () => {
    const { user, logout, isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }

    return (
        <div>
            <p>Welcome, {user.name}</p>
            <button onClick={logout}>Logout</button>
        </div>
    );
};
```

## Multiple Contexts

```jsx
// contexts/ThemeContext.js
const ThemeContext = createContext();
const useTheme = () => useContext(ThemeContext);

const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState('light');
    const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light');
    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

// contexts/CartContext.js
const CartContext = createContext();
const useCart = () => useContext(CartContext);

const CartProvider = ({ children }) => {
    const [items, setItems] = useState([]);
    
    const addItem = (item) => setItems(prev => [...prev, item]);
    const removeItem = (id) => setItems(prev => prev.filter(i => i.id !== id));
    const total = items.reduce((sum, item) => sum + item.price, 0);

    return (
        <CartContext.Provider value={{ items, addItem, removeItem, total }}>
            {children}
        </CartContext.Provider>
    );
};

// App.js - Combine providers
const App = () => (
    <AuthProvider>
        <ThemeProvider>
            <CartProvider>
                <Router>
                    <AppRoutes />
                </Router>
            </CartProvider>
        </ThemeProvider>
    </AuthProvider>
);
```

## Context with useReducer

```jsx
import { createContext, useContext, useReducer } from 'react';

// Actions
const ACTIONS = {
    ADD_TO_CART: 'ADD_TO_CART',
    REMOVE_FROM_CART: 'REMOVE_FROM_CART',
    UPDATE_QUANTITY: 'UPDATE_QUANTITY',
    CLEAR_CART: 'CLEAR_CART'
};

// Reducer
const cartReducer = (state, action) => {
    switch (action.type) {
        case ACTIONS.ADD_TO_CART:
            const exists = state.items.find(i => i.id === action.payload.id);
            if (exists) {
                return {
                    ...state,
                    items: state.items.map(i => 
                        i.id === action.payload.id 
                            ? { ...i, quantity: i.quantity + 1 }
                            : i
                    )
                };
            }
            return {
                ...state,
                items: [...state.items, { ...action.payload, quantity: 1 }]
            };

        case ACTIONS.REMOVE_FROM_CART:
            return {
                ...state,
                items: state.items.filter(i => i.id !== action.payload)
            };

        case ACTIONS.CLEAR_CART:
            return { ...state, items: [] };

        default:
            return state;
    }
};

// Context
const CartContext = createContext();

const CartProvider = ({ children }) => {
    const [state, dispatch] = useReducer(cartReducer, { items: [] });

    const addToCart = (product) => dispatch({ type: ACTIONS.ADD_TO_CART, payload: product });
    const removeFromCart = (id) => dispatch({ type: ACTIONS.REMOVE_FROM_CART, payload: id });
    const clearCart = () => dispatch({ type: ACTIONS.CLEAR_CART });

    const total = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    return (
        <CartContext.Provider value={{ 
            items: state.items, 
            total,
            addToCart, 
            removeFromCart, 
            clearCart 
        }}>
            {children}
        </CartContext.Provider>
    );
};

const useCart = () => useContext(CartContext);
```
