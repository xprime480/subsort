package subsort

import (
	"strings"
	"testing"
)

func TestGetNonblankEmptyInput(t *testing.T) {
	// arrange
	data := ""
	r := strings.NewReader(data)

	// act
	lines, err := GetNonBlankLinesFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 0 {
		t.Fatalf("Expected empty return value, got %v", lines)
	}
}

func TestGetNonblankUnterminatedWithWhitespace(t *testing.T) {
	// arrange
	data := "foo   "
	r := strings.NewReader(data)

	// act
	lines, err := GetNonBlankLinesFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 1 {
		t.Fatalf("Expected single line, got %v", lines)
	}
	if lines[0] != "foo   " {
		t.Fatalf("Expected 'foo   ' for first line, got %s", lines[0])
	}
}

func TestGetNonblankWithBlankline(t *testing.T) {
	// arrange
	data := "foo\n\nbar"
	r := strings.NewReader(data)

	// act
	lines, err := GetNonBlankLinesFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 2 {
		t.Fatalf("Expected two lines, got %v", lines)
	}
	if lines[0] != "foo" {
		t.Fatalf("Expected 'foo' for first line, got %s", lines[0])
	}
	if lines[1] != "bar" {
		t.Fatalf("Expected 'bar' for second line, got %s", lines[1])
	}
}

func TestGetDataEmptyInput(t *testing.T) {
	// arrange
	data := ""
	r := strings.NewReader(data)

	// act
	lines, err := GetDataFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 0 {
		t.Fatalf("Expected empty return value, got %v", lines)
	}
}

func TestGetDataUnterminatedWithWhitespace(t *testing.T) {
	// arrange
	data := "foo   "
	r := strings.NewReader(data)

	// act
	lines, err := GetDataFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 1 {
		t.Fatalf("Expected single line, got %v", lines)
	}
	if lines[0] != "foo" {
		t.Fatalf("Expected 'foo' for first line, got '%s'", lines[0])
	}
}

func TestGetDataWithBlankline(t *testing.T) {
	// arrange
	data := "foo\n\nbar"
	r := strings.NewReader(data)

	// act
	lines, err := GetDataFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 3 {
		t.Fatalf("Expected two lines, got %v", lines)
	}
	if lines[0] != "foo" {
		t.Fatalf("Expected 'foo' for first line, got '%s'", lines[0])
	}
	if lines[1] != "" {
		t.Fatalf("Expected '' for second line, got '%s'", lines[1])
	}
	if lines[2] != "bar" {
		t.Fatalf("Expected 'bar' for third line, got '%s'", lines[2])
	}
}

