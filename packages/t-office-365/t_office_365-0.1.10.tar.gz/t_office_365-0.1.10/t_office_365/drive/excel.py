"""Excel class."""
from typing import List

import requests
from O365 import Account

from t_office_365.core import Core
from t_office_365.decorators import retry_if_exception
from t_office_365.endpoints import workbook_api
from t_office_365.utils import check_result


class Excel(Core):
    """Excel class is used for API calls to Excel."""

    def __init__(self, account: Account, drive_id: str) -> None:
        """Initializes an instance of the Excel class.

        :param:
        - account (O365.Account): The O365 Account used for authentication.
        - drive_id (str): The ID of the drive.
        """
        super().__init__(account)
        self.__drive_id = drive_id

    @retry_if_exception
    def get_sheet_names(self, file_id: str) -> dict:
        """Get sheet names from Excel file.

        :param:
        - file_id (str): The ID of the Excel file.

        :return:
            dict: The sheet names json.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        url = self.get_url(workbook_api.worksheets(self.__drive_id, file_id))
        result = requests.get(url, headers=self.headers())
        check_result(result, f"{file_id}")
        return result.json()

    @retry_if_exception
    def create_sheet(self, file_id: str, sheet_name: str) -> None:
        """Create a new sheet in Excel.

        :param:
        - file_id (str): The ID of the Excel file.
        - sheet_name (str): The name of the new sheet.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        url = self.get_url(workbook_api.worksheets(self.__drive_id, file_id))
        payload = {"name": sheet_name}
        result = requests.post(url, json=payload, headers=self.headers())
        check_result(result, f"{file_id}")

    @retry_if_exception
    def get_rows_values(
        self, file_id: str, sheet_name: str, max_row: int = 100, max_column: int = 26
    ) -> List[List[str]]:
        """Get rows values from Excel.

        :param:
        - file_id (str): The ID of the Excel file.
        - sheet_name (str): The name of the sheet.
        - max_row (int): The index of the last row to retrieve.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        result = self.get_rows_range_data(file_id, sheet_name, max_row=max_row, max_column=max_column)
        return result["values"]

    @retry_if_exception
    def get_rows_range_data(
        self,
        file_id: str,
        sheet_name: str,
        min_row: int = 1,
        max_row: int = 100,
        min_column: int = 1,
        max_column: int = 26,
    ) -> dict:
        """Get rows range data from Excel.

        :param:
        - file_id (str): The ID of the Excel file.
        - sheet_name (str): The name of the sheet.
        - max_row (int, optional): The index of the last row to retrieve.
        - max_column (int, optional): The index of the column to retrieve.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        url = self.get_url(
            workbook_api.get_row_endpoint(
                drive_id=self.__drive_id,
                file_id=file_id,
                sheet_name=sheet_name,
                min_row=min_row,
                max_row=max_row,
                min_column=self.__get_column_letter(min_column),
                max_column=self.__get_column_letter(max_column),
            )
        )
        result = requests.get(url, headers=self.headers())
        check_result(result, f"{file_id}")
        return result.json()

    @retry_if_exception
    def get_row_values(self, file_id: str, sheet_name: str, row: int, max_column: int = 26) -> List[str]:
        """Get rows values from Excel.

        :param:
        - file_id (str): The ID of the Excel file.
        - sheet_name (str): The name of the sheet.
        - row (int): The row index of the sheet to retrieve.
        - max_column (str): The max column index to retrieve.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        range_data = self.get_rows_range_data(file_id, sheet_name, min_row=row, max_row=row, max_column=max_column)
        try:
            return range_data["values"][0]
        except IndexError:
            raise ValueError(f"Unable to read values in {row} row.")

    @retry_if_exception
    def get_cell_value(self, file_id: str, sheet_name: str, row: int, column: int) -> str:
        """Get cell value from Excel.

        :param:
        - file_id (str): The ID of the Excel file.
        - sheet_name (str): The name of the sheet.
        - row (int): The row index of the row.
        - column (int): The column index of the cell.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        url = self.get_url(workbook_api.get_cell_endpoint(self.__drive_id, file_id, sheet_name, row - 1, column - 1))
        result = requests.get(url, headers=self.headers())
        check_result(result, f"Getting cell value from file {file_id}")
        try:
            return result.json()["values"][0][0]
        except IndexError:
            raise ValueError(f"Unable to read cell in {row} row, {column} column.")

    @retry_if_exception
    def update_cell_value(self, file_id: str, sheet_name: str, row: int, column: int, value: str) -> None:
        """Update cell value in Excel.

        :param:
        - file_id (str): The ID of the Excel file.
        - sheet_name (str): The name of the sheet.
        - row (int): The row index of the sheet to update.
        - column (int): The column index to update.
        - value: The new value to be set in the cell.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        url = self.get_url(workbook_api.get_cell_endpoint(self.__drive_id, file_id, sheet_name, row - 1, column - 1))
        payload = {"values": [[value]]}
        result = requests.patch(url, json=payload, headers=self.headers())
        check_result(result, f"{file_id}")

    @retry_if_exception
    def update_row_values(self, file_id: str, sheet_name: str, values: List[str], row: int) -> None:
        """Update row values in Excel.

        :param:
        - file_id (str): The ID of the Excel file.
        - sheet_name (str): The name of the sheet.
        - values: The new values to be set in the row.
        - row (int): The row index of the sheet to update.

        :raises:
        - BadRequestError: If there is a bad request.
        - UnexpectedError: If there is an unexpected error during the request.
        """
        url = self.get_url(
            workbook_api.get_row_endpoint(
                drive_id=self.__drive_id,
                file_id=file_id,
                sheet_name=sheet_name,
                min_row=row,
                max_row=row,
                max_column=self.__get_column_letter(len(values)),
            )
        )
        payload = {"values": [values]}
        result = requests.patch(url, json=payload, headers=self.headers())
        check_result(result, f"{file_id}")

    @staticmethod
    def __get_column_letter(column_int: int) -> str:
        """Get column letter."""
        if column_int < 1 or column_int > 702:
            raise ValueError("Column number must be greater than 0 and less than 703.")
        start_index = 1  # it can start either at 0 or at 1
        letter = ""
        while column_int > 25 + start_index:
            letter += chr(65 + int((column_int - start_index) / 26) - 1)
            column_int = column_int - (int((column_int - start_index) / 26)) * 26
        letter += chr(65 - start_index + (int(column_int)))
        return letter
