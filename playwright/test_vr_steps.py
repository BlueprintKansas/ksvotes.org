from helpers import complete_step_0, click_submit, click_register_now

def test_citizenship(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_citizen-1").click()
    click_submit(page)
    assert page.locator("text=Voter registration is only available to U.S. citizens.").inner_text().strip() == "Voter registration is only available to U.S. citizens."
    page.locator("id=is_eighteen-0").click() # either yes or no allowed
    page.locator("id=is_citizen-0").click() # only yes allowed to proceed
    click_submit(page)
    assert page.url.endswith("/vr/name")
