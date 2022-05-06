from helpers import *

def test_vr_to_ab(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_eighteen-0").click()
    page.locator("id=is_citizen-0").click()
    click_submit(page) # step 1
    click_submit(page) # step 2
    click_submit(page) # step 3
    click_submit(page) # step 4
    click_submit(page) # step 5
    create_signature(page)
    click_sign(page) # step 6
    select_county(page, "Douglas")
    page.locator("[name=affirmation]").click()
    click_submit(page)
    assert page.url.endswith("/vr/submission")
    assert len(page.locator("text=Success!").all_text_contents()) == 1
    page.locator("text=Apply for Advance Ballot").click()

    assert page.url.endswith("/ab/election_picker")
    page.locator("id=elections-0").check() # with AB_PRIMARY_DEADLINE set, Primary election is an option to .check instead of .click
    click_submit(page)
    assert page.url.endswith("/ab/election_picker")
    assert len(page.locator("text=Required >> visible=true").all_text_contents()) == 2 # help text + Party validation error
    page.select_option("select#party", label="Republican") # TODO in future this might optionally include Unaffiliated
    click_submit(page)

    assert page.url.endswith("/ab/identification")
    # no value will trigger modal with instructions
    click_submit(page)
    page.locator("id=confirm-modal-try-again").click()
    # any value is accepted
    page.locator("id=ab_identification").fill("K00-00-0000")
    click_submit(page)
    assert page.url.endswith("/ab/preview")
    select_county(page, "Douglas")
    create_signature(page)
    click_sign(page)
    page.locator("id=confirm-modal-ok").click()
    page.locator("[name=affirmation]").click()
    click_submit(page)
