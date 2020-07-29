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
  print(context.browser.page_source)
  assert 'Check my registration' in context.browser.page_source

@given(u'I enter valid voter details')
def step_impl(context):
  """
    TODO
  """
  context.browser.find_element_by_name('username').send_keys('validusername')
  context.browser.find_element_by_name('password').send_keys('validpassword')


@when(u'I click on Submit button')
def step_impl(context):
  """
    Find the input button on the html page which has value = Submit
    and invoke .click()
  """
  context.browser.find_element_by_xpath(f"//input[@type='submit' and @value='Submit']").click()

