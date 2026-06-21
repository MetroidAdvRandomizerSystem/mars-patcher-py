## Versioning
Our version number consists of 0.MINOR.PATCH where:
- MINOR gets increased when we add or remove a new feature
- PATCH gets increased when the changes consist of only bug fixes

There is no regular release schedule. New releases are allowed to be dropped at any time.  

## Releasing for Developers
- Make sure that the `VERSION` field in `pull-assembly-patches.py` is the Fusion ASM version that is meant to be used.
- Do a quick check that the planned release contains all wanted ZM *and* Fusion features. 
- Create and push a tag onto the `main` branch. The tag is just the version number — no prefixes or suffixes.
- Wait for CI to create upload that version to pypi.org 
 

## TODO
- actually have a consistent and following changelog. Unsure if the work for that should include having a proper changelog for all older versions, or just start doing it and mark the past stuff as as "todo"
- instructions for getting new ZM decomp/patch. This is blocked by more work on the ZM rando.
