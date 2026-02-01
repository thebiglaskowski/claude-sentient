# Snippet: go-test

## Description

Go test file with table-driven tests, mocks, and HTTP handler testing patterns.

## When to Use

- Writing unit tests in Go
- Testing HTTP handlers
- Table-driven test patterns
- Mock-based testing

## Code

### Basic Unit Test

```go
package service_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestCalculateTotal(t *testing.T) {
	// Arrange
	items := []Item{
		{Price: 1000, Quantity: 2},
		{Price: 500, Quantity: 1},
	}
	taxRate := 0.1

	// Act
	total := CalculateTotal(items, taxRate)

	// Assert
	expected := 2750 // (2000 + 500) * 1.1
	assert.Equal(t, expected, total)
}
```

### Table-Driven Tests

```go
package validator_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestValidateEmail(t *testing.T) {
	tests := []struct {
		name    string
		email   string
		wantErr bool
	}{
		{
			name:    "valid email",
			email:   "user@example.com",
			wantErr: false,
		},
		{
			name:    "valid email with subdomain",
			email:   "user@mail.example.com",
			wantErr: false,
		},
		{
			name:    "empty email",
			email:   "",
			wantErr: true,
		},
		{
			name:    "missing @",
			email:   "userexample.com",
			wantErr: true,
		},
		{
			name:    "missing domain",
			email:   "user@",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := ValidateEmail(tt.email)

			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}
```

### HTTP Handler Test

```go
package handlers_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestResourceHandler_Create(t *testing.T) {
	tests := []struct {
		name           string
		requestBody    interface{}
		mockSetup      func(*MockResourceService)
		expectedStatus int
		expectedBody   map[string]interface{}
	}{
		{
			name: "successful creation",
			requestBody: map[string]string{
				"name":  "Test Resource",
				"email": "test@example.com",
			},
			mockSetup: func(m *MockResourceService) {
				m.On("Create", mock.Anything, mock.Anything).Return(&Resource{
					ID:    uuid.MustParse("123e4567-e89b-12d3-a456-426614174000"),
					Name:  "Test Resource",
					Email: "test@example.com",
				}, nil)
			},
			expectedStatus: http.StatusCreated,
			expectedBody: map[string]interface{}{
				"data": map[string]interface{}{
					"id":    "123e4567-e89b-12d3-a456-426614174000",
					"name":  "Test Resource",
					"email": "test@example.com",
				},
			},
		},
		{
			name: "validation error - missing name",
			requestBody: map[string]string{
				"email": "test@example.com",
			},
			mockSetup:      func(m *MockResourceService) {},
			expectedStatus: http.StatusBadRequest,
		},
		{
			name:           "invalid JSON",
			requestBody:    "invalid json",
			mockSetup:      func(m *MockResourceService) {},
			expectedStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Arrange
			mockService := new(MockResourceService)
			tt.mockSetup(mockService)

			handler := NewResourceHandler(mockService)

			var body []byte
			switch v := tt.requestBody.(type) {
			case string:
				body = []byte(v)
			default:
				body, _ = json.Marshal(v)
			}

			req := httptest.NewRequest(http.MethodPost, "/resources", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			rec := httptest.NewRecorder()

			// Act
			handler.Create(rec, req)

			// Assert
			assert.Equal(t, tt.expectedStatus, rec.Code)

			if tt.expectedBody != nil {
				var response map[string]interface{}
				err := json.Unmarshal(rec.Body.Bytes(), &response)
				require.NoError(t, err)
				// Compare relevant fields
			}

			mockService.AssertExpectations(t)
		})
	}
}
```

### Mock with testify/mock

```go
package mocks

import (
	"context"

	"github.com/google/uuid"
	"github.com/stretchr/testify/mock"
)

type MockResourceService struct {
	mock.Mock
}

func (m *MockResourceService) FindAll(ctx context.Context, page, limit int, sort string) (*PaginatedResult, error) {
	args := m.Called(ctx, page, limit, sort)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*PaginatedResult), args.Error(1)
}

func (m *MockResourceService) FindByID(ctx context.Context, id uuid.UUID) (*Resource, error) {
	args := m.Called(ctx, id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*Resource), args.Error(1)
}

func (m *MockResourceService) Create(ctx context.Context, req CreateResourceRequest) (*Resource, error) {
	args := m.Called(ctx, req)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*Resource), args.Error(1)
}

func (m *MockResourceService) Update(ctx context.Context, id uuid.UUID, req CreateResourceRequest) (*Resource, error) {
	args := m.Called(ctx, id, req)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*Resource), args.Error(1)
}

func (m *MockResourceService) Delete(ctx context.Context, id uuid.UUID) error {
	args := m.Called(ctx, id)
	return args.Error(0)
}
```

### Test with Database (testcontainers)

```go
package integration_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/require"
	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/modules/postgres"
)

func TestResourceRepository_Integration(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping integration test")
	}

	ctx := context.Background()

	// Start PostgreSQL container
	container, err := postgres.RunContainer(ctx,
		testcontainers.WithImage("postgres:15-alpine"),
		postgres.WithDatabase("testdb"),
		postgres.WithUsername("test"),
		postgres.WithPassword("test"),
	)
	require.NoError(t, err)
	defer container.Terminate(ctx)

	// Get connection string
	connStr, err := container.ConnectionString(ctx, "sslmode=disable")
	require.NoError(t, err)

	// Run migrations and tests
	db := setupDatabase(t, connStr)
	repo := NewResourceRepository(db)

	t.Run("Create and FindByID", func(t *testing.T) {
		resource := &Resource{Name: "Test", Email: "test@example.com"}

		created, err := repo.Create(ctx, resource)
		require.NoError(t, err)
		require.NotEmpty(t, created.ID)

		found, err := repo.FindByID(ctx, created.ID)
		require.NoError(t, err)
		assert.Equal(t, created.Name, found.Name)
	})
}
```

## Customization Points

- Test framework — `testing` + `testify` or just standard library
- Mock generation — Consider `mockery` for auto-generation
- Database tests — `testcontainers` or `dockertest`
- Coverage — Run with `go test -coverprofile=coverage.out`

## Related Snippets

- [go-handler](../api/go-handler.md) — HTTP handlers to test
- [jest-test](./jest-test.md) — JavaScript testing patterns
