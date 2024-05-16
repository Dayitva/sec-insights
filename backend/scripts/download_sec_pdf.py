from pathlib import Path
from typing import List, Optional

import pdfkit
from file_utils import filing_exists
from fire import Fire
from sec_edgar_downloader import Downloader
from distutils.spawn import find_executable
from tqdm.contrib.itertools import product
from app.core.config import settings

DEFAULT_OUTPUT_DIR = "data/"
# You can lookup the CIK for a company here: https://www.sec.gov/edgar/searchedgar/companysearch
DEFAULT_CIKS = [
    # AAPL
    "320193",
    # MSFT
    "789019",
    # AMZN
    "0001018724",
    # # GOOGL
    # "1652044",
    # # META
    # "1326801",
    # # TSLA
    # "1318605",
    # # NVDA
    # "1045810",
    # # NFLX
    # "1065280",
    # # PYPL
    # "0001633917",
    # # PFE (Pfizer)
    # "78003",
    # # AZNCF (AstraZeneca)
    # "901832",
    # # LLY (Eli Lilly)
    # "59478",
    # # MRNA (Moderna)
    # "1682852",
    # # JNJ (Johnson & Johnson)
    # "200406",
]

# DEFAULT_CIKS = [
#     # JBL
#     "898293",
#     # TER
#     "97210",
#     # WBD
#     "1437107",
#     # CMCSA
#     "1166691",
#     # AMAT
#     "6951",
#     # SNPS
#     "883241",
#     # ADSK
#     "769397",
#     # AVGO
#     "1730168",
#     # AKAM
#     "1086222",
#     # GOOG
#     "1652044",
#     # CPAY
#     "1175454",
#     # IBM
#     "51143",
#     # FSLR
#     "1274494",
#     # LYV
#     "1335258",
#     # SWKS
#     "4127",
#     # ADI
#     "6281",
#     # ENPH
#     "1463101",
#     # META
#     "1326801",
#     # EA
#     "712515",
#     # AAPL
#     "320193",
#     # KEYS
#     "1601046",
#     # NXPI
#     "1413447",
#     # TMUS
#     "1283699",
#     # ROP
#     "882835",
#     # PTC
#     "857005",
#     # PARA
#     "813828",
#     # VRSN
#     "1014473",
#     # FTNT
#     "1262039",
#     # TXN
#     "97476",
#     # FI
#     "798354",
#     # CSCO
#     "858877",
#     # ORCL
#     "1341439",
#     # CDNS
#     "813672",
#     # T
#     "732717",
#     # NVDA
#     "1045810",
#     # NTAP
#     "1002047",
#     # CHTR
#     "1091667",
#     # NOW
#     "1373715",
#     # WDC
#     "106040",
#     # PANW
#     "1327567",
#     # ANSS
#     "1013462",
#     # ACN
#     "1467373",
#     # GLW
#     "24741",
#     # MCHP
#     "827054",
#     # STX
#     "1137789",
#     # ADBE
#     "796343",
#     # MSFT
#     "789019",
#     # NWS
#     "1564708",
#     # CRM
#     "1108524",
#     # EPAM
#     "1352010",
#     # SMCI
#     "1375365",
#     # KLAC
#     "319201",
#     # OMC
#     "29989",
#     # QCOM
#     "804328",
#     # MSI
#     "68505",
#     # CDW
#     "1402057",
#     # AMD
#     "2488",
#     # JNPR
#     "1043604",
#     # ON
#     "1097864",
#     # QRVO
#     "1604778",
#     # JKHY
#     "779152",
#     # INTU
#     "896878",
#     # MPWR
#     "1280452",
#     # PAYC
#     "1590955",
#     # GPN
#     "1123360",
#     # UBER
#     "1543151",
#     # IT
#     "749251",
#     # HPQ
#     "47217",
#     # NFLX
#     "1065280",
#     # FOXA
#     "1754301",
#     # LRCX
#     "707549",
#     # FICO
#     "814547",
#     # VZ
#     "732712",
#     # HPE
#     "1645590",
#     # LDOS
#     "1336920",
#     # TYL
#     "860731",
#     # FTV
#     "1659166",
#     # GEN
#     "849399",
#     # ZBRA
#     "877212",
#     # INTC
#     "50863",
#     # BR
#     "1383312",
#     # CTSH
#     "1058290",
#     # TEL
#     "1385157",
#     # DIS
#     "1744489",
#     # IPG
#     "51644",
#     # DAY
#     "1725057",
#     # APH
#     "820313",
#     # FFIV
#     "1048695",
#     # GRMN
#     "1121788",
#     # ANET
#     "1596532",
#     # TRMB
#     "864749",
#     # FIS
#     "1136893",
#     # TDY
#     "1094285",
#     # MU
#     "723125",
#     # TTWO
#     "946581",
# ]

DEFAULT_FILING_TYPES = [
    "10-K",
]


def _download_filing(
    cik: str, filing_type: str, output_dir: str, limit=None, before=None, after=None
):
    dl = Downloader(settings.SEC_EDGAR_COMPANY_NAME, settings.SEC_EDGAR_EMAIL, output_dir)
    dl.get(filing_type, cik, limit=limit, before=before, after=after, download_details=True)


def _convert_to_pdf(output_dir: str):
    """Converts all html files in a directory to pdf files."""

    # NOTE: directory structure is assumed to be:
    # output_dir
    # ├── sec-edgar-filings
    # │   ├── AAPL
    # │   │   ├── 10-K
    # │   │   │   ├── 0000320193-20-000096
    # │   │   │   │   ├── primary-document.html
    # │   │   │   │   ├── primary-document.pdf   <-- this is what we want

    data_dir = Path(output_dir) / "sec-edgar-filings"

    for cik_dir in data_dir.iterdir():
        for filing_type_dir in cik_dir.iterdir():
            for filing_dir in filing_type_dir.iterdir():
                filing_doc = filing_dir / "primary-document.html"
                filing_pdf = filing_dir / "primary-document.pdf"
                if filing_doc.exists() and not filing_pdf.exists():
                    print("- Converting {}".format(filing_doc))
                    input_path = str(filing_doc.absolute())
                    output_path = str(filing_pdf.absolute())
                    try:
                        # fix for issue here:
                        # https://github.com/wkhtmltopdf/wkhtmltopdf/issues/4460#issuecomment-661345113
                        options = {'enable-local-file-access': None}
                        pdfkit.from_file(input_path, output_path, options=options, verbose=True)
                    except Exception as e:
                        print(f"Error converting {input_path} to {output_path}: {e}")


def main(
    output_dir: str = DEFAULT_OUTPUT_DIR,
    ciks: List[str] = DEFAULT_CIKS,
    file_types: List[str] = DEFAULT_FILING_TYPES,
    before: Optional[str] = None,
    after: Optional[str] = None,
    limit: Optional[int] = 5,
    convert_to_pdf: bool = True,
):
    print('Downloading filings to "{}"'.format(Path(output_dir).absolute()))
    print("File Types: {}".format(file_types))
    if convert_to_pdf:
        if find_executable("wkhtmltopdf") is None:
            raise Exception(
                "ERROR: wkhtmltopdf (https://wkhtmltopdf.org/) not found, "
                "please install it to convert html to pdf "
                "`sudo apt-get install wkhtmltopdf`"
            )
    for symbol, file_type in product(ciks, file_types):
        try:
            if filing_exists(symbol, file_type, output_dir):
                print(f"- Filing for {symbol} {file_type} already exists, skipping")
            else:
                print(f"- Downloading filing for {symbol} {file_type}")
                _download_filing(symbol, file_type, output_dir, limit, before, after)
        except Exception as e:
            print(
                f"Error downloading filing for symbol={symbol} & file_type={file_type}: {e}"
            )

    if convert_to_pdf:
        print("Converting html files to pdf files")
        _convert_to_pdf(output_dir)


if __name__ == "__main__":
    Fire(main)
