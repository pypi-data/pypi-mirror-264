# HWDOCER releases

See what is planned in the [roadmap][roadmap_file]

## 0.1.3

Release date: _2024-03-27_

**Features:**

- Copy all images defined in harness with tag `image`.`src` to output path (for html correct render)

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs

## 0.1.2

Release date: _2024-03-27_

**Features:**

- Improve debug verbosity
- Input file search is more iterative now

**Change:**

- Changed input file search to use glob instead of os.walk

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs

## 0.1.1

Release date: _2024-03-26_

**Fix:**

- Project publishing metadata added/corrected

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs

## 0.1.0

Release date: _2024-03-26_

**Features:**

- Initial functional release
- development venv setup
- logging in multiprocessing thread
- drawio automatic drawing via system call
- wireviz automatic drawing
- basic functional test for diagram and harness
- selectable verbosity in console and log (one argument for both)
- buildable & deployable with poetry

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs

---

[roadmap_file]: roadmap.md
