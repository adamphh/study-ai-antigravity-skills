---
name: React Router
description: Hướng dẫn sử dụng React Router cho navigation
---

# React Router

## Cài đặt

```bash
npm install react-router-dom
```

## Setup cơ bản

```jsx
import { BrowserRouter, Routes, Route, Link, NavLink } from 'react-router-dom';

const App = () => {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/">Home</Link>
                <Link to="/about">About</Link>
                <NavLink to="/products" className={({ isActive }) => isActive ? 'active' : ''}>
                    Products
                </NavLink>
            </nav>

            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/products" element={<Products />} />
                <Route path="/products/:id" element={<ProductDetail />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
};
```

## Nested Routes

```jsx
const App = () => (
    <Routes>
        <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="products" element={<Products />}>
                <Route index element={<ProductList />} />
                <Route path=":id" element={<ProductDetail />} />
                <Route path="new" element={<NewProduct />} />
            </Route>
            <Route path="*" element={<NotFound />} />
        </Route>
    </Routes>
);

// Layout with Outlet
import { Outlet } from 'react-router-dom';

const Layout = () => (
    <div>
        <Header />
        <main>
            <Outlet /> {/* Child routes render here */}
        </main>
        <Footer />
    </div>
);
```

## Hooks

```jsx
import { 
    useParams, 
    useNavigate, 
    useLocation, 
    useSearchParams 
} from 'react-router-dom';

const ProductDetail = () => {
    // Get URL params - /products/:id
    const { id } = useParams();

    // Programmatic navigation
    const navigate = useNavigate();
    
    const goBack = () => navigate(-1);
    const goToProducts = () => navigate('/products');
    const goWithState = () => navigate('/checkout', { 
        state: { from: 'product' },
        replace: true // Thay thế history entry
    });

    // Get current location
    const location = useLocation();
    console.log(location.pathname); // '/products/123'
    console.log(location.state);    // State passed from navigate

    // Query params - ?search=phone&page=1
    const [searchParams, setSearchParams] = useSearchParams();
    const search = searchParams.get('search');
    const page = searchParams.get('page');

    const updateSearch = (term) => {
        setSearchParams({ search: term, page: '1' });
    };

    return <div>Product {id}</div>;
};
```

## Protected Routes

```jsx
import { Navigate, useLocation } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    const { isAuthenticated } = useAuth();
    const location = useLocation();

    if (!isAuthenticated) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return children;
};

// Usage
<Route 
    path="/dashboard" 
    element={
        <ProtectedRoute>
            <Dashboard />
        </ProtectedRoute>
    } 
/>

// Redirect after login
const Login = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const from = location.state?.from?.pathname || '/';

    const handleLogin = async () => {
        await login();
        navigate(from, { replace: true });
    };
};
```

## Lazy Loading Routes

```jsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

const App = () => (
    <Routes>
        <Route path="/" element={<Home />} />
        <Route 
            path="/dashboard" 
            element={
                <Suspense fallback={<Loading />}>
                    <Dashboard />
                </Suspense>
            } 
        />
    </Routes>
);
```
