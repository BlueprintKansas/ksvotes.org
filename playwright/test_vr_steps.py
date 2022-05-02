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
    assert page.locator("text=Previous Name").is_visible() == False
    click_change_of_name(page)
    assert page.locator("text=Previous Name").is_visible() == True
    page.select_option("select#prev_prefix", label="Miss")
    page.locator("[name=prev_name_first]").fill("Previous No")
    page.locator("[name=prev_name_middle]").fill("Previous Other")
    page.locator("[name=prev_name_last]").fill("Previous Person")
    page.select_option("select#prev_suffix", label="III")
    click_submit(page)
    assert page.url.endswith("/vr/address")
    # on back, the checkbox is checked and Previous Name section visible
    click_back(page)
    assert page.locator("text=Previous Name").is_visible() == True
    assert page.input_value("[name=prev_name_first]") == "Previous No"
    assert page.input_value("[name=prev_name_middle]") == "Previous Other"
    assert page.input_value("[name=prev_name_last]") == "Previous Person"
    assert page.input_value("[name=prev_prefix]") == "miss"
    assert page.input_value("[name=prev_suffix]") == "iii"
    # toggling checkbox clears input values
    click_change_of_name(page)
    assert page.locator("text=Previous Name").is_visible() == False
    click_change_of_name(page)
    assert page.locator("text=Previous Name").is_visible() == True
    assert page.input_value("[name=prev_name_last]") == ""
    assert page.input_value("[name=prev_prefix]") == ""
    click_submit(page)
    assert page.url.endswith("/vr/name") # validation prevents submit
    assert page.locator("text=Required").all_text_contents() == ["Required", "Required"] # first + last required
    click_change_of_name(page)
    assert page.locator("text=Previous Name").is_visible() == False
    click_submit(page)
    assert page.url.endswith("/vr/address")

def test_address(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_eighteen-0").click()
    page.locator("id=is_citizen-0").click()
    click_submit(page)
    click_submit(page)
    assert page.url.endswith("/vr/address")
    assert page.input_value("[name=addr]") == "123 Main St"
    assert page.input_value("[name=unit]") == ""
    assert page.input_value("[name=city]") == "Nowhere"
    assert page.input_value("[name=state]") == "KS"
    assert page.locator("[name=state]").get_attribute("readonly") == "readonly"
    assert page.input_value("[name=zip]") == "12345"
    # required fields
    for field in ["addr", "city", "zip"]:
        selector = f"[name={field}]"
        orig_value = page.input_value(selector)
        page.locator(selector).fill("")
        click_submit(page)
        assert page.locator("text=Required").all_text_contents() == ["Required"]
        page.locator(selector).fill(orig_value)
    # ZIP code pattern
    page.locator("[name=zip]").fill("1234")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == ["5 digit ZIP Code required"]
    page.locator("[name=zip]").fill("12345-123")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == ["5 digit ZIP Code required"]
    page.locator("[name=zip]").fill("12345-1234")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == []

    # repeat for previous address
    assert page.locator("text=What was your address where you were registered before?").is_visible() == False
    click_previous_address(page)
    assert page.locator("text=What was your address where you were registered before?").is_visible() == True
    # start empty
    assert page.input_value("[name=prev_addr]") == ""
    assert page.input_value("[name=prev_unit]") == ""
    assert page.input_value("[name=prev_city]") == ""
    assert page.input_value("[name=prev_state]") == ""
    assert page.input_value("[name=prev_zip]") == ""
    page.locator("[name=prev_addr]").fill("456 Any St")
    page.locator("[name=prev_unit]").fill("Apt A")
    page.locator("[name=prev_city]").fill("Some Place")
    page.locator("[name=prev_state]").fill("MO")
    page.locator("[name=prev_zip]").fill("00000")
    # required fields
    for field in ["prev_addr", "prev_city", "prev_state", "prev_zip"]:
        selector = f"[name={field}]"
        orig_value = page.input_value(selector)
        page.locator(selector).fill("")
        click_submit(page)
        assert page.locator("text=Required").all_text_contents() == ["Required"]
        page.locator(selector).fill(orig_value)
    # ZIP code pattern
    page.locator("[name=prev_zip]").fill("1234")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == ["5 digit ZIP Code required"]
    page.locator("[name=prev_zip]").fill("12345-123")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == ["5 digit ZIP Code required"]
    page.locator("[name=prev_zip]").fill("12345-1234")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == []

    # repeat for mailing address
    assert page.locator("text=What is the address where you get your mail?").is_visible() == False
    click_has_mailing_address(page)
    assert page.locator("text=What is the address where you get your mail?").is_visible() == True
    # start empty
    assert page.input_value("[name=mail_addr]") == ""
    assert page.input_value("[name=mail_unit]") == ""
    assert page.input_value("[name=mail_city]") == ""
    assert page.input_value("[name=mail_state]") == ""
    assert page.input_value("[name=mail_zip]") == ""
    page.locator("[name=mail_addr]").fill("999 Mailing Ave")
    page.locator("[name=mail_unit]").fill("Apt B")
    page.locator("[name=mail_city]").fill("Specific City")
    page.locator("[name=mail_state]").fill("NE")
    page.locator("[name=mail_zip]").fill("99999")
    # required fields
    for field in ["mail_addr", "mail_city", "mail_state", "mail_zip"]:
        selector = f"[name={field}]"
        orig_value = page.input_value(selector)
        page.locator(selector).fill("")
        click_submit(page)
        assert page.locator("text=Required").all_text_contents() == ["Required"]
        page.locator(selector).fill(orig_value)
    # ZIP code pattern
    page.locator("[name=mail_zip]").fill("1234")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == ["5 digit ZIP Code required"]
    page.locator("[name=mail_zip]").fill("12345-123")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == ["5 digit ZIP Code required"]
    page.locator("[name=mail_zip]").fill("12345-1234")
    assert page.locator("text=5 digit ZIP Code required").all_text_contents() == []

    # submit passes validation, advances to next page
    click_submit(page)
    assert page.locator("text=Required").all_text_contents() == []
    assert page.url.endswith("/vr/party")

    # back works, values are sticky
    click_back(page)
    assert page.locator("text=What was your address where you were registered before?").is_visible() == True
    assert page.input_value("[name=prev_addr]") == "456 Any St"
    assert page.input_value("[name=prev_unit]") == "Apt A"
    assert page.input_value("[name=prev_city]") == "Some Place"
    assert page.input_value("[name=prev_state]") == "MO"
    assert page.input_value("[name=prev_zip]") == "12345-1234"
    assert page.locator("text=What is the address where you get your mail?").is_visible() == True
    assert page.input_value("[name=mail_addr]") == "999 Mailing Ave"
    assert page.input_value("[name=mail_unit]") == "Apt B"
    assert page.input_value("[name=mail_city]") == "Specific City"
    assert page.input_value("[name=mail_state]") == "NE"
    assert page.input_value("[name=mail_zip]") == "12345-1234"

    # toggling checkbox clears fields
    click_previous_address(page)
    assert page.locator("text=What was your address where you were registered before?").is_visible() == False
    click_previous_address(page)
    assert page.locator("text=What was your address where you were registered before?").is_visible() == True
    assert page.input_value("[name=prev_addr]") == ""
    assert page.input_value("[name=prev_unit]") == ""
    assert page.input_value("[name=prev_city]") == ""
    assert page.input_value("[name=prev_state]") == ""
    assert page.input_value("[name=prev_zip]") == ""

    click_has_mailing_address(page)
    assert page.locator("text=What is the address where you get your mail?").is_visible() == False
    click_has_mailing_address(page)
    assert page.locator("text=What is the address where you get your mail?").is_visible() == True
    assert page.input_value("[name=mail_addr]") == ""
    assert page.input_value("[name=mail_unit]") == ""
    assert page.input_value("[name=mail_city]") == ""
    assert page.input_value("[name=mail_state]") == ""
    assert page.input_value("[name=mail_zip]") == ""

    click_submit(page)
    assert len(page.locator("text=Required").all_text_contents()) == 8
    click_previous_address(page)
    click_has_mailing_address(page)
    click_submit(page)
    assert page.url.endswith("/vr/party")

def test_address_verification(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_eighteen-0").click()
    page.locator("id=is_citizen-0").click()
    click_submit(page)
    click_submit(page)
    assert page.url.endswith("/vr/address")
    # demo address is fake so USPS verification should fail
    click_submit(page)
    assert page.url.endswith("/vr/party")
    assert len(page.locator("text=We couldn't verify your address with the Postal Service").all_text_contents()) == 1

    # use a legit address
    click_back(page)
    page.locator("[name=addr]").fill("753 Sunset Dr")
    page.locator("[name=city]").fill("Lawrence")
    page.locator("[name=zip]").fill("66044")
    click_submit(page)
    assert page.url.endswith("/vr/party")
    assert len(page.locator("text=753 SUNSET DR").all_text_contents()) == 1

def test_party(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_eighteen-0").click()
    page.locator("id=is_citizen-0").click()
    click_submit(page) # step 1
    click_submit(page) # step 2
    click_submit(page) # step 3
    assert page.url.endswith("/vr/party")
    page.select_option("select#party", label="")
    click_submit(page)
    assert len(page.locator("text=Required").all_text_contents()) == 1
    page.select_option("select#party", label="Democratic")
    assert page.input_value("[name=party]") == "Democratic"
    page.select_option("select#party", label="Republican")
    assert page.input_value("[name=party]") == "Republican"
    page.select_option("select#party", label="Unaffiliated")
    assert page.input_value("[name=party]") == "Unaffiliated"
    page.select_option("select#party", label="Libertarian")
    assert page.input_value("[name=party]") == "Libertarian"
    click_submit(page)
    assert page.url.endswith("/vr/identification")

def test_identification(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_eighteen-0").click()
    page.locator("id=is_citizen-0").click()
    click_submit(page) # step 1
    click_submit(page) # step 2
    click_submit(page) # step 3
    click_submit(page) # step 4
    assert page.url.endswith("/vr/identification")
    assert page.input_value("[name=identification]") == "NONE"
    page.locator("[name=identification]").fill("")
    click_submit(page)
    assert len(page.locator("text=Required").all_text_contents()) == 1
    page.locator("[name=identification]").fill("NONE")
    click_submit(page)
    assert page.url.endswith("/vr/preview")

def test_preview(page):
    complete_step_0(page)
    click_register_now(page)
    page.locator("id=is_eighteen-0").click()
    page.locator("id=is_citizen-0").click()
    click_submit(page) # step 1
    click_submit(page) # step 2
    click_submit(page) # step 3
    click_submit(page) # step 4
    click_submit(page) # step 5
    assert page.url.endswith("/vr/preview")
    page.locator("id=btn-clear-signature").click()
    click_sign(page)
    assert len(page.locator("text=Signature required").all_text_contents()) == 1
    create_signature(page)
    click_sign(page)
    assert page.url.endswith("/vr/affirmation")

def test_affirmation(page):
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
    assert page.url.endswith("/vr/affirmation")
    select_county(page, "Douglas")
    click_submit(page)
    assert len(page.locator("text=Required").all_text_contents()) == 1
    page.locator("[name=affirmation]").click()
    click_submit(page)
    assert page.url.endswith("/vr/submission")
    assert len(page.locator("text=Success!").all_text_contents()) == 1
