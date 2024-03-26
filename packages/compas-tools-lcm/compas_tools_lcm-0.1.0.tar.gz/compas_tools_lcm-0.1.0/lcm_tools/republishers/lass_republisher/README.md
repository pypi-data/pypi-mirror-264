# LASS Republishers to New Standard

This is a simple Python script which subscribed to the INS and PROSILICA messages in the LCMTypes
old standard and republishes them in the new standard.

Authors: Sebastián Rodríguez, [srodriguez@mbari.org](mailto:srodriguez@mbari.org)

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

# INS
./lcm_ins_republisher

# Camera
./lcm_prosilica_republisher
```
