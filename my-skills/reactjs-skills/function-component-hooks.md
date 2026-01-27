---
name: Function Component with Hooks
description: Hướng dẫn tạo Function Component với Hooks trong React
---

# Function Component với Hooks

## Cấu trúc cơ bản

```jsx
import React, { useState } from 'react';

const MyComponent = ({ title }) => {
    const [count, setCount] = useState(0);

    const handleClick = () => {
        setCount(count + 1);
    };

    return (
        <div>
            <h1>Hello, {title}</h1>
            <p>Count: {count}</p>
            <button onClick={handleClick}>Increment</button>
        </div>
    );
};

export default MyComponent;
```

## useState Hook

```jsx
import { useState } from 'react';

const StateExample = () => {
    // Primitive state
    const [count, setCount] = useState(0);
    const [name, setName] = useState('');
    const [isActive, setIsActive] = useState(false);

    // Object state
    const [user, setUser] = useState({ name: '', email: '' });

    // Array state
    const [items, setItems] = useState([]);

    // Lazy initialization (expensive computation)
    const [data, setData] = useState(() => computeExpensiveValue());

    // Update state
    const increment = () => {
        setCount(count + 1);
        // Hoặc functional update (an toàn với async)
        setCount(prev => prev + 1);
    };

    // Update object (phải spread để merge)
    const updateUser = () => {
        setUser(prev => ({ ...prev, name: 'New Name' }));
    };

    // Update array
    const addItem = (item) => {
        setItems(prev => [...prev, item]);
    };

    const removeItem = (id) => {
        setItems(prev => prev.filter(item => item.id !== id));
    };

    return <div>...</div>;
};
```

## useEffect Hook

```jsx
import { useState, useEffect } from 'react';

const EffectExample = ({ userId }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // 1. Chạy mỗi render (không có dependency array)
    useEffect(() => {
        console.log('Runs every render');
    });

    // 2. Chạy một lần khi mount (empty dependency array)
    useEffect(() => {
        console.log('Runs once on mount');
        fetchInitialData();
    }, []);

    // 3. Chạy khi dependency thay đổi
    useEffect(() => {
        console.log('userId changed:', userId);
        fetchUser(userId);
    }, [userId]);

    // 4. Cleanup function
    useEffect(() => {
        const subscription = subscribeToData(userId);
        
        return () => {
            // Cleanup khi component unmount hoặc trước khi effect chạy lại
            subscription.unsubscribe();
        };
    }, [userId]);

    // 5. Async trong useEffect
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await fetch(`/api/users/${userId}`);
                const data = await response.json();
                setUser(data);
            } catch (error) {
                console.error('Error:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [userId]);

    return <div>...</div>;
};
```

## useRef Hook

```jsx
import { useRef, useEffect } from 'react';

const RefExample = () => {
    // DOM reference
    const inputRef = useRef(null);
    
    // Mutable value (không trigger re-render)
    const countRef = useRef(0);
    const timerRef = useRef(null);

    const focusInput = () => {
        inputRef.current.focus();
    };

    const startTimer = () => {
        timerRef.current = setInterval(() => {
            countRef.current += 1;
            console.log('Count:', countRef.current);
        }, 1000);
    };

    const stopTimer = () => {
        clearInterval(timerRef.current);
    };

    // Cleanup timer on unmount
    useEffect(() => {
        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, []);

    return (
        <>
            <input ref={inputRef} />
            <button onClick={focusInput}>Focus</button>
        </>
    );
};
```

## useMemo và useCallback

```jsx
import { useMemo, useCallback, useState } from 'react';

const MemoExample = ({ items, filter }) => {
    const [count, setCount] = useState(0);

    // useMemo - cache kết quả tính toán
    const filteredItems = useMemo(() => {
        console.log('Filtering items...');
        return items.filter(item => item.includes(filter));
    }, [items, filter]); // Chỉ recalculate khi items hoặc filter thay đổi

    const expensiveValue = useMemo(() => {
        return computeExpensiveValue(count);
    }, [count]);

    // useCallback - cache function reference
    const handleClick = useCallback(() => {
        console.log('Clicked!');
    }, []); // Function không đổi

    const handleItemClick = useCallback((id) => {
        console.log('Item:', id, 'Count:', count);
    }, [count]); // Function mới khi count thay đổi

    return (
        <div>
            {filteredItems.map(item => (
                <ChildComponent 
                    key={item.id} 
                    onClick={handleClick} 
                />
            ))}
        </div>
    );
};
```

## useContext Hook

```jsx
import { createContext, useContext, useState } from 'react';

// 1. Create context
const ThemeContext = createContext();

// 2. Provider component
const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState('light');
    
    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

// 3. Custom hook for consuming context
const useTheme = () => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within ThemeProvider');
    }
    return context;
};

// 4. Use in component
const ThemedButton = () => {
    const { theme, toggleTheme } = useTheme();
    
    return (
        <button 
            onClick={toggleTheme}
            style={{ background: theme === 'dark' ? '#333' : '#fff' }}
        >
            Toggle Theme
        </button>
    );
};
```

## useReducer Hook

```jsx
import { useReducer } from 'react';

// Reducer function
const reducer = (state, action) => {
    switch (action.type) {
        case 'INCREMENT':
            return { ...state, count: state.count + 1 };
        case 'DECREMENT':
            return { ...state, count: state.count - 1 };
        case 'SET_NAME':
            return { ...state, name: action.payload };
        case 'RESET':
            return initialState;
        default:
            return state;
    }
};

const initialState = { count: 0, name: '' };

const ReducerExample = () => {
    const [state, dispatch] = useReducer(reducer, initialState);

    return (
        <div>
            <p>Count: {state.count}</p>
            <button onClick={() => dispatch({ type: 'INCREMENT' })}>+</button>
            <button onClick={() => dispatch({ type: 'DECREMENT' })}>-</button>
            <input 
                value={state.name}
                onChange={(e) => dispatch({ type: 'SET_NAME', payload: e.target.value })}
            />
        </div>
    );
};
```
