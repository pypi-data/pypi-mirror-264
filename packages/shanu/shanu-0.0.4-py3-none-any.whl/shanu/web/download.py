import os
from threading import Thread
import requests
from tqdm import tqdm


class DownloadThread(Thread):
    def __init__(self, url, start_byte, end_byte, part_number, progress_bar):
        super().__init__()
        self.url = url
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.part_number = part_number
        self.progress_bar = progress_bar

    def run(self):
        headers = {"Range": f"bytes={self.start_byte}-{self.end_byte}"}
        response = requests.get(self.url, headers=headers, stream=True)
        with open(f"part{self.part_number}", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    self.progress_bar.update(
                        len(chunk)
                    )  # Update the progress bar


def combine_parts(total_parts, output_file):
    with open(output_file, "wb") as outfile:
        for i in range(total_parts):
            with open(f"part{i}", "rb") as infile:
                outfile.write(infile.read())
            os.remove(f"part{i}")  # Clean up part file


def download_file_in_parts(url, num_parts, output_file):
    response = requests.head(url)
    content_length = int(response.headers.get("content-length", 0))
    part_size = content_length // num_parts

    progress_bar = tqdm(
        total=content_length, unit="B", unit_scale=True, desc="Downloading"
    )

    threads = []
    for i in range(num_parts):
        start_byte = i * part_size
        end_byte = (start_byte + part_size - 1) if i < num_parts - 1 else ""
        thread = DownloadThread(url, start_byte, end_byte, i, progress_bar)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    progress_bar.close()  # Close the progress bar
    combine_parts(num_parts, output_file)
