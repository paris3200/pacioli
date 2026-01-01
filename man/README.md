# Pacioli Man Page

This directory contains the manual page for Pacioli.

## Viewing the Man Page

### From this directory

```sh
man ./pacioli.1
```

### After installation

If you've installed Pacioli via pip or Poetry, you can view the man page by installing it to your system:

```sh
# Copy to user man pages directory
sudo cp pacioli.1 /usr/local/share/man/man1/
sudo mandb  # Update man database

# Now you can view it with:
man pacioli
```

### Alternative: View without installation

```sh
# Using man directly
man /path/to/pacioli/man/pacioli.1

# Convert to text
man ./pacioli.1 | col -b > pacioli.txt

# Convert to PDF
man -t ./pacioli.1 | ps2pdf - pacioli_manpage.pdf
```

## Man Page Format

The man page is written in groff format (troff/nroff markup language), which is the standard format for Unix/Linux manual pages.
