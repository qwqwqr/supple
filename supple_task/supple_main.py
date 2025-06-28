import numpy as np
import pandas as pd
from tqdm import tqdm

import supple_request as sr
import supple_data_recording as sdr


def all_result_data(file_path: str, num: int) -> list:
    result_data = []
    df = pd.read_excel(file_path, sheet_name='Sheet2')
    data = df['pmcid'].head(num).tolist()
    # data = df['doi'].tolist()

    for doi in tqdm(data):
        pmc_id = sr.req_to_check_pmc_id(doi)
        oa_status = not pd.isna(pmc_id)
        pdf = sr.check_pdf_via_ncbi_europepmc(pmc_id)

        if pdf is None:
            pdf = sr.check_pdf_via_unpaywall(doi, 'ngubpuabpgobuwuob123tbu2o@gmail.com')

        supplementary = sr.check_supplementary_files(pmc_id)

        oa_status = 1 if oa_status else 0
        supplementary = 1 if supplementary else 0

        result_data.append([doi, oa_status, pdf, pmc_id, supplementary])
    return result_data


file_path = r'C:\Users\e4e5q\PycharmProjects\PrForTests\supple_task\supple_data\result.xlsx'
data_test = all_result_data(file_path, 2119)
sdr.data_recording(data_test)
