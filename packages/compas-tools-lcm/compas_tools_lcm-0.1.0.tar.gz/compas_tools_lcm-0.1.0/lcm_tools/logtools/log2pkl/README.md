# LCM to log converter.

This is a simple Python script to convert an LCM log into a Pickle file, given a directory path. The
code will search recursively for lcmlogs if the directory has subdirectories.

Authors: Sebastián Rodríguez, [srodriguez@mbari.org](mailto:srodriguez@mbari.org), Giancarlo Troni,
[gtroni@mbari.org](mailto:gtroni@mbari.org)

## Install dependencies

```bash
pip install -r requirements.txt
```

### LCMTypes

The LCMTypes library is installed locally using the [LCMTypes Bitbucket
repository](https://bitbucket.org/compas-sw/compas_lcmtypes/src/main/) as a submodule. If you want
to use a specific version of the LCMTypes, you can checkout to a specific commit into the `lcmtypes`
directory.

## Usage

```bash
cd lcm-tools/build/bin
./logtools_log2pkl -p <directory path>
```

### Example

```bash
cd lcm-tools/build/bin
./logtools_log2pkl -p /data/
```
