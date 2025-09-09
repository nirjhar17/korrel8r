// Copyright: This file is part of korrel8r, released under https://github.com/korrel8r/korrel8r/blob/main/LICENSE

package traverse

import (
	"sync"

	"github.com/go-logr/logr"
	"github.com/korrel8r/korrel8r/pkg/korrel8r"
	"github.com/korrel8r/korrel8r/pkg/unique"
)

// Errors is a goroutine-safe collection of unique errors.
type Errors struct {
	m    sync.Mutex
	errs unique.Errors
	ok   int
	log  logr.Logger
}

func NewErrors(log logr.Logger) *Errors {
	return &Errors{log: log}
}

// Log the first instance of err, don't log duplicates
func (e *Errors) Log(err error, msg string, kv ...any) bool {
	e.m.Lock()
	defer e.m.Unlock()
	if err == nil {
		e.ok++ // Count the number of sucesses..
	}
	if e.errs.Add(err) {
		e.log.Error(err, msg, kv...)
		return true
	}
	return false
}

// Err returns the resulting error which may be a PartialError.
// Must not be called concurrently.
func (e *Errors) Err() error {
	switch {
	case e.errs.Err() == nil:
		return nil
	case e.ok > 0:
		return &korrel8r.PartialError{Err: e.errs.Err()}
	default:
		return e.errs.Err()
	}
}
