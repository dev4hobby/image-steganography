import click
from binjector.utils import read_settings, set_token
from binjector.steganography import Steganography

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', required=True, type=click.Path(exists=True), help='Input file')
@click.option('-o', type=click.Path(exists=False), help='Output file')
@click.option('-m', required= True, type=click.Path(exists=True), help='Message file')
def hide(i, o, m):
    s = Steganography()
    # hide your message into image
    if not o:
        from datetime import datetime
        o = f'output_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    try:
        with open(m, "r") as message_file:
            message = message_file.read()
        s.hide_message(i, o, message)
        print('Done')
    except Exception as e:
        print(e)
        raise e

@cli.command()
@click.option('-i', required=True, type=click.Path(exists=True), help='Input file')
def seek(i):
    s = Steganography()
    # seek your message into image
    try:
        print(s.seek_message(i))
    except Exception as e:
        print(e)
        raise e

@cli.command()
def settings():
    try:
        config = read_settings()
        print(config)
    except Exception as e:
        print(e)
        raise e

@cli.command()
def refresh_token():
    try:
        set_token()
    except Exception as e:
        print(e)
        raise e

if __name__ == '__main__': 
    cli()
