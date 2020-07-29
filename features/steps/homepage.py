from behave import given, when, then


@given(u'I navigate to home page')
def step_impl(context):
  """
    Navigate to home page and as the web server will run in local when we run
    end to end tests using behave, the url will be http://127.0.0.1:5000/
  """
  context.browser.get('http://127.0.0.1:5000/')

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


@when(u'I click on Submit button')
def step_impl(context):
  """
    Find the input button on the html page which has value = Submit
    and invoke .click()
  """
  context.browser.find_element_by_xpath(f"//button[@type='submit']").click()

@then(u'Step 0 completes with registration found')
def step_impl(context):
  """
    Voter record found in SOS VoterView
  """
  print(context.browser.page_source)
  assert 'Success' in context.browser.page_source
