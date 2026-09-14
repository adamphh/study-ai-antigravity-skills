---
name: React Testing
description: Hướng dẫn viết tests cho React components
---

# Testing React Components

## Setup

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

## Basic Component Test

```jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
    test('renders correctly', () => {
        render(<MyComponent title="Hello" />);
        
        expect(screen.getByText('Hello')).toBeInTheDocument();
        expect(screen.getByRole('button')).toBeInTheDocument();
    });

    test('handles click', async () => {
        const handleClick = jest.fn();
        render(<MyComponent onClick={handleClick} />);
        
        await userEvent.click(screen.getByRole('button'));
        
        expect(handleClick).toHaveBeenCalledTimes(1);
    });
});
```

## Common Queries

```jsx
// By text
screen.getByText('Hello');
screen.getByText(/hello/i);  // regex, case insensitive

// By role
screen.getByRole('button');
screen.getByRole('button', { name: 'Submit' });
screen.getByRole('textbox');
screen.getByRole('heading', { level: 1 });

// By label
screen.getByLabelText('Email');

// By placeholder
screen.getByPlaceholderText('Enter email');

// By test id
screen.getByTestId('custom-element');

// Query variants
screen.queryByText('May not exist');  // Returns null if not found
screen.findByText('Async content');   // Returns Promise
screen.getAllByRole('listitem');      // Returns array
```

## Testing User Interactions

```jsx
import userEvent from '@testing-library/user-event';

test('form submission', async () => {
    const user = userEvent.setup();
    const handleSubmit = jest.fn();
    
    render(<LoginForm onSubmit={handleSubmit} />);
    
    // Type in inputs
    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'password123');
    
    // Check checkbox
    await user.click(screen.getByRole('checkbox'));
    
    // Select dropdown
    await user.selectOptions(screen.getByRole('combobox'), 'admin');
    
    // Submit form
    await user.click(screen.getByRole('button', { name: 'Submit' }));
    
    expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
    });
});
```

## Testing Async Behavior

```jsx
import { render, screen, waitFor } from '@testing-library/react';

test('loads and displays data', async () => {
    render(<UserList />);
    
    // Wait for loading to disappear
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    
    // Wait for data
    await waitFor(() => {
        expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    // Or use findBy (combines getBy + waitFor)
    const user = await screen.findByText('John Doe');
    expect(user).toBeInTheDocument();
});
```

## Mocking API Calls

```jsx
// __mocks__/api.js
export const fetchUsers = jest.fn();

// UserList.test.jsx
import { fetchUsers } from './api';

jest.mock('./api');

test('displays users from API', async () => {
    fetchUsers.mockResolvedValue([
        { id: 1, name: 'John' },
        { id: 2, name: 'Jane' }
    ]);
    
    render(<UserList />);
    
    expect(await screen.findByText('John')).toBeInTheDocument();
    expect(screen.getByText('Jane')).toBeInTheDocument();
    expect(fetchUsers).toHaveBeenCalledTimes(1);
});

test('displays error on failure', async () => {
    fetchUsers.mockRejectedValue(new Error('Failed'));
    
    render(<UserList />);
    
    expect(await screen.findByText(/error/i)).toBeInTheDocument();
});
```

## Testing with Context

```jsx
const renderWithProviders = (ui, { theme = 'light', ...options } = {}) => {
    const Wrapper = ({ children }) => (
        <ThemeProvider value={theme}>
            <AuthProvider>
                {children}
            </AuthProvider>
        </ThemeProvider>
    );
    
    return render(ui, { wrapper: Wrapper, ...options });
};

test('uses theme from context', () => {
    renderWithProviders(<ThemedButton />, { theme: 'dark' });
    expect(screen.getByRole('button')).toHaveClass('dark');
});
```

## Testing Router

```jsx
import { MemoryRouter } from 'react-router-dom';

const renderWithRouter = (ui, { route = '/' } = {}) => {
    return render(
        <MemoryRouter initialEntries={[route]}>
            {ui}
        </MemoryRouter>
    );
};

test('navigates to about page', async () => {
    renderWithRouter(<App />);
    
    await userEvent.click(screen.getByText('About'));
    
    expect(screen.getByText('About Page')).toBeInTheDocument();
});
```

## Testing Hooks

```jsx
import { renderHook, act } from '@testing-library/react';
import useCounter from './useCounter';

test('useCounter increments', () => {
    const { result } = renderHook(() => useCounter(0));
    
    expect(result.current.count).toBe(0);
    
    act(() => {
        result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
});
```

## Snapshot Testing

```jsx
test('matches snapshot', () => {
    const { container } = render(<Card title="Test" />);
    expect(container).toMatchSnapshot();
});
```
