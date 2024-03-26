# splice

This is a simple Python script to splice images into an LCM log from a directory, using the file
name as a timestamp.

Author: Kevin Barnard, [kbarnard@mbari.org](mailto:kbarnard@mbari.org)

## Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
cd lcm_tools/build/bin
./lcmsplice <input> <channel name> <image directory> <output>
```

Pass in the `-o` flag to overwrite the output log, if it already exists.

### Example

```bash
cd lcm-tools/build/bin
./logtools_img2log lcmlog.00 PROSILICA_L PROSILICA_L/ lcmlog-with-left-images.00
```

For the case of stereo, simply run the script again for the second camera, e.g.:

```bash
cd lcm-tools/build/bin
./logtools_img2log lcmlog-with-left-images.00 PROSILICA_R PROSILICA_R/ lcmlog-with-images.00
```
