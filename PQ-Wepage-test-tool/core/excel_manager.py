import openpyxl


class ExcelManager:

    REQUIRED_COLUMNS = [
        "ID",
        "Page",
        "Action",
        "Locator Type",
        "Locator",
        "Input",
        "Expected Result",
        "Validation",
        "Enabled"
    ]

    def __init__(self):

        self.test_cases = []

    def load_test_cases(self, file_path):

        self.test_cases = []

        try:

            workbook = openpyxl.load_workbook(
                file_path,
                data_only=True
            )

            sheet = workbook.active

            # ---------------------------------------------
            # Read Header
            # ---------------------------------------------

            headers = [
                cell.value
                for cell in sheet[1]
            ]

            # Remove spaces from header names
            headers = [
                str(header).strip()
                if header is not None
                else ""
                for header in headers
            ]

            # ---------------------------------------------
            # Validate Required Columns
            # ---------------------------------------------

            missing_columns = [
                column
                for column in self.REQUIRED_COLUMNS
                if column not in headers
            ]

            if missing_columns:

                return False, (
                    "Missing required columns:\n\n"
                    + "\n".join(missing_columns)
                )

            # ---------------------------------------------
            # Create Column Map
            # ---------------------------------------------

            column_map = {
                header: index
                for index, header in enumerate(headers)
            }

            # ---------------------------------------------
            # Read Test Cases
            # ---------------------------------------------

            for row in sheet.iter_rows(
                min_row=2,
                values_only=True
            ):

                # Ignore completely empty rows
                if not any(row):
                    continue

                test_case = {}

                for column in self.REQUIRED_COLUMNS:

                    index = column_map[column]

                    value = row[index]

                    if value is None:
                        value = ""

                    test_case[column] = str(value).strip()

                self.test_cases.append(test_case)

            # ---------------------------------------------
            # Return Test Cases
            # ---------------------------------------------

            return True, self.test_cases

        except Exception as e:

            return False, str(e)