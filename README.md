# Image Steganography

![image_out]('./image_out.png')  
What you see isn't everything.  
This image contains hidden data.

## Dependency

`Python>=3.8.x` with `pip`

```txt
numpy==1.21.2
Pillow==8.3.2
```

### Install

```bash
pip install -r requirements.txt
```

## How to use

### Check setting file

You can check the image path or other required values.

```json
{
  "encoding": "utf8",
  "bits": 8,
  "token_string": "#secret#",
  "payload": "./payload.txt",
  "in_image": "./image.png",
  "out_image": "./image_out.png",
  "modified_image": "./image_out.png"
}
```

### Hide message

converts the input string to binary and replaces the LSB of each pixel

```bash
python hide.py
```

or

```bash
python hide.py -in image.png -out image_out.png -m payload.txt
```

### Seek message

Concatenate each LSB in the image to see the hidden string.

```bash
python seek.py
```

or

```bash
python seek.py -in image_out.png
```
