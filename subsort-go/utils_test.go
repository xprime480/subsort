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

func TestSubsetFromRangeEmptySet(t *testing.T) {
	subset := GetSubsetFromRange(0, 0, 5)
	if len(subset) > 0 {
		t.Fatalf("Expected empty subset, got %v", subset)
	}
}

func TestSubsetFromRangeZeroCount(t *testing.T) {
	subset := GetSubsetFromRange(0, 10, 0)
	if len(subset) > 0 {
		t.Fatalf("Expected empty subset, got %v", subset)
	}
}

func TestSubsetFromRangeAllCount(t *testing.T) {
	subset := GetSubsetFromRange(0, 10, 10)
	if len(subset) != 10 {
		t.Fatalf("Expected subset of size 10, got %v", subset)
	}

	min, max, distinct := getStats(subset)
	if min != 0 || max != 9 {
		t.Fatalf("Found items out of range 0 - 9: %v", subset)
	}
	if distinct != 10 {
		t.Fatalf("Expected 10 items, got %d: %v", distinct, subset)
	}
}

func TestSubsetFromRangeAllExcessCount(t *testing.T) {
	subset := GetSubsetFromRange(0, 10, 15)
	if len(subset) != 10 {
		t.Fatalf("Expected subset of size 10, got %v", subset)
	}

	min, max, distinct := getStats(subset)
	if min != 0 || max != 9 {
		t.Fatalf("Found items out of range 0 - 9: %v", subset)
	}
	if distinct != 10 {
		t.Fatalf("Expected 10 items, got %d: %v", distinct, subset)
	}
}
func TestSubsetFromRangeAllCountOffset(t *testing.T) {
	subset := GetSubsetFromRange(10, 20, 10)
	if len(subset) != 10 {
		t.Fatalf("Expected subset of size 10, got %v", subset)
	}

	min, max, distinct := getStats(subset)
	if min != 10 || max != 19 {
		t.Fatalf("Found items out of range 10 - 19: %v", subset)
	}
	if distinct != 10 {
		t.Fatalf("Expected 10 distinct items, got %d: %v", distinct, subset)
	}
}

func TestSubsetFromRangeAllCountOffsetPartial(t *testing.T) {
	subset := GetSubsetFromRange(10, 20, 5)
	if len(subset) != 5 {
		t.Fatalf("Expected subset of size 5, got %v", subset)
	}

	min, max, distinct := getStats(subset)
	if min < 10 || max > 19 {
		t.Fatalf("Found items out of range 10 - 19: %v", subset)
	}
	if distinct != 5 {
		t.Fatalf("Expected 5 distinct items, got %d: %v", distinct, subset)
	}
}

func getStats(set [] int) (int, int, int) {
	min, max := set[0], set[0]
	distinct := make(map[int]bool, 0)

	for _, v := range set {
		if v <= min { min = v }
		if v >= max { max = v }
		distinct[v] = true
	}

	return min, max, len(distinct)
}
