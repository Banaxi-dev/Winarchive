
# WinArchive

WinArchive is a powerfull Python program that supports various archive formats such as ZIP, 7z, RAR, CAB, and a custom `.archive` format. It enables the creation and extraction of archives, including the ability to password-protect archives (for 7z and the custom format).

## Features

- **Create Archives**: Supports formats such as ZIP, 7z, RAR, CAB, and a custom `.archive` format.
- **Extract Archives**: Extract files from supported archive formats.
- **Password Protection**: Optional password protection for 7z, RAR, and custom `.archive` archives.
- **Custom Format**: Create and extract a simple, custom archive format (`.archive`).

## Installation

1. **Install Python**: Ensure that Python 3.x is installed on your system. You can download Python from [python.org](https://www.python.org/).
2. **Install Dependencies**: Install the required Python modules using pip:

   ```bash
   pip install py7zr
   ```

## Usage

### Creating an Archive

You can create an archive by running the script with the following parameters:

```bash
python winarchive.py [format] [input] [output] [optional_password]
```

- `format`: The desired archive format (`zip`, `7z`, `rar`, `cab`, `archive`).
- `input`: The path to the directory or file to be archived.
- `output`: The path to the output archive file.
- `optional_password`: (Optional) A password to protect the archive (only for 7z and `.archive`).

**Example**:

```bash
python winarchive.py 7z my_folder my_archive.7z mypassword123
```

### Extracting an Archive

To extract an archive, run the script with the following parameters:

```bash
python winarchive.py extract [archive_file] [output_dir] [optional_password]
```

- `archive_file`: The path to the archive file to be extracted.
- `output_dir`: The directory where the files should be extracted.
- `optional_password`: (Optional) A password if the archive is protected.

**Example**:

```bash
python winarchive.py extract my_archive.7z extracted_folder mypassword123
```

## Known Security Issues

**Warning**: The custom `.archive` format stores the file name, file contents, and password in plain text. This poses a significant security risk, as anyone with access to the `.archive` file can easily read this information. The developers are working on fixing this vulnerability in the next version.

## License

This project is licensed under the MIT License. For more details, see the `LICENSE` file.
