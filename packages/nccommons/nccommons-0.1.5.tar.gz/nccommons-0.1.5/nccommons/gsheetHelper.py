from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json


class GsheetsLibraryHelper:
    ROBOT_LIBRARY_SCOPE = "SUITE"
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self):
        self.gauth_dict = {
            "type": "service_account",
            "project_id": "massive-vector-413710",
            "private_key_id": "d93f654bf56fc43fd9924bdfb5fe3d3dd302190e",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC1O1fnr+gsooGe\nPzJThHnVrUVflyzjCYbxWa9plyM8zSU2cCkPkbEaK2A8tp4wlYaQGWyUQpU+Wy4M\nwJn8N+g6+ECGis3xlVBL53r95/ULIh+Eo0l8PDfk7eTq3wSe+vXQnp4bArLw8CXR\nRPEkDEo24tQs0lgNhVKmpgR+QeihpSLOK9Y0UH6IrUyJ2W5YAj5C8NvZz+r3VK2q\nAiF/lhuZ7ly7kVgwKAXuJROQAzLJApP9Njy48q257DO6x8sdMbNhw1XQ+Z1rMx2n\n2v/lOJ+YFGVeYtmXc0PROY7t1v0tKPdEmxMdzh/kI78Wr36XeRoknPZkI9yt4ROd\nm/XHDsYJAgMBAAECggEAEtSfLh4bcCPUdvZXCtF9fUO7LRL+oXp4cHRiowSGr0cb\ngjwGMC1xquft4HETH7YxnKBfpUoDys5biwyqE0hV02a/AZvDiUH77V8YavBiiC0b\n/EKhHIz/O8SyH+tbRg+KYgpRIDpYEGvLaiKRMa8rOOe5pwyWBJWhQFqIpfvAKadb\nPssFxAqG6up+iLV7jFMHBIITjsAKYFZ227y+lm8GvFiQ4Fmk34CjTRCmu7M7MtBs\nriiD+3k5FV9hwWnH1w9ojyqy5cEv+uFljrNp+SOE69w5Uu+TXmFiHsb+nkG67rIx\nvLz+NC2+JdIveltFVuHN0zLPwxxy0CNlXfBMxrhOZwKBgQD11omCfTaX0hgoFZ87\nmb41r/xi8SO6NgHQsJiLoqBe+HgKHCu5MiPloSUiJ4chuCX6P7XBBtJE9k5MCnyJ\nCwLjdDSN6D/lJCUQK6Q1NCxvc8QuD9C0KQiQrNv0rvgXQoJjOZ5m0vQ7QSuoty6F\nvwN8qMwMkUXSzUrLEwj28ohIIwKBgQC8uSRToz2BOplfqGOeI6fHGhDym+HQdhpe\nuWdkiErwQLhZZI+Mo/7ezbALHA5oPvKwAwte9IeV1h1Yf67RVLwRty+zr1pfC1wB\n3WWgxY5DTQEEJ06iPzBHIH00ZH1e6tpKxhFLuW/+7nvmwgxr73sPABGKNHRwOaQB\nUx2xQMtl4wKBgQDYibXpqFzz8Wyxsgnlt5AhPfgzNm/fzz5eEY7sP7y+qmEhlpq0\nr4OK+hv5L5QJkWhyOrffZCDF+aYRuJLlKzvKGUtJS68sKGA1FBu5eVFCglfksq2E\nYzhWJsw/g/amlkC/IbtympHht4+7Nk7WI9/wZ8YDs9oqygT9RrD4w7xivQKBgAcw\nwqqRIKnI0skrQEhpMV5LpvOnbs4jgdO0GrVg4AIRZTS6uSFxqidRDPEPa5kbNOHx\n67/9byENXGbfzohZQyUlpqKg/r96TlIf3lxmyonT6EMBQGS8JZnAKiUR4xj3t8N7\nknMhKJw89+mN4S1HnZevt/tdDkasW4xVX18+icFjAoGAW/3e5UjbTPsu0YKtpobk\n8LEggRmAGUPKnMmvtNUZoMmqLKDDIDKLTwLiC8/NW1wcq9m9nhbHn1EwbQDdgpsu\nAleXOPMW1pUG1wjVOg5lEUDUkLrsmBrVdIFakYjDTI9jzWO72izkLhFugR6qYC/b\nm0ZK1watKt8g1aYjTV8wHBc=\n-----END PRIVATE KEY-----\n",
            "client_email": "webhook@massive-vector-413710.iam.gserviceaccount.com",
            "client_id": "103628700990269113192",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/webhook%40massive-vector-413710.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
}
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            self.gauth_dict
        )
        self.gc = gspread.authorize(credentials=self.credentials)

    def find_cell(self, gsheet_name, worksheet_name, value):
        """Finds a cell with the specified value in the worksheet.

        Args:
            worksheet_name (str): The name of the worksheet.
            value (str): The value to find.

        Returns:
            gspread.Cell: The cell object if found, None if not found.
        """
        try:
            self.sh = self.gc.open(gsheet_name)
            print("OUTPUTTTTTT",self.sh.worksheet(worksheet_name).findall(value)[0])
            return self.sh.worksheet(worksheet_name).findall(value)[0]
        except IndexError:
            return None
        
    def search_text_in_cell(self, gsheet_name, worksheet_name, value):
        """Searches for cells that contain the specified value in any column of the worksheet.

        Args:
            gsheet_name (str): The name of the Google Sheet.
            worksheet_name (str): The name of the worksheet.
            value (str): The value to search for.

        Returns:
            list: A list of cell objects if found, empty list if not found.
        """
        try:
            worksheet = self.gc.open(gsheet_name).worksheet(worksheet_name)
            cells_containing_value = []
            # Search through all cells in the worksheet
            cell_list = worksheet.get_all_values()
            for row_index, row in enumerate(cell_list, start=1):
                for col_index, cell in enumerate(row, start=1):
                    if value.lower() in cell.lower():  # Case-insensitive search
                        cells_containing_value.append(worksheet.cell(row_index, col_index))
            return cells_containing_value
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet '{worksheet_name}' not found in Google Sheet '{gsheet_name}'.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_values_list(self, gsheet_name, worksheet_name, row):
        """Returns a list of the values in the specified row of the worksheet.

        Args:
            worksheet_name (str): The name of the worksheet.
            row (int): The row number.

        Returns:
            list: A list of the values in the row.
        """
        try:
            self.sh = self.gc.open(gsheet_name)
            return self.sh.worksheet(worksheet_name).row_values(row)
        except IndexError:
            return []

    def delete_entire_row_in_worksheet(self, gsheet_name, worksheet_name, row):
        self.sh = self.gc.open(gsheet_name)
        self.sh.worksheet(worksheet_name).delete_rows(row)

    def clear_range_in_worksheet(self, gsheet_name, worksheet_name, cell_range):
        self.sh = self.gc.open(gsheet_name)
        self.sh.worksheet(worksheet_name).batch_clear(cell_range)

    def clear_entire_worksheet(self, gsheet_name, worksheet_name):
        self.sh = self.gc.open(gsheet_name)
        self.sh.worksheet(worksheet_name).clear()


if __name__ == "__main__":
    # Give Google Sheets access to rf-ui-automation@autoqa-385507.iam.gserviceaccount.com
    gshelper = GsheetsLibraryHelper()
    cell = gshelper.search_text_in_cell("feeds", "Sheet1", "65e96553-7d59254149d0672f2a5d21d0")
    if cell:
        print(cell)
        #print(f"Found something at R{cell.row}C{cell.col}")
        #print(cell.value)
        #values_list = gshelper.get_values_list("feeds", "Sheet1", cell.row)
        #print(values_list)
        #gshelper.delete_entire_row_in_worksheet("gs_demo", "Sheet1", cell.row)
        #gshelper.clear_range_in_worksheet("gs_demo", "Sheet1", ["A1:B1"])
        #gshelper.clear_entire_worksheet("gs_demo", "Sheet1")
    else:
        print("The value was not found")
