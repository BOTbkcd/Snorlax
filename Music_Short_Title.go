package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
)

const NNN_SELECTION = "/home/bot_bkcd/.config/nnn/.selection"

func main() {
	f, err := os.ReadFile(NNN_SELECTION)
	if err != nil {
		log.Fatal(err)
	}

	paths := bytes.Split(f, []byte("\000"))

	wg := sync.WaitGroup{}
	wg.Add(len(paths))

	for _, path := range paths {
		go func(filePath string) {
			defer wg.Done()
			updateTitle(filePath)
		}(string(path))
	}

	wg.Wait()
}

func updateTitle(path string) {
	_, title, isPresent := strings.Cut(filepath.Base(path), " - ")
	if isPresent {
		formattedTitle := sanitizeTitle(title)
		fmt.Println(formattedTitle)

		//No need to escape space or ' character, Command function takes care of that
		exec.Command("kid3-cli", "-c", fmt.Sprintf("set title '%s'", formattedTitle), path).Output()
	}
}

func sanitizeTitle(title string) string {
	newTitle := strings.TrimSuffix(title, filepath.Ext(title))
	return strings.Replace(newTitle, "'", "\\'", -1)
}
