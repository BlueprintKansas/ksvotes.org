from helpers import *

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

def test_name(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_eighteen-0").click()
    page.locator("id=is_citizen-0").click()
    click_submit(page)
    assert page.url.endswith("/vr/name")
    # values are pre-filled from step0
    assert page.input_value("[name=prefix]") == ""
    assert page.input_value("[name=name_first]") == "No"
    assert page.input_value("[name=name_middle]") == "Such"
    assert page.input_value("[name=name_last]") == "Person"
    assert page.input_value("[name=suffix]") == ""
    # change middle name, then test it sticks
    page.locator("[name=name_middle]").fill("Other")
    click_submit(page)
    click_back(page)
    assert page.input_value("[name=name_middle]") == "Other"
    # add name change
    click_change_of_name(page)
    page.select_option("select#prev_prefix", label="Miss")
    page.locator("[name=prev_name_first]").fill("Previous No")
    page.locator("[name=prev_name_middle]").fill("Previous Other")
    page.locator("[name=prev_name_last]").fill("Previous Person")
    page.select_option("select#prev_suffix", label="III")
    click_submit(page)
