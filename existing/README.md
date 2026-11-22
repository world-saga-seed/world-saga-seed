Put your existing manuscripts and notes here. Claude reads this folder and never changes it.

**A text that is not your own** (a public-domain edition, a translation, a reference work) goes in a folder of its own, `existing/<source>/`, with a `SOURCE.md` beside it: what it is (author, title, edition, year), where it was fetched and when, its license or public-domain status, and a `SHA256SUMS` file with a checksum for each of its files. Write it once, at intake; never edit the source files after.

If a source is large, or its terms do not let you republish it, keep its files out of git (list them in `.gitignore`) and commit only `SOURCE.md` and `SHA256SUMS`, so anyone can fetch the same files and check them.

Plain text made from a source (paragraph-numbered chapters, say) is not the source: it goes in `sources/<source>/`, made by a script in `scripts/`, so it can be made again from `existing/`.
