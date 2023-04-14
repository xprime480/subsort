package subsort

import (
	"strings"
	"testing"
)

func TestEmptyInputConfig(t *testing.T) {
	// arrange
	data := ""
	r := strings.NewReader(data)

	// act
	config, err := NewConfig(r)

	// assert
	assertNormalReturn(t, config, err)
	if len(config.Config) != 0 {
		t.Fatalf("Expected empty config mappings, got %v", config.Config)
	}
}

func TestKeyWithoutValueConfig(t *testing.T) {
	// arrange
	data := "aKey"
	r := strings.NewReader(data)

	// act
	config, err := NewConfig(r)

	// assert
	assertNormalReturn(t, config, err)
	if len(config.Config) != 1 {
		t.Fatalf("Expected one mapping, got %v", config.Config)
	}
	value, found := config.Config["aKey"]
	if ! found {
		t.Fatalf("Expected to find key 'aKey' but did not (dict: %v)", config.Config)
	}
	if value != "true" {
		t.Fatalf("Expected to find value 'true', but got %s", value)
	}
}

func TestDuplicateKeysConfig(t *testing.T) {
	// arrange
	data := "key = 1\nkey = 2"
	r := strings.NewReader(data)

	// act
	config, err := NewConfig(r)

	// assert
	assertNormalReturn(t, config, err)
	if len(config.Config) != 1 {
		t.Fatalf("Expected one mapping, got %v", config.Config)
	}
	value, found := config.Config["key"]
	if ! found {
		t.Fatalf("Expected to find key 'key' but did not (dict: %v)", config.Config)
	}
	if value != "2" {
		t.Fatalf("Expected to find value '2', but got %s", value)
	}
}

func TestGetIntOrDefaultNotPresentConfig(t *testing.T) {
	// arrange
	data := ""
	r := strings.NewReader(data)

	// act
	config, _ := NewConfig(r)
	value := GetIntOrDefault(config, "key", 2)

	// assert
	if value != 2 {
		t.Fatalf("Expected value 2, got %d", value)
	}
}

func TestGetIntOrDefaultWrongTypeConfig(t *testing.T) {
	// arrange
	data := "key = cat"
	r := strings.NewReader(data)

	// act
	config, _ := NewConfig(r)
	value := GetIntOrDefault(config, "key", 2)

	// assert
	if value != 2 {
		t.Fatalf("Expected value 2, got %d", value)
	}
}

func TestGetIntOrDefaultPresentConfig(t *testing.T) {
	// arrange
	data := "key = 1"
	r := strings.NewReader(data)

	// act
	config, _ := NewConfig(r)
	value := GetIntOrDefault(config, "key", 2)

	// assert
	if value != 1 {
		t.Fatalf("Expected value 1, got %d", value)
	}
}

func TestGetFloatOrDefaultNotPresentConfig(t *testing.T) {
	// arrange
	data := ""
	r := strings.NewReader(data)

	// act
	config, _ := NewConfig(r)
	value := GetFloatOrDefault(config, "key", 1.618)

	// assert
	if value != 1.618 {
		t.Fatalf("Expected value 1.618, got %f", value)
	}
}

func TestGetFloatOrDefaultWrongTypeConfig(t *testing.T) {
	// arrange
	data := "key = cat"
	r := strings.NewReader(data)

	// act
	config, _ := NewConfig(r)
	value := GetFloatOrDefault(config, "key", 1.618)

	// assert
	if value != 1.618 {
		t.Fatalf("Expected value 1.618, got %f", value)
	}
}

func TestGetFloatOrDefaultPresentConfig(t *testing.T) {
	// arrange
	data := "key = 3.14"
	r := strings.NewReader(data)

	// act
	config, _ := NewConfig(r)
	value := GetFloatOrDefault(config, "key", 1.618)

	// assert
	if value != 3.14 {
		t.Fatalf("Expected value 3.14, got %f", value)
	}
}

func assertNormalReturn(t *testing.T, config *Config, err error) {
	if err != nil {
		t.Fatalf("Unexpected error returned: %v", err)
	}
	if config == nil {
		t.Fatal("Expected a config object but got none")
	}
	if ! config.IsReady {
		t.Fatal("Got an incompletely initialized config")
	}
}