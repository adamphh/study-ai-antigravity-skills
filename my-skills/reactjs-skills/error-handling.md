---
name: Error Handling
description: Hướng dẫn xử lý lỗi trong React
---

# Error Handling trong React

## Class Component - Error Boundary

```jsx
import React, { Component } from 'react';

class ErrorBoundary extends Component {
    state = { hasError: false, error: null, errorInfo: null };

    static getDerivedStateFromError(error) {
        // Update state để render fallback UI
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // Log error to service
        console.error('Error caught:', error);
        console.error('Error info:', errorInfo);
        
        this.setState({ error, errorInfo });
        
        // Send to error tracking service
        // errorService.log({ error, errorInfo });
    }

    handleReset = () => {
        this.setState({ hasError: false, error: null, errorInfo: null });
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-boundary">
                    <h2>Something went wrong</h2>
                    <details>
                        <summary>Error details</summary>
                        <pre>{this.state.error?.toString()}</pre>
                        <pre>{this.state.errorInfo?.componentStack}</pre>
                    </details>
                    <button onClick={this.handleReset}>Try Again</button>
                </div>
            );
        }

        return this.props.children;
    }
}

// Usage
const App = () => (
    <ErrorBoundary>
        <Header />
        <ErrorBoundary>
            <MainContent />
        </ErrorBoundary>
        <Footer />
    </ErrorBoundary>
);
```

## Error Boundary với Fallback Component

```jsx
class ErrorBoundary extends Component {
    state = { hasError: false };

    static getDerivedStateFromError() {
        return { hasError: true };
    }

    componentDidCatch(error, info) {
        this.props.onError?.(error, info);
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback || <DefaultErrorUI />;
        }
        return this.props.children;
    }
}

// Usage with custom fallback
<ErrorBoundary fallback={<MyCustomError />}>
    <RiskyComponent />
</ErrorBoundary>

<ErrorBoundary 
    fallback={<p>Widget failed to load</p>}
    onError={(error) => logError(error)}
>
    <Widget />
</ErrorBoundary>
```

## Function Component - Try/Catch

```jsx
import { useState } from 'react';

const SafeComponent = () => {
    const [error, setError] = useState(null);

    const handleClick = async () => {
        try {
            await riskyOperation();
        } catch (err) {
            setError(err.message);
        }
    };

    const handleRender = () => {
        try {
            return <RiskyRender />;
        } catch (err) {
            return <p>Render failed: {err.message}</p>;
        }
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <button onClick={handleClick}>Do Something</button>
            {handleRender()}
        </div>
    );
};
```

## Async Error Handling Hook

```jsx
const useAsyncError = () => {
    const [, setError] = useState();

    return (error) => {
        setError(() => {
            throw error; // Will be caught by ErrorBoundary
        });
    };
};

// Usage
const AsyncComponent = () => {
    const throwError = useAsyncError();

    useEffect(() => {
        fetchData()
            .catch(throwError); // Propagate to ErrorBoundary
    }, []);

    return <div>Content</div>;
};
```

## API Error Handling

```jsx
const useApi = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleError = (err) => {
        if (err.response) {
            // Server responded with error status
            switch (err.response.status) {
                case 400:
                    setError('Invalid request');
                    break;
                case 401:
                    setError('Please login');
                    // redirect to login
                    break;
                case 403:
                    setError('Access denied');
                    break;
                case 404:
                    setError('Not found');
                    break;
                case 500:
                    setError('Server error');
                    break;
                default:
                    setError('Something went wrong');
            }
        } else if (err.request) {
            // No response received
            setError('Network error');
        } else {
            setError(err.message);
        }
    };

    const request = async (fn) => {
        setLoading(true);
        setError(null);
        try {
            const result = await fn();
            return result;
        } catch (err) {
            handleError(err);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return { request, loading, error, clearError: () => setError(null) };
};
```

## Form Validation Errors

```jsx
const useFormErrors = () => {
    const [errors, setErrors] = useState({});

    const setFieldError = (field, message) => {
        setErrors(prev => ({ ...prev, [field]: message }));
    };

    const clearFieldError = (field) => {
        setErrors(prev => {
            const newErrors = { ...prev };
            delete newErrors[field];
            return newErrors;
        });
    };

    const clearAllErrors = () => setErrors({});

    const hasErrors = Object.keys(errors).length > 0;

    return { errors, setFieldError, clearFieldError, clearAllErrors, hasErrors };
};

// Usage
const Form = () => {
    const { errors, setFieldError, clearFieldError, hasErrors } = useFormErrors();

    const validate = (values) => {
        if (!values.email) setFieldError('email', 'Required');
        if (!values.password) setFieldError('password', 'Required');
    };

    return (
        <form>
            <input name="email" onFocus={() => clearFieldError('email')} />
            {errors.email && <span>{errors.email}</span>}
            
            <button disabled={hasErrors}>Submit</button>
        </form>
    );
};
```
