import os
import shutil
import subprocess as sp
import sys
import time
import urllib.request

import requests

import checkv
from checkv import utility


class DatabaseDownloader:
    def __init__(self, destination):
        self.url = "https://portal.nersc.gov/CheckV/"
        self.destination = destination
        self.version = (
            urllib.request.urlopen(self.url + "CURRENT_RELEASE.txt")
            .read()
            .decode("utf-8")
            .strip()
        )
        self.filename = self.version + ".tar.gz"
        self.output_file = os.path.join(self.destination, self.filename)

    def download(self):
        attempt = 0
        max_attempts = 5
        wait_seconds = 3
        database_url = self.url + self.filename

        while attempt < max_attempts:
            try:
                # Determine the size of the file already downloaded
                existing_size = (
                    os.path.getsize(self.output_file)
                    if os.path.exists(self.output_file)
                    else 0
                )
                headers = {"Range": f"bytes={existing_size}-"} if existing_size else {}
                with requests.get(
                    database_url, headers=headers, stream=True
                ) as response:
                    response.raise_for_status()  # Ensure we notice bad responses
                    total_size_in_bytes = (
                        int(response.headers.get("content-length", 0)) + existing_size
                    )
                    mode = "ab" if existing_size else "wb"
                    with open(self.output_file, mode) as fo:
                        for chunk in response.iter_content(chunk_size=8192):
                            fo.write(chunk)
                    # Check if download is complete
                    if os.path.getsize(self.output_file) >= total_size_in_bytes:
                        print("Download completed successfully.")
                        break  # Exit the loop if download is complete
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                attempt += 1
                print(f"Attempting to retry in {wait_seconds} seconds...")
                time.sleep(wait_seconds)
                continue  # Retry the download
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break  # Exit on any other error
        if attempt == max_attempts:
            print(f"Failed to download after {max_attempts} attempts.")

    def extract(self):
        shutil.unpack_archive(self.output_file, self.destination, "gztar")
        os.remove(self.output_file)

    def diamond_makedb(self):
        self.dbdir = os.path.join(
            self.destination, self.filename.replace(".tar.gz", "")
        )
        cmd = "diamond makedb "
        cmd += f"--in {self.dbdir}/genome_db/checkv_reps.faa "
        cmd += f"--db {self.dbdir}/genome_db/checkv_reps "
        cmd += f"--threads 1 "
        cmd += "1> /dev/null "
        cmd += f"2> {self.dbdir}/genome_db/checkv_reps.log "
        p = sp.Popen(cmd, shell=True)
        return_code = p.wait()
        if return_code != 0:
            msg = "\nError: DIAMOND database failed to build\n"
            msg += f"See log for details: {self.dbdir}/genome_db/checkv_reps.log"
            sys.exit(msg)


def fetch_arguments(parser):
    parser.set_defaults(func=main)
    parser.set_defaults(program="download_database")
    parser.add_argument(
        "destination",
        type=str,
        help="Directory where the database will be downloaded to.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress logging messages",
    )


def main(args):
    program_start = time.time()
    logger = utility.get_logger(args["quiet"])
    if not os.path.exists(args["destination"]):
        os.makedirs(args["destination"])

    logger.info(f"\nCheckV v{checkv.__version__}: download_database")

    logger.info("[1/4] Checking latest version of CheckV's database...")
    db = DatabaseDownloader(args["destination"])

    logger.info(f"[2/4] Downloading '{db.version}'...")
    db.download()

    logger.info(f"[3/4] Extracting '{db.version}'...")
    db.extract()

    logger.info(f"[4/4] Building DIAMOND database...")
    db.diamond_makedb()

    logger.info("Run time: %s seconds" % round(time.time() - program_start, 2))
    logger.info("Peak mem: %s GB" % round(utility.max_mem_usage(), 2))
