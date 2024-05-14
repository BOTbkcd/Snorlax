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

// Location where nnn store the selected files
// The file paths are seperated by null byte
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
			updateArtist(filePath)
		}(string(path))
	}

	wg.Wait()
}

func updateArtist(path string) {
	artist, _, isPresent := strings.Cut(filepath.Base(path), " - ")
	if isPresent {
		fmt.Println(artist)

		//No need to escape space or ' character, Command function takes care of that
		exec.Command("kid3-cli", "-c", fmt.Sprintf("set artist '%s'", sanitizeTitle(artist)), path).Output()
	}
}

func sanitizeTitle(title string) string {
	return strings.Replace(title, "'", "\\'", -1)
}
