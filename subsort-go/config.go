package subsort

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type Config struct {
	IsReady bool
	Config  map[string] string
}

func buildDict(lines []string) map[string]string {
	data := make(map[string]string, 10)

	for _, line := range(lines) {
		parts := strings.Split(line, "=")
		if len(parts) == 1 {
			key := strings.TrimSpace(parts[0])
			data[key] = "true"
		} else if len(parts) == 2 {
			key := strings.TrimSpace(parts[0])
			val := strings.TrimSpace(parts[1])
			data[key] = val
		} else {
			fmt.Fprintf(os.Stderr, "Dodgy data: %s", line)
		}
	}

	return data
}

func NewConfig(r io.Reader) (*Config, error) {
	lines, err := getNonBlankLinesFromBuffer(r)
	if err != nil {
		return nil, err
	}

	 c := new(Config)
	 c.Config = buildDict(lines)
	 c.IsReady = true

	 return c, nil
}

func getValueOrDefault[T any](c *Config, key string, defaultValue T, converter func(string) (T, error)) T {
	value, present := c.Config[key]
	if  present {
		final, err := converter(value)
		if err == nil {
			return final
		}
	}
	return defaultValue
}

func GetIntOrDefault(c *Config, key string, defaultValue int) int {
	return getValueOrDefault(c, key, defaultValue, func (val string) (int, error) {
		return strconv.Atoi(val)
	})
}

func GetFloatOrDefault(c *Config, key string, defaultValue float32) float32 {
	return getValueOrDefault(c, key, defaultValue, func (val string) (float32, error) {
		v, err := strconv.ParseFloat(val, 8)
		return float32(v), err
	})
}