import requests
import numpy as np
import pandas as pd
from tqdm import tqdm

import urllib.request
import urllib.parse


def check_pdf_via_ncbi_europepmc(pmcid: str) -> str | None:
    pdf_url_ncbi = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
    pdf_url_europepmc = f"https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmcid}&blobtype=pdf"

    sources = [
        ("NCBI", pdf_url_ncbi),
        ("EuropePMC", pdf_url_europepmc)
    ]

    for source_name, url in sources:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )

            with urllib.request.urlopen(req) as response:
                final_url = response.geturl()
                content_type = response.headers.get('Content-Type', '')
                if final_url.endswith('.pdf') or 'application/pdf' in content_type:
                    return final_url

        except urllib.error.HTTPError as e:
            continue
            # print(f"{source_name}: Ошибка доступа - {e.code} {e.reason}")
        # except Exception as e:
        #     print(f"{source_name}: Ошибка - {str(e)}")
    return None


def check_pdf_via_unpaywall(doi: str, email: str) -> str | None:
    api_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("is_oa") and data.get("best_oa_location"):
            return data["best_oa_location"].get("url_for_pdf")

        return None

    except requests.exceptions.RequestException as e:
        # print(f"Ошибка запроса к Unpaywall: {e}")
        return None


def req_to_check_pmc_id(doi: str) -> str | None:
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={doi}&format=json"
    pmc_id = np.nan
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            response_data = response.json()
            is_oa = 'pmcid' in response_data['records'][0]
            if is_oa:
                pmc_id = response_data['records'][0]['pmcid']
                return pmc_id
            return pmc_id
        else:
            # print(f"Ошибка для DOI {doi}: {response.status_code}")
            return pmc_id

    except Exception as e:
        # print(f"Сбой для DOI {doi}: {str(e)}")
        return pmc_id


def check_supplementary_files(pmc_id: str) -> bool:
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc_id}/supplementaryFiles"

    try:
        response = requests.head(
            url,
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "").lower()
            return "xml" not in content_type
        return False

    except requests.exceptions.RequestException:
        return False


