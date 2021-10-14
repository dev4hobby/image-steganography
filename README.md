# Image Steganography

![image_out](./output.png)  
What you see isn't everything.  
This image contains hidden data.

![example](./result.gif)  

## Dependency

`Python>=3.8.x` with `pip`

```txt
numpy==1.21.2
Pillow==8.3.2
fastapi==0.68.1
pydantic==1.8.2
uvicorn==0.15.0
python-multipart==0.0.5
```

## Install

```bash
pip install -r requirements.txt
```

## Use as a module

### Hide message

converts the input string to binary and replaces the LSB of each pixel

```bash
python hide.py
```

or

```bash
python hide.py -in image.png -out output.png -m message.txt
```

### Seek message

Concatenate each LSB in the image to see the hidden string.

```bash
python seek.py
```

or

```bash
python seek.py -in output.png
```

## Serve as WebServer (with FastAPI)

can serve steganography module on web server if you want.  

```bash
uvicorn main:app --host=0.0.0.0 --port=8000
```

### Connect to browser (with Next.js)

can serve steganography webpage if you want

```bash
cd steganography-web && yarn && yarn dev
```


### API Document

[Automatic docs](https://fastapi.tiangolo.com/features/#automatic-docs)

Check this out

- [docs](https://image-steganography-d3fau1t.herokuapp.com/docs)
- [redoc](https://image-steganography-d3fau1t.herokuapp.com/redoc)

## Appendix

### Check setting file

You can check the image path or other required values.

```json
{
  "encoding": "utf8",
  "bits": 8,
  "token_string": "#secret#",
  "message": "./message.txt",
  "in_image": "./image.png",
  "out_image": "./output.png",
  "modified_image": "./output.png"
}
```
