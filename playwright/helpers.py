# helpers
def complete_step_0(page):
    page.goto("/demo")
    page.locator("[name=email-confirm]").fill("nosuchperson@example.com")
    assert page.input_value("[name=dob]") == "01/01/2000"
    page.locator("xpath=//button[@type='submit']").click()
    assert page.url.endswith("/change-or-apply/")
    assert page.locator("text=You are not registered").all_text_contents() == ["You are not registered to vote."]

def click_submit(page):
    page.locator("xpath=//button[@type='submit']").click()

def click_register_now(page):
    page.locator("text=Register now!").click()

def click_apply_for_advance_ballot(page):
    page.locator("text=Apply for Advance Ballot").click()

def click_back(page):
    page.locator("id=btn-back").click()

def click_change_of_name(page):
    page.locator("id=has_prev_name").click()
