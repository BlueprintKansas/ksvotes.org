# helpers
def click_submit(page):
    page.locator("xpath=//button[@type='submit']").click()

def test_happy_path(page):
    page.goto("/")
    page.locator("[name=name_first]").fill("Kris")
    page.locator("[name=name_last]").fill("Kobach")
    page.locator("[name=dob]").fill("03/26/1966")
    page.locator("[name=zip]").fill("66044")
    page.locator("[name=email]").fill("someone@example.com")
    page.locator("[name=email-confirm]").fill("someone@example.com")
    click_submit(page)
    assert page.url.endswith("/change-or-apply/")
    assert page.locator("text=Success").all_text_contents() == ["Success! We found your Kansas voter registration."]

def test_zipcode_required(page):
    page.goto("/")
    page.locator("[name=name_first]").fill("Kris")
    page.locator("[name=name_last]").fill("Kobach")
    page.locator("[name=dob]").fill("03/26/1966")
    page.locator("[name=email]").fill("someone@example.com")
    page.locator("[name=email-confirm]").fill("someone@example.com")
    click_submit(page)
    assert page.locator("text=Required").all_text_contents() == ["Required"]

def test_zipcode_pattern(page):
    page.goto("/")
    page.locator("[name=zip]").fill("1234")
    click_submit(page)
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == ["5 digit ZIP Code required"]

def test_last_name_required(page):
    page.goto("/")
    page.locator("[name=name_first]").fill("Kris")
    page.locator("[name=dob]").fill("03/26/1966")
    page.locator("[name=zip]").fill("66044")
    page.locator("[name=email]").fill("someone@example.com")
    page.locator("[name=email-confirm]").fill("someone@example.com")
    click_submit(page)
    assert page.locator("text=Required").all_text_contents() == ["Required"]

def test_first_name_required(page):
    page.goto("/")
    page.locator("[name=name_last]").fill("Kobach")
    page.locator("[name=dob]").fill("03/26/1966")
    page.locator("[name=zip]").fill("66044")
    page.locator("[name=email]").fill("someone@example.com")
    page.locator("[name=email-confirm]").fill("someone@example.com")
    click_submit(page)
    assert page.locator("text=Required").all_text_contents() == ["Required"]

def test_dob_required(page):
    page.goto("/")
    page.locator("[name=name_first]").fill("Kris")
    page.locator("[name=name_last]").fill("Kobach")
    page.locator("[name=zip]").fill("66044")
    page.locator("[name=email]").fill("someone@example.com")
    page.locator("[name=email-confirm]").fill("someone@example.com")
    click_submit(page)
    assert page.locator("text=Required").all_text_contents() == ["Required"]

def test_dob_munging(page):
    page.goto("/")
    page.locator("[name=dob]").fill("03261966")
    page.locator("[name=zip]").focus() # must blur dob field
    assert page.input_value("[name=dob]") == "03/26/1966"

def test_email_match(page):
    page.goto("/")
    page.locator("[name=email]").fill("someone@example.com")
    page.locator("[name=email-confirm]").fill("other@example.com")
    click_submit(page)
    assert page.locator("text=The email address does not match.").all_text_contents() == ["The email address does not match."]

def test_email_pattern(page):
    page.goto("/")
    page.locator("[name=email]").fill("someone@example")
    page.locator("[name=email-confirm]").fill("someone@example")
    assert page.locator("text=Must be a valid email address").all_text_contents() == ["Must be a valid email address"]

def test_email_required(page):
    page.goto("/")
    page.locator("[name=name_first]").fill("Kris")
    page.locator("[name=name_last]").fill("Kobach")
    page.locator("[name=zip]").fill("66044")
    page.locator("[name=dob]").fill("03261966")
    page.locator("[name=email-confirm]").fill("someone@example.com")
    click_submit(page)
    assert page.locator("text=Required").all_text_contents() == ["Required"]
