# helpers
def complete_step_0(page):
    page.goto("/demo")
    page.locator("[name=email-confirm]").fill("nosuchperson@example.com")
    assert page.input_value("[name=dob]") == "01/01/2000"
    page.locator("xpath=//button[@type='submit']").click()
    assert page.url.endswith("/change-or-apply/")
    assert page.locator("text=You are not registered").all_text_contents() == ["You are not registered to vote."]

def click_submit(page):
    page.locator("id=btn-next").click()

def click_register_now(page):
    page.locator("text=Register now!").click()

def click_apply_for_advance_ballot(page):
    page.locator("text=Apply for Advance Ballot").click()

def click_back(page):
    page.locator("id=btn-back").click()

def click_change_of_name(page):
    page.locator("id=has_prev_name").click()

def click_previous_address(page):
    page.locator("id=has_prev_addr").click()

def click_has_mailing_address(page):
    page.locator("id=has_mail_addr").click()

def create_signature(page):
    # 2 dots
    page.locator("id=signature >> canvas").click(position={"x": 10, "y": 10})
    page.locator("id=signature >> canvas").click(position={"x": 20, "y": 20})

def click_sign(page):
    page.locator("id=sign-button").click()

def select_county(page, county):
    page.locator("id=change-county-btn").click()
    page.select_option("select#county", label=county)
    page.locator("id=btn-apply").click()
