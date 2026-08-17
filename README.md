# XunYiWenYao Crawler System

## Project Overview

A multi-process web crawler built with Python for batch scraping Q&A content (titles and descriptions) from the medical consultation section of **XunYiWenYao** (xywy.com). The system adopts a **producer-consumer architecture** to achieve concurrent crawling, aggregates results via cross-process shared data, and finally persists structured data into an Excel file.

## Project Structure

```
├── main.py                 # Entry point, launches the crawler workflow
├── config
│   └── settings.py         # Request headers, Cookie, and anti-crawl config
├── core
│   ├── handler.py          # Core logic: HTTP requests, XPath parsing, data extraction
│   └── service.py          # Process management: producer/consumer scheduling
├── utils
│   └── utils.py            # Utilities: process queue construction, shared config
├── dao
│   └── save_data.py        # Data persistence: write results to Excel
└── save_file
    └── xunyiwenyao.xlsx    # Output result (auto-generated)
```

## Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Language        | Python 3.7+                         |
| HTTP Client     | requests                            |
| HTML Parsing    | lxml (XPath)                        |
| Data Processing | pandas                              |
| Excel Engine    | openpyxl                            |
| Concurrency     | multiprocessing (Producer-Consumer) |

## Installation

```bash
pip install requests lxml pandas openpyxl
```

## Usage

1. Clone or download the project.
2. Install dependencies (see above).
3. Run the entry point:

   ```bash
   python main.py
   ```

4. After crawling completes, results are saved to `save_file/xunyiwenyao.xlsx`.

## Core Implementation

### 1. Producer-Consumer Model
- **Producer process**: generates paginated URLs in batches and pushes them into a process-safe queue. After all URLs are produced, it injects **end signals** (one per consumer) into the queue.
- **Consumer processes (5 by default)**: concurrently pull URLs from the queue, parse each page to extract Q&A data, and append records to a cross-process shared list.

### 2. Multi-Process Data Safety
- Uses `multiprocessing.Manager` to create a shared list accessible across processes.
- **End-signal mechanism** replaces naive empty-queue checks, preventing consumers from exiting prematurely while the producer is still generating URLs.

### 3. Unified Persistence
- After all processes finish, the aggregated shared data is written to Excel in a single batch, avoiding file-write conflicts under concurrent access.

## Notes

1. This project is for **technical learning and research only**. Do not use it for commercial purposes. Please comply with the target website's `robots.txt` and terms of service.
2. Cookies have an expiration period. If requests fail or return empty data, update the Cookie in `config/settings.py`.
3. Page parsing relies on XPath expressions. If the target website structure changes, adjust the parsing rules in `core/handler.py` accordingly.
4. Request delays are built in to reduce frequency. Do not arbitrarily speed up requests, as this may trigger anti-crawl mechanisms.
