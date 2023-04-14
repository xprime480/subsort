package subsort

import (
	"bufio"
	"io"
	"os"
	"math/rand"
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

func GetSubsetFromRange(min, max, count int) []int {
	if count == 0 {
		return make([]int, 0)
	}

	data := iota(min, max)

	for i := range data {
		j := rand.Intn(i + 1)
		data[i], data[j] = data[j], data[i]
	}

	if count > max - min {
		count = max - min
	}
	data = data[0:count]

	return data
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

func iota(min, max int) []int {
	if max <= min {
		return make([]int, 0, 0)
	}

	data := make([]int, max-min, max-min)
	for i := 0; min < max ; min++ {
		data[i] = min
		i++
	}
	return data
}

func fileOp(fname string, op func (r io.Reader) ([]string, error)) ([]string, error) {
	fh, err := os.Open(fname)
    if err != nil {
		return nil, err
    }
    defer fh.Close()

	return op(fh)
}
