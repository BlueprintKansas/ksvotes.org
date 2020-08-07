from behave import given, when, then


@given(u'I navigate to home page')
def step_impl(context):
  """
    Navigate to home page and as the web server will run in local when we run
    end to end tests using behave, the url will be http://127.0.0.1:5000/
  """
  context.browser.get('http://127.0.0.1:5000/')

@given(u'I navigate to some site with embedded ksvotes form')
def step_impl(context):
  """
    External sites can xpost to ours
  """
  import pathlib
  example_form_path = str(pathlib.Path(__file__).parent.parent.absolute()) + '/someorg-form.html'
  print(example_form_path)
  context.browser.get('file://' + example_form_path)


@then(u'Home page load is successful')
def step_impl(context):
  """
    Home page has some telltale signs
  """
  assert 'Check my registration' in context.browser.page_source


@given(u'I enter valid voter details')
def step_impl(context):
  """
    Valid voter details will be found in SOS voter info
  """
  context.browser.find_element_by_name('name_first').send_keys('Kris')
  context.browser.find_element_by_name('name_last').send_keys('Kobach')
  context.browser.find_element_by_name('dob').send_keys('03/26/1966')
  context.browser.find_element_by_name('zip').send_keys('66044')
  context.browser.find_element_by_name('email').send_keys('someone@example.com')
  context.browser.find_element_by_name('email-confirm').send_keys('someone@example.com')


@given(u'I enter voter data on external form')
def step_impl(context):
  """
  """
  print(context.browser.page_source)
  context.browser.find_element_by_name('name_first').send_keys('Some')
  context.browser.find_element_by_name('name_last').send_keys('Body')
  context.browser.find_element_by_name('dob').send_keys('03/26/1970')
  context.browser.find_element_by_name('zip').send_keys('66044')
  context.browser.find_element_by_name('email').send_keys('someone@example.com')


@when(u'I click on Submit button')
def step_impl(context):
  """
    Find the input button on the html page which has value = Submit
    and invoke .click()
  """
  context.browser.find_element_by_xpath(f"//button[@type='submit']").click()


@when(u'I click submit')
def step_impl(context):
  """
  """
  context.browser.find_element_by_xpath(f"//input[@type='submit']").click()


@then(u'My voter details are prepopulated')
def step_impl(context):
  """
  """
  assert 'Check my registration' in context.browser.page_source
  assert context.browser.find_element_by_xpath(f"//input[@name='email']").get_attribute("value") == 'someone@example.com'


@then(u'Step 0 completes with registration found')
def step_impl(context):
  """
    Voter record found in SOS VoterView
  """
  assert 'Success' in context.browser.page_source
  assert '/change-or-apply/' in context.browser.current_url


@given(u'I enter a DOB indicating I am younger than 18')
def step_impl(context):
  from datetime import datetime
  this_year = str(datetime.now().year)
  context.browser.find_element_by_name('dob').send_keys('01/01/' + this_year)


@then(u'I get an error about my age')
def step_impl(context):
  print(context.browser.page_source)
  assert 'you are at least 16 years old' in context.browser.page_source
