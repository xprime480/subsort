package subsort

import (
	"bufio"
	"io"
	"os"
)

func getNonBlankLinesFromBuffer(r io.Reader) ([]string, error) {
	lines := make([]string, 0, 20)

    scanner := bufio.NewScanner(r)
    for scanner.Scan() {
		s := scanner.Text()
		if s != "" {
			lines = append(lines, s)
		}
    }

    if err := scanner.Err(); err != nil {
		return lines, err
	}

	return lines, nil

}

func getNonBlankLinesFromFile(fname string) ([]string, error) {
	
	fh, err := os.Open(fname)
    if err != nil {
		return nil, err
    }
    defer fh.Close()

	return getNonBlankLinesFromBuffer(fh)
}
