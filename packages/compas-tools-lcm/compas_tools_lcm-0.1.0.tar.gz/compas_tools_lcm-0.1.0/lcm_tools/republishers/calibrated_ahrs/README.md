# Calibrated AHRS.

This is a simple Python script to subscribe to an AHRS channel, and republish the calibrated AHRS in
a different channel.

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
./lcm_tools_ahrs -i <input channel> -o <output channel> -p <config file>
```

### Example

```bash
cd lcm-tools/build/bin
./lcm_tools_ahrs -i VN100_AHRS -o VN100_AHRS_C -p ../config/config_calibrated_ahrs.json
```
