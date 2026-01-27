---
name: Custom Hooks
description: Hướng dẫn tạo Custom Hooks trong React
---

# Custom Hooks trong React

Custom hooks cho phép tái sử dụng logic giữa các components.

## Quy tắc đặt tên

- Tên hook **phải** bắt đầu bằng `use`
- VD: `useLocalStorage`, `useFetch`, `useDebounce`

## 1. useFetch - Fetch Data

```jsx
import { useState, useEffect } from 'react';

const useFetch = (url, options = {}) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();

        const fetchData = async () => {
            setLoading(true);
            setError(null);

            try {
                const response = await fetch(url, {
                    ...options,
                    signal: controller.signal
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                setData(result);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError(err.message);
                }
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
const UserList = () => {
    const { data: users, loading, error } = useFetch('/api/users');

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
};
```

## 2. useLocalStorage

```jsx
import { useState, useEffect } from 'react';

const useLocalStorage = (key, initialValue) => {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error(error);
            return initialValue;
        }
    });

    const setValue = (value) => {
        try {
            const valueToStore = value instanceof Function 
                ? value(storedValue) 
                : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error(error);
        }
    };

    return [storedValue, setValue];
};

// Usage
const Settings = () => {
    const [theme, setTheme] = useLocalStorage('theme', 'light');
    
    return (
        <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
            Theme: {theme}
        </button>
    );
};
```

## 3. useDebounce

```jsx
import { useState, useEffect } from 'react';

const useDebounce = (value, delay = 500) => {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => clearTimeout(timer);
    }, [value, delay]);

    return debouncedValue;
};

// Usage - Search
const SearchInput = () => {
    const [search, setSearch] = useState('');
    const debouncedSearch = useDebounce(search, 300);

    useEffect(() => {
        if (debouncedSearch) {
            fetchSearchResults(debouncedSearch);
        }
    }, [debouncedSearch]);

    return <input value={search} onChange={e => setSearch(e.target.value)} />;
};
```

## 4. useToggle

```jsx
import { useState, useCallback } from 'react';

const useToggle = (initialValue = false) => {
    const [value, setValue] = useState(initialValue);

    const toggle = useCallback(() => setValue(v => !v), []);
    const setTrue = useCallback(() => setValue(true), []);
    const setFalse = useCallback(() => setValue(false), []);

    return { value, toggle, setTrue, setFalse };
};

// Usage
const Modal = () => {
    const { value: isOpen, toggle, setFalse: close } = useToggle(false);
    
    return (
        <>
            <button onClick={toggle}>Toggle Modal</button>
            {isOpen && <div className="modal"><button onClick={close}>Close</button></div>}
        </>
    );
};
```

## 5. useClickOutside

```jsx
import { useEffect, useRef } from 'react';

const useClickOutside = (callback) => {
    const ref = useRef(null);

    useEffect(() => {
        const handleClick = (event) => {
            if (ref.current && !ref.current.contains(event.target)) {
                callback();
            }
        };

        document.addEventListener('mousedown', handleClick);
        return () => document.removeEventListener('mousedown', handleClick);
    }, [callback]);

    return ref;
};

// Usage - Dropdown
const Dropdown = () => {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useClickOutside(() => setIsOpen(false));

    return (
        <div ref={dropdownRef}>
            <button onClick={() => setIsOpen(!isOpen)}>Menu</button>
            {isOpen && <ul><li>Item 1</li><li>Item 2</li></ul>}
        </div>
    );
};
```

## 6. useWindowSize

```jsx
import { useState, useEffect } from 'react';

const useWindowSize = () => {
    const [size, setSize] = useState({
        width: window.innerWidth,
        height: window.innerHeight
    });

    useEffect(() => {
        const handleResize = () => {
            setSize({
                width: window.innerWidth,
                height: window.innerHeight
            });
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return size;
};

// Usage
const ResponsiveComponent = () => {
    const { width } = useWindowSize();
    
    return width < 768 ? <MobileView /> : <DesktopView />;
};
```

## 7. usePrevious

```jsx
import { useRef, useEffect } from 'react';

const usePrevious = (value) => {
    const ref = useRef();
    
    useEffect(() => {
        ref.current = value;
    }, [value]);
    
    return ref.current;
};

// Usage
const Counter = () => {
    const [count, setCount] = useState(0);
    const prevCount = usePrevious(count);
    
    return (
        <div>
            <p>Current: {count}, Previous: {prevCount}</p>
            <button onClick={() => setCount(c => c + 1)}>+</button>
        </div>
    );
};
```
