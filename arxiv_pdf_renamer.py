# pip install arxiv

'''
Author: Behzad Shomali
Date: 2022-12-23

To get help for the script, run:
    python arxiv_pdf_renamer.py -h
'''


import arxiv
import os
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser('Rename arxiv pdf files to the title of the paper')
    parser.add_argument('path', type=str, help='Path to the folder containing the pdf files')
    parser.add_argument('--delimiter', type=str, default='_', help='Delimiter to use for renaming the pdf files')
    parser.add_argument('--verbose', action='store_true', help='Print the title of the paper and its reference id')
    return parser.parse_args()

def get_pdf_info(pdf_file_path):
    """Get the title of the paper from the pdf file name"""
    
    reference_id = pdf_file_path.split('/')[-1][:-4]

    try:
        search = arxiv.Search(
            id_list=[reference_id],
            max_results=1,
        )

        result = next(search.results())
        title = result.title

        if verbose:
            if title is None:
                print(f'Paper title not found for {reference_id} :(')
            else:
                print(f'Paper title: {title}')
                print(f'Paper reference id: {reference_id}\n')
        
        return reference_id, title
    
    except Exception:
        return reference_id, None
    
def rename_pdf(pdf_file_path, delimiter):
    """Rename the pdf file to the title of the paper"""
    
    reference_id, title = get_pdf_info(pdf_file_path)
    
    if title is not None:
        new_file_path = pdf_file_path.replace(reference_id, title).strip().replace(' ', delimiter)
        os.rename(pdf_file_path, new_file_path)


if __name__ == '__main__':
    args = get_args()
    path = args.path
    delimiter = args.delimiter
    verbose = args.verbose
    
    pdf_file_names = [file_name for file_name in os.listdir(path) if file_name.endswith('.pdf')]
    for i, pdf_name in enumerate(pdf_file_names):
        print(f'Processing PDF file {i+1}/{len(pdf_file_names)}...')
        pdf_file_path = path + '/' + pdf_name
        rename_pdf(pdf_file_path, delimiter)