from __future__ import annotations

import os
import subprocess
from PyPDF2 import PdfReader

import logging
import sys
import os
import posixpath
import shutil
import filecmp
from pathlib import Path

import ocrmypdf

def filecompare(a, b):
    try:
        return filecmp.cmp(a, b, shallow=True)
    except FileNotFoundError:
        return False


























# Check for the presence of JBIG2 encoder and pngquant
def check_dependencies():
	try:
		subprocess.run("jbig2 --version", shell = True, check = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		print("JBIG2 encoder is available.")
	except (subprocess.CalledProcessError, FileNotFoundError):
		print("JBIG2 encoder is not available. This may affect PDF compression quality.")

	try:
		subprocess.run("pngquant --version", shell = True, check = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		print("pngquant is available.")
	except (subprocess.CalledProcessError, FileNotFoundError):
		print("pngquant is not available. This may affect image quality in PDFs.")


# Process PDFs in a specified directory with OCR, make them PDF/A compliant and optimize
def process_pdfs(pdf_directory, output_directory, language = 'eng'):
	check_dependencies()  # Check for necessary dependencies before processing

	# Ensure the output directory exists
	os.makedirs(output_directory, exist_ok = True)

	# List all PDF files in the directory
	pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
	print(pdf_files)

	for pdf_file in pdf_files:
		file_path = os.path.join(pdf_directory, pdf_file)

		# Define output paths
		output_pdf_path = os.path.join(output_directory, pdf_file)
		output_txt_path = os.path.join(output_directory, os.path.splitext(pdf_file)[0] + '.txt')

		# Build the command string for OCR
		command = (f"ocrmypdf --sidecar {output_txt_path} --skip-text --jbig2-lossy --optimize 3 -l {language} --output-type "
				   f"pdfa-1"
				   f" {file_path} {output_pdf_path}")

		try:
			# Run the OCRmyPDF command
			subprocess.run(command, shell = True, check = True)
			print(f"Processed {pdf_file}")
		except subprocess.CalledProcessError as e:
			print(f"Failed to process {pdf_file}: {e}")

	print("Processing complete.")



if __name__ == '__main__':
	log_file = 'log.txt'
	logging.basicConfig(
			level = logging.INFO,
			format = "%(asctime)s %(message)s",
			filename = log_file,
			filemode = "a",
			)

	pdf_directory = "/path/to/pdf/files"
	output_directory = "/path/to/output/files"
	logging.info(f"PDF directory {pdf_directory}")
	logging.info(f"Output directory {output_directory}")

	ocrmypdf.configure_logging(ocrmypdf.Verbosity.default)

	process_pdfs(pdf_directory, output_directory, language = 'eng')  # Default to English
