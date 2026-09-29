class TestEngine:

    def __init__(self, page, meter_ip):
        self.page = page
        self.meter_ip = meter_ip

    # -------------------------------------------------
    # Get Playwright locator
    # -------------------------------------------------

    def get_locator(self, locator_type, locator):

        locator_type = str(
            locator_type
        ).strip().lower()

        locator = str(
            locator
        ).strip()

        if locator_type == "id":

            return self.page.locator(
                f"#{locator}"
            )

        elif locator_type == "name":

            return self.page.locator(
                f'[name="{locator}"]'
            )

        elif locator_type == "css":

            return self.page.locator(
                locator
            )

        elif locator_type == "xpath":

            return self.page.locator(
                f"xpath={locator}"
            )

        elif locator_type == "text":

            return self.page.get_by_text(
                locator,
                exact=True
            )

        elif locator_type == "placeholder":

            return self.page.get_by_placeholder(
                locator
            )

        else:

            raise ValueError(
                f"Unsupported locator type: "
                f"{locator_type}"
            )

    # -------------------------------------------------
    # Navigate to page
    # -------------------------------------------------

    def navigate_to_page(self, page_name):

        page_name = str(
            page_name
        ).strip().lower()

        page_urls = {
            "settings":
                f"http://{self.meter_ip}/settings.html",
        }

        if page_name not in page_urls:

            raise ValueError(
                f"Unsupported page: {page_name}"
            )

        url = page_urls[
            page_name
        ]

        print(
            f"\nNavigating to: {url}"
        )

        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=10000
        )

        print(
            f"Page loaded: {page_name}"
        )

    # -------------------------------------------------
    # Execute one test step
    # -------------------------------------------------

    def execute_step(self, test_step):

        action = str(
            test_step.get(
                "Action",
                ""
            )
        ).strip().upper()

        locator_type = test_step.get(
            "Locator Type",
            ""
        )

        locator = test_step.get(
            "Locator",
            ""
        )

        input_value = test_step.get(
            "Input",
            ""
        )

        test_id = test_step.get(
            "ID",
            "UNKNOWN"
        )

        print(
            f"\nExecuting: {test_id}"
        )

        print(
            f"Action   : {action}"
        )

        print(
            f"Locator  : "
            f"{locator_type} = {locator}"
        )

        try:

            # -----------------------------------------
            # FILL
            # -----------------------------------------

            if action == "FILL":

                element = self.get_locator(
                    locator_type,
                    locator
                )

                element.fill(
                    str(input_value),
                    timeout=5000
                )

                print(
                    f"Input    : {input_value}"
                )

                print(
                    "Result   : PASS"
                )

                return True, "PASS"

            # -----------------------------------------
            # CLICK
            # -----------------------------------------

            elif action == "CLICK":
                element = self.get_locator(locator_type, locator)

                print(f"Matching elements: {element.count()}")
                print(f"Visible         : {element.is_visible()}")
                print(f"Enabled         : {element.is_enabled()}")
                print(f"Bounding box    : {element.bounding_box()}")

                try:
                    element.evaluate("el => el.click()")

                    print("DOM click      : PASS")
                    return True, "PASS"

                except Exception as error:
                    print("DOM click      : FAIL")
                    print(f"Error          : {error}")
                    return False, str(error)

            # -----------------------------------------
            # Unsupported action
            # -----------------------------------------

            else:

                message = (
                    f"Unsupported action: {action}"
                )

                print(
                    "Result   : FAIL"
                )

                print(
                    message
                )

                return False, message

        except Exception as error:

            print(
                "Result   : FAIL"
            )

            print(
                f"Error    : {error}"
            )

            return False, str(error)

    # -------------------------------------------------
    # Execute all test cases
    # -------------------------------------------------

    def execute_test_cases(self, test_cases):

        results = []

        current_test_case = None

        for test_step in test_cases:

            enabled = str(
                test_step.get(
                    "Enabled",
                    ""
                )
            ).strip().upper()

            if enabled != "YES":
                continue

            test_id = str(
                test_step.get(
                    "ID",
                    ""
                )
            ).strip()

            # -----------------------------------------
            # Convert:
            #
            # TC042-1 -> TC042
            # TC042-2 -> TC042
            # TC043-1 -> TC043
            # -----------------------------------------

            test_case_id = test_id.rsplit(
                "-",
                1
            )[0]

            page_name = str(
                test_step.get(
                    "Page",
                    ""
                )
            ).strip()

            # -----------------------------------------
            # New test case
            # -----------------------------------------

            if test_case_id != current_test_case:

                current_test_case = test_case_id

                print(
                    "\n=============================="
                )

                print(
                    f"STARTING TEST CASE: "
                    f"{test_case_id}"
                )

                print(
                    "=============================="
                )

                try:

                    self.navigate_to_page(
                        page_name
                    )

                except Exception as error:

                    print(
                        f"Page navigation failed: "
                        f"{error}"
                    )

                    results.append({
                        "ID": test_id,
                        "Page": page_name,
                        "Action":
                            test_step.get(
                                "Action",
                                ""
                            ),
                        "Locator":
                            test_step.get(
                                "Locator",
                                ""
                            ),
                        "Result":
                            f"FAIL - {error}"
                    })

                    continue

            # -----------------------------------------
            # Execute step
            # -----------------------------------------

            success, message = (
                self.execute_step(
                    test_step
                )
            )

            results.append({
                "ID": test_id,
                "Page": page_name,
                "Action":
                    test_step.get(
                        "Action",
                        ""
                    ),
                "Locator":
                    test_step.get(
                        "Locator",
                        ""
                    ),
                "Result": message
            })

        return results