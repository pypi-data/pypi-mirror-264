import logging
import os
from datetime import datetime


def file_handler(fullpath, **kwargs) -> datetime | None:
    logging.debug(f"Handling {fullpath} as a simple file")
    try:
        mtime = os.path.getmtime(fullpath)
        dtime = datetime.fromtimestamp(mtime)
    except Exception as e:
        logging.error(f"{e}: Could not fetch timestamp for {fullpath} (), skipping")
        return None
    return dtime


def pdf_handler(fullpath, **kwargs):
    logging.debug(f"Handling {fullpath} as a PDF file")

    import pdfrw

    r = pdfrw.PdfReader(fullpath)
    try:
        # Why do PDFs have such a weird timestamp format?
        # example from a random PDF: (D:20131222010843-06'00')
        # grabbing only what we need up to seconds, no TZ
        dtime = r.Info.CreationDate[3:17]
        dtime = datetime.strptime(dtime, "%Y%m%d%H%M%S")
    except Exception as e:
        logging.error(
            f"{e}: Could not read PDF metadata from {fullpath}, "
            "falling back to file_handler"
        )
        return file_handler(fullpath, **kwargs)
    return dtime


def exif_handler(fullpath, **kwargs):
    logging.debug(f"Handling {fullpath} as an EXIF image")

    from PIL import Image

    dtime = None
    try:
        image = Image.open(fullpath)
        exif = image._getexif()
        dtime = exif.get(0x9003)
    except Exception as e:
        logging.debug(e)
        logging.warn(
            f"Could not read EXIF metadata from {fullpath}, "
            "falling back to file_handler"
        )
        return file_handler(fullpath, **kwargs)
    dtime = datetime.strptime(dtime, "%Y:%m:%d %H:%M:%S")
    return dtime


def video_handler(fullpath, **kwargs):
    logging.debug(f"Handling {fullpath} as a video file")

    from enzyme import MKV

    try:
        with open(fullpath, "rb") as fh:
            mkv = MKV(fh)
    except Exception as e:
        logging.debug(e)
        logging.error(
            f"Could not read Video metadata from {fullpath}, "
            "falling back to file_handler"
        )
        return file_handler(fullpath, **kwargs)

    return mkv.info.date_utc
