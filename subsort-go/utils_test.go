package subsort

import (
	"strings"
	"testing"
)

func TestEmptyInputFile(t *testing.T) {
	// arrange
	data := ""
	r := strings.NewReader(data)

	// act
	lines, err := getNonBlankLinesFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 0 {
		t.Fatalf("Expected empty return value, got %v", lines)
	}
}

func TestUnterminatedFile(t *testing.T) {
	// arrange
	data := "foo"
	r := strings.NewReader(data)

	// act
	lines, err := getNonBlankLinesFromBuffer(r)

	// assert
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if len(lines) != 1 {
		t.Fatalf("Expected single line, got %v", lines)
	}
	if lines[0] != "foo" {
		t.Fatalf("Expected 'foo' for first line, got %s", lines[0])
	}
}

func TestWithBlanklineFile(t *testing.T) {
	// arrange
	data := "foo\n\nbar"
	r := strings.NewReader(data)

	// act
	lines, err := getNonBlankLinesFromBuffer(r)

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
