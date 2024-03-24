#!env/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
import asyncio
import subprocess
from watchfiles import awatch, DefaultFilter


def TexFile(string):
    if not string.lower().endswith(".tex"):
        raise argparse.ArgumentTypeError("File must be a .tex file")
    return string


def only_tex(change, path):
    return path.endswith(".tex")


class Filter(DefaultFilter):
    allowed_extensions = ".tex"

    def __call__(self, change, path):
        print(f"Change: {change} Path: {path}")
        return super().__call__(change, path) and path.endswith(self.allowed_extensions)


class LatexHotReload:
    def __init__(self):
        self.tasks = set()

    async def handle_args(self, args):
        if args.file:
            await self.watch_file(args.file, args.directory)
            return

        print("No arguments provided. Use -h for help.")

    async def watch_file(self, file, directory):
        # Check if file exists
        if not os.path.exists(file):
            print(f"File {file} does not exist")
            return

        # Check if directory exists
        if directory and not os.path.exists(directory):
            print(f"Directory {directory} does not exist")
            return

        # Change to directory of file
        os.chdir(os.path.dirname(file))

        # Get filename
        texfile = os.path.basename(file)

        # Set filepath
        path = os.path.basename(directory) if directory else texfile

        # Clean artifacts
        for ext in [".aux", ".log", ".out", ".pdf"]:
            if os.path.exists(texfile.replace(".tex", ext)):
                os.remove(texfile.replace(".tex", ext))

        # Check for changes
        print(f"Watching for changes in {path}...")
        async for changes in awatch(path, watch_filter=only_tex):
            # Stop previous tasks
            if self.tasks:
                for task in self.tasks:
                    task.cancel()
                self.tasks.clear()

            await asyncio.sleep(0.5)

            # Start background tasks
            task = asyncio.create_task(self.build(texfile))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

    async def build(self, texfile):
        process = await asyncio.create_subprocess_shell(
            f"pdflatex {texfile}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            print(f"Reloaded.")
        else:
            print(f"Failed to build {texfile}")
            print(stderr.decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Reloads LaTeX files on change.")
    parser.add_argument(
        "-f", "--file", help="File to watch", type=TexFile, required=True
    )
    parser.add_argument(
        "-d", "--directory", help="Directory to watch", type=str, required=False
    )

    # Parse arguments
    args = parser.parse_args()

    latex = LatexHotReload()
    try:
        asyncio.run(latex.handle_args(args))
    except KeyboardInterrupt:
        print("Exiting...")
        for task in latex.tasks:
            task.cancel()


if __name__ == "__main__":
    main()
