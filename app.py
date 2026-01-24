import zipfile
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Final, Mapping, Optional

import requests
from bs4 import BeautifulSoup


class AnexosDownloader:
    BASE_URL: Final[str] = ("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
    HEADERS: Final[Mapping[str, str]] = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def _get_page_content(self, url: str) -> str:
        """Fetch page content and return as text."""
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

    def _extract_pdf_links(self, soup: BeautifulSoup) -> Mapping[str, str]:
        """
        Extract PDF links for Anexo I and II from page content.
        Returns dictionary with 'Anexo I' and 'Anexo II' as keys.
        """
        links: dict[str, str] = {}
        pdf_links = soup.select('a.external-link[href$=".pdf"]')

        for link in pdf_links:
            link_text = link.text.strip()
            if "Anexo I" in link_text:
                links["Anexo I"] = str(link["href"])
            if "Anexo II" in link_text:
                links["Anexo II"] = str(link["href"])

        if not links:
            raise ValueError("No PDF links found for Anexo I or II")
        return links

    def _download_pdf(self, url: str, path: Path) -> None:
        """Download a PDF file from URL and save to specified path."""
        response = self.session.get(url)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)

    def _create_zip(self, files: Mapping[str, Path], zip_name: str) -> None:
        """Create ZIP archive with given files"""
        with zipfile.ZipFile(zip_name, "w") as zipf:
            for name, path in files.items():
                zipf.write(path, arcname=path.name)

    def run(self) -> Optional[str]:
        """Main method to execute the download and zip processes."""
        try:
            # Fetch and parse page
            html = self._get_page_content(self.BASE_URL)
            soup = BeautifulSoup(html, "html.parser")

            # Get PDF links
            pdf_links = self._extract_pdf_links(soup)
            required_anexos: set[str] = {"Anexo I", "Anexo II"}
            if not required_anexos.issubset(pdf_links.keys()):
                missing = required_anexos - pdf_links.keys()
                raise ValueError(f"Missing required anexos: {', '.join(missing)}")

            # Download PDFs to temp directory
            with TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                downloaded: dict[str, Path] = {}

                for name, url in pdf_links.items():
                    if name in required_anexos:
                        file_path = temp_path / f"{name}.pdf"
                        self._download_pdf(url, file_path)
                        downloaded[name] = file_path
                        print(f"Downloaded '{name}'")

                # Create ZIP with timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                zip_filename = f"anexos_{timestamp}.zip"
                self._create_zip(downloaded, zip_filename)

                print(f"Created ZIP archive: '{zip_filename}'")
                return zip_filename

        except requests.exceptions.RequestException as e:
            print(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        return None


if __name__ == "__main__":
    downloader = AnexosDownloader()
    result = downloader.run()
    if not result:
        print("Failed to create ZIP file")
