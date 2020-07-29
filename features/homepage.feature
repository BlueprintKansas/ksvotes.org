Feature: HomePage
  """
  HomePage feature will test for successful load of home page
  """

  Scenario: Success home page load
    Given I navigate to home page
    Then Home page load is successful

  Scenario: Success valid voter details
    Given I enter valid voter details
    When I click on Submit button
    Then Step 0 completes with registration found

