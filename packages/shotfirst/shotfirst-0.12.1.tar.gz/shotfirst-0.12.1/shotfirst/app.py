import argparse
import fnmatch
import hashlib
import importlib
import json
import logging
import mimetypes
import multiprocessing
import os
import queue
import shutil
import sys
import threading
import traceback

import pyinotify

import shotfirst

# Default number of importers
DEFAULT_THREADS = multiprocessing.cpu_count()
TRUE_VALUES = (
    "yes",
    "1",
    "true",
)


class ImportHandler(pyinotify.ProcessEvent):

    config = {}

    def _make_conf(self, vals):
        values = vals.copy()

        if "mask" not in values:
            values["mask"] = ""

        if "operation" not in values:
            values["operation"] = "copy2"

        values["excludes"] = values.get("excludes", [])

        m = values.get("handler", "shotfirst.handlers.file_handler")

        try:
            mod = importlib.import_module(".".join(m.split(".")[:-1]))
            method = getattr(mod, m.split(".")[-1])
        except Exception:
            raise NotImplementedError(f"Handler {m} is not implemented")

        values["handler"] = method

        return values

    def my_init(self, config, threads=DEFAULT_THREADS):

        cfg = {}
        for keys, values in list(config.items()):
            assert "target" in values, (
                "Each item in the config must " "have a target declared"
            )
            for key in keys.split(","):
                k = key.strip()
                logging.debug(f"Loading {k}")
                cfg[k] = self._make_conf(values)
        self.config = cfg
        logging.debug(self.config)
        self.fileq = queue.Queue()

        for i in range(int(threads)):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            f = self.fileq.get()
            try:
                self.import_file(f)
            except Exception as e:
                logging.error(f"Failed to import {f}: {e}")
                logging.error(traceback.format_exc())
            self.fileq.task_done()

    def process_IN_CLOSE_WRITE(self, event):
        self.add_file(event.pathname)

    def process_IN_MOVED_TO(self, event):
        self.add_file(event.pathname)

    def add_file(self, fullpath):
        logging.debug(f"Analyzing {fullpath} for inclusion...")
        bname = os.path.basename(fullpath)
        try:
            (f_type, f_encoding) = mimetypes.guess_type(fullpath)
            logging.debug(f"{fullpath} is {f_type}")
            logging.debug(self.config[f_type])
            if f_type in self.config:
                for exclude in self.config[f_type]["excludes"]:
                    logging.debug(f"Comparing {bname} against {exclude}")
                    if fnmatch.fnmatch(bname, exclude):
                        logging.info(f"Excluding {fullpath} ({f_type})...")
                        return
                logging.info(f"Queueing {fullpath} ({f_type})...")
                self.fileq.put(fullpath)
            else:
                raise ValueError(f"Invalid or not-configured mime-type {f_type}")
        except Exception as e:
            logging.error(f"Error adding {fullpath}: {e}")
            return

    def _get_config(self, orig_file):
        (f_type, f_encoding) = mimetypes.guess_type(orig_file)
        cfg = self.config[f_type]
        logging.debug(cfg)
        return f_type, self.config[f_type]

    def import_file(self, orig_file):
        fname = os.path.basename(orig_file)
        mime_type, config = self._get_config(orig_file)
        dtime = config["handler"](orig_file, config=config)
        if not dtime:
            return False
        logging.info(f"Timestamp for {orig_file} is {dtime}")
        fsubdir = os.path.join(
            os.path.expanduser(config["target"]), dtime.strftime(config["mask"])
        )
        dest_file = os.path.join(fsubdir, fname)
        if os.path.exists(dest_file):
            logging.debug(f"Destination file {dest_file} already exists, comparing...")
            dest_md5 = hashlib.md5(open(dest_file, "rb").read()).hexdigest()
            orig_md5 = hashlib.md5(open(orig_file, "rb").read()).hexdigest()
            logging.debug(f"{orig_md5} == {dest_md5} ? {orig_md5 == dest_md5}")
            logging.info(f"Operation: {config['operation']}")
            if dest_md5 == orig_md5:
                msg = f"File {orig_file} was already processed. "
                if config["operation"].startswith("copy"):
                    msg += "Leaving source file alone"
                else:
                    msg += "Removing source file"
                    os.unlink(orig_file)
                logging.warn(msg)
                # if files checksums are identical, nothing else to do
                return
            else:
                msg = (
                    f"A file with the same name ({fname}) exists, "
                    "but it seems different. "
                )
                match config["operation"]:
                    case "copy2" | "move":
                        msg += "Leaving alone"
                        logging.warning(msg)
                        # if the operation is not meant to replace, nothing else to do
                        return
                    case "copy2replace" | "movereplace":
                        msg += "Removing destination file"
                        os.unlink(dest_file)
                logging.warning(msg)

        if not os.path.isdir(fsubdir):
            try:
                os.makedirs(fsubdir)
            except Exception as e:
                logging.debug(e)
        operation = getattr(shutil, config["operation"].replace("replace", ""))
        operation(orig_file, dest_file)
        logging.info(f"Imported {orig_file} -> {dest_file} (via {config['operation']})")


def import_file(handler, filename, filedir, log):
    if not filedir.endswith("/"):
        filedir += "/"

    fullpath = os.path.realpath(f"{filedir}{filename}")

    if os.path.isdir(fullpath):
        return

    handler.add_file(fullpath)


def get_mask(listen_events=["IN_MOVED_TO", "IN_CLOSE_WRITE"]):
    mask = 0
    while listen_events:
        mask = mask | getattr(pyinotify, listen_events.pop())

    return mask


def import_files(handler, paths, recurse, log=logging):
    for path in paths:
        logging.info(f"Import from {path}")
        if recurse:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    import_file(handler, filename, root, log)
        else:
            for filename in os.listdir(path):
                import_file(handler, filename, path, log)
    return 0


def load_config(config):
    jsonf = {}
    with open(config, "rb") as fh:
        jsonf = json.loads(fh.read())
    return jsonf


def os_true(var):
    v = os.environ.get(var, "false")
    return v.lower() in TRUE_VALUES


def main():
    if os_true("SDEBUG"):
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=shotfirst.__desc__,
    )
    parser.add_argument(
        "-v", "--version", action="version", version=shotfirst.__version__
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=os.environ.get("STHREADS") or DEFAULT_THREADS,
        help="Default number of worker threads to create",
    )
    parser.add_argument(
        "--no-auto-add",
        action="store_true",
        default=os_true("SNOAUTOADD"),
        help="Do not automatically watch sub-directories",
    )
    parser.add_argument(
        "--no-recurse",
        action="store_true",
        default=os_true("SNORECURSE"),
        help="Do not recurse",
    )
    parser.add_argument("config", nargs=1, help="JSON configuration file")
    parser.add_argument(
        "paths", metavar="path", nargs="+", help="Director(y|ies) to watch"
    )
    args = parser.parse_args()

    logging.info(
        f"Starting shotfirst v{shotfirst.__version__} (threads: {args.threads}, "
        f"recurse: {not args.no_recurse}, auto_add: {not args.no_auto_add})"
    )

    handler = ImportHandler(threads=args.threads, config=load_config(args.config.pop()))

    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)

    mask = get_mask()
    for path in args.paths:
        ret = wm.add_watch(
            os.path.expanduser(path),
            mask,
            rec=not args.no_recurse,
            auto_add=not args.no_auto_add,
        )
        if ret[path] == -1:
            logging.critical(f"add_watch failed for {path}, bailing out!")
            return 1

    import_files(handler, args.paths, not args.no_recurse)

    notifier.loop()


if __name__ == "__main__":
    sys.exit(main())
