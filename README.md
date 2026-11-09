# Link Guard website

Source of [link-guard.nullringresearch.de](https://link-guard.nullringresearch.de/): the
landing page for Link Guard. The documentation under `/thunderbird/` is built from the
signed releases of
[thunderbird-link-guard](https://github.com/marco-schm/thunderbird-link-guard).

```sh
python3 -I build.py . out    # builds the static pages into out/
```

The pages contain no JavaScript, no cookies and no third-party requests; fonts, styles
and the logo are inlined so the site works under a Content-Security-Policy of
`default-src 'none'`.

## Releases

The server publishes only tags signed with the Link Guard release key and never moves
backwards. To release, raise `VERSION`, merge to `main`, then run
`scripts/sign-release-tag.sh` with the security key attached and push the tag.

## License

MIT for the code and texts. IBM Plex Sans and IBM Plex Mono are © IBM Corp. under the
SIL Open Font License 1.1 (`src/fonts/OFL.txt`).
