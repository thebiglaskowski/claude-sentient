# Snippet: go-handler

## Description

Go HTTP handler with proper error handling, validation, and middleware patterns using standard library or chi router.

## When to Use

- Creating new Go API endpoints
- REST resource operations
- Backend HTTP handlers

## Code

### Standard Library Handler

```go
package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"

	"github.com/google/uuid"
)

// Response helpers
type APIResponse struct {
	Data  interface{} `json:"data,omitempty"`
	Error string      `json:"error,omitempty"`
}

type PaginatedResponse struct {
	Data       interface{} `json:"data"`
	Total      int         `json:"total"`
	Page       int         `json:"page"`
	Limit      int         `json:"limit"`
	TotalPages int         `json:"total_pages"`
}

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(APIResponse{Data: data})
}

func respondError(w http.ResponseWriter, status int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(APIResponse{Error: message})
}

// Resource represents your domain entity
type Resource struct {
	ID          uuid.UUID `json:"id"`
	Name        string    `json:"name"`
	Email       string    `json:"email"`
	Description string    `json:"description,omitempty"`
	CreatedAt   string    `json:"created_at"`
}

// CreateResourceRequest for validation
type CreateResourceRequest struct {
	Name        string `json:"name"`
	Email       string `json:"email"`
	Description string `json:"description,omitempty"`
}

func (r *CreateResourceRequest) Validate() error {
	if r.Name == "" || len(r.Name) > 100 {
		return errors.New("name must be 1-100 characters")
	}
	if r.Email == "" {
		return errors.New("email is required")
	}
	return nil
}

// Handler struct with dependencies
type ResourceHandler struct {
	service ResourceService
}

func NewResourceHandler(service ResourceService) *ResourceHandler {
	return &ResourceHandler{service: service}
}

// GET /resources
func (h *ResourceHandler) List(w http.ResponseWriter, r *http.Request) {
	// Parse query params
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page < 1 {
		page = 1
	}

	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	if limit < 1 || limit > 100 {
		limit = 20
	}

	sort := r.URL.Query().Get("sort")
	if sort != "asc" && sort != "desc" {
		sort = "desc"
	}

	// Call service
	result, err := h.service.FindAll(r.Context(), page, limit, sort)
	if err != nil {
		respondError(w, http.StatusInternalServerError, "Failed to fetch resources")
		return
	}

	respondJSON(w, http.StatusOK, PaginatedResponse{
		Data:       result.Data,
		Total:      result.Total,
		Page:       page,
		Limit:      limit,
		TotalPages: (result.Total + limit - 1) / limit,
	})
}

// GET /resources/{id}
func (h *ResourceHandler) Get(w http.ResponseWriter, r *http.Request) {
	// Extract ID from path (adjust based on router)
	idStr := r.PathValue("id") // Go 1.22+ or use chi.URLParam

	id, err := uuid.Parse(idStr)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid resource ID")
		return
	}

	resource, err := h.service.FindByID(r.Context(), id)
	if err != nil {
		if errors.Is(err, ErrNotFound) {
			respondError(w, http.StatusNotFound, "Resource not found")
			return
		}
		respondError(w, http.StatusInternalServerError, "Failed to fetch resource")
		return
	}

	respondJSON(w, http.StatusOK, resource)
}

// POST /resources
func (h *ResourceHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateResourceRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	if err := req.Validate(); err != nil {
		respondError(w, http.StatusBadRequest, err.Error())
		return
	}

	resource, err := h.service.Create(r.Context(), req)
	if err != nil {
		respondError(w, http.StatusInternalServerError, "Failed to create resource")
		return
	}

	respondJSON(w, http.StatusCreated, resource)
}

// PUT /resources/{id}
func (h *ResourceHandler) Update(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")

	id, err := uuid.Parse(idStr)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid resource ID")
		return
	}

	var req CreateResourceRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	if err := req.Validate(); err != nil {
		respondError(w, http.StatusBadRequest, err.Error())
		return
	}

	resource, err := h.service.Update(r.Context(), id, req)
	if err != nil {
		if errors.Is(err, ErrNotFound) {
			respondError(w, http.StatusNotFound, "Resource not found")
			return
		}
		respondError(w, http.StatusInternalServerError, "Failed to update resource")
		return
	}

	respondJSON(w, http.StatusOK, resource)
}

// DELETE /resources/{id}
func (h *ResourceHandler) Delete(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")

	id, err := uuid.Parse(idStr)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid resource ID")
		return
	}

	err = h.service.Delete(r.Context(), id)
	if err != nil {
		if errors.Is(err, ErrNotFound) {
			respondError(w, http.StatusNotFound, "Resource not found")
			return
		}
		respondError(w, http.StatusInternalServerError, "Failed to delete resource")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}
```

### Router Setup (Go 1.22+)

```go
package main

import (
	"net/http"
)

func main() {
	mux := http.NewServeMux()

	handler := NewResourceHandler(resourceService)

	// Routes
	mux.HandleFunc("GET /resources", handler.List)
	mux.HandleFunc("GET /resources/{id}", handler.Get)
	mux.HandleFunc("POST /resources", handler.Create)
	mux.HandleFunc("PUT /resources/{id}", handler.Update)
	mux.HandleFunc("DELETE /resources/{id}", handler.Delete)

	// Wrap with middleware
	server := &http.Server{
		Addr:    ":8080",
		Handler: loggingMiddleware(recoveryMiddleware(mux)),
	}

	server.ListenAndServe()
}
```

### Middleware Examples

```go
package middleware

import (
	"log"
	"net/http"
	"time"
)

func LoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		// Wrap response writer to capture status
		wrapped := &responseWriter{ResponseWriter: w, status: http.StatusOK}

		next.ServeHTTP(wrapped, r)

		log.Printf(
			"%s %s %d %s",
			r.Method,
			r.URL.Path,
			wrapped.status,
			time.Since(start),
		)
	})
}

func RecoveryMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Printf("panic recovered: %v", err)
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

type responseWriter struct {
	http.ResponseWriter
	status int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.status = code
	rw.ResponseWriter.WriteHeader(code)
}
```

## Customization Points

- `ResourceService` — Replace with your service interface
- `Resource` — Replace with your domain entity
- Validation — Add more validation rules as needed
- Router — Adapt for chi, gin, or other routers

## Related Snippets

- [go-test](../testing/go-test.md) — Test this handler
- [error-class](../utility/error-class.md) — Error patterns
