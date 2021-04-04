from sec_edgar_downloader import Downloader
import os

def download_latest_filing(file_type, ticker):
	dl = Downloader(os.getcwd())
	dl.get(file_type, ticker, amount=1)
	dl_path = os.getcwd() +'/sec-edgar-filings/{}/{}/'.format(ticker, file_type)

	inner_most_dir = [x[0] for x in os.walk(dl_path)][1]
	html_path = f'{inner_most_dir}/filing-details.html'
	txt_path = f'{inner_most_dir}/full-submission.txt'

	return (html_path, txt_path)

# html, txt = download_latest_filing("8-K","RPLA")
# print(html)
# print(txt)