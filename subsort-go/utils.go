package subsort

import (
	"bufio"
	"io"
	"math"
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

func MakeGeometricSeries(sumOfTerms, termCount, firstTermMinimum int, ratios ...float64) []int {
	data := make([]int, 0)

	if sumOfTerms <= 0 {
		return make([]int, termCount)
	}
	if termCount <= 0 {
		return data
	}
	if termCount == 1 {
		return append(data, sumOfTerms)
	}
	
	ratio := 2.0
	if len(ratios) > 0 {
		ratio = ratios[0]
	}

	if ratio < 0.0 {
		data = append(data, sumOfTerms)
		for i := 1 ; i < termCount ; i++ {
			data = append(data, 0)
		}
		return data
	}

	data = makeGeometricSeriesFast(sumOfTerms, termCount, ratio)
	if data[0] < firstTermMinimum {
		data = makeGeometricSeriesIncrementally(sumOfTerms, termCount, firstTermMinimum, ratio)
	}

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

func makeGeometricSeriesFast(sumOfTerms, termCount int, ratio float64) []int {
	sumOfDivisors := math.Pow(float64(ratio), float64(termCount))

	weights := make([]float64, termCount, termCount)
	for i := 0 ; i < termCount ; i++ {
		weights[i] = sumOfDivisors / math.Pow(float64(ratio), float64(i))
	}

	tweakRange := [...]float64 {-1.0, 1.0}

	for {
		tweak := (tweakRange[0] + tweakRange[1]) / 2.0
		guess := make([]int, termCount)
		delta := -1 * sumOfTerms
		for i := 0 ; i < termCount ; i++ {
			g := int(math.Round(float64(sumOfTerms)/weights[i] + tweak))
			guess[i] = g
			delta += g
		}

		if delta == 0 {
			return guess
		}
		if delta > 0 {
			tweakRange[1] = tweak
		} else {
			tweakRange[0] = tweak
		}
	}
}

func makeGeometricSeriesIncrementally(sumOfTerms, termCount, firstTermMinimum int, ratio float64) []int {
	data := make([]int, termCount)

	for i := 0 ; sumOfTerms > 0 ; i++ {
		temp := firstTermMinimum
		if sumOfTerms < temp {
			temp = sumOfTerms
		}

		data[i] = temp
		sumOfTerms -= temp
		firstTermMinimum *= 2
	}
	
	return data
}