package subsort

import (
	"bufio"
	"io"
	"os"
	"strings"
)

func GetLinesFromBuffer(r io.Reader) ([]string, error) {
	lines := make([]string, 0, 20)

    scanner := bufio.NewScanner(r)
    for scanner.Scan() {
		s := scanner.Text()
		lines = append(lines, s)
    }

    if err := scanner.Err(); err != nil {
		return lines, err
	}

	return lines, nil
}

func filter(lines []string, f func(string) bool) []string {
	filtered := make([]string, 0, len(lines))
	for _, line := range lines {
		if f(line) {
			filtered = append(filtered, line)
		}
	}
	return filtered
}

func transform(lines []string, f func(string) string) []string {
	transformed := make([]string, len(lines), len(lines))
	for index, line := range lines {
		transformed[index] = f(line)
	}
	return transformed
}

func GetNonBlankLinesFromBuffer(r io.Reader) ([]string, error) {
	lines, err := GetLinesFromBuffer(r)
	if err != nil {
		return lines, err
	}

	filtered := filter(lines, func(s string) bool { return s != ""})
	return filtered, nil
}

func GetNonBlankLinesFromFile(fname string) ([]string, error) {
	return fileOp(fname, GetNonBlankLinesFromBuffer)
}

func GetDataFromBuffer(r io.Reader) ([]string, error) {
	lines, err := GetLinesFromBuffer(r)
	if err != nil {
		return lines, err
	}

	transformed := transform(lines, func(s string) string { return strings.TrimSpace(s) })
	return transformed, nil
}

func GetDataFromFile(fname string) ([]string, error) {
	return fileOp(fname, GetDataFromBuffer)
}

func fileOp(fname string, op func (r io.Reader) ([]string, error)) ([]string, error) {
	fh, err := os.Open(fname)
    if err != nil {
		return nil, err
    }
    defer fh.Close()

	return op(fh)
}
