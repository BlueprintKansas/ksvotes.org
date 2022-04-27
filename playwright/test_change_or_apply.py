# helpers
def complete_step_0(page):
    page.goto("/demo")
    page.locator("[name=email-confirm]").fill("nosuchperson@example.com")
    assert page.input_value("[name=dob]") == "01/01/2000"
    page.locator("xpath=//button[@type='submit']").click()
    assert page.url.endswith("/change-or-apply/")
    assert page.locator("text=You are not registered").all_text_contents() == ["You are not registered to vote."]

def test_register_now(page):
    complete_step_0(page)
    page.locator("text=Register now!").click()
    assert page.url.endswith("/vr/citizenship")
    assert page.locator("text=Citizenship").all_text_contents() == ["Citizenship and Age"]

def test_advance_ballot(page):
    complete_step_0(page)
    page.locator("text=Apply for Advance Ballot").click()
    assert page.url.endswith("/ab/election_picker")
    assert page.locator("text=Election(s)").all_text_contents() == ["Election(s)"]

def test_advance_ballot_status(page):
    complete_step_0(page)
    link = page.locator("text=Check advance ballot status")
    assert link.get_attribute("href") == "https://myvoteinfo.voteks.org/voterview"
    assert link.get_attribute("target") == "_blank"
