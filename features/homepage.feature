Feature: HomePage
  """
  HomePage feature will test for successful load of home page
  """

  Scenario: Success home page load
    Given I navigate to home page
    Then Home page load is successful

  Scenario: Success valid voter details
    Given I navigate to home page
    Given I enter valid voter details
    When I click on Submit button
    Then Step 0 completes with registration found

  Scenario: Failure on invalid DOB
    Given I navigate to home page
    Given I enter a DOB indicating I am younger than 18
    When I click on Submit button
    Then I get an error about my age

  Scenario: Embedded ref form on external site
    Given I navigate to some site with embedded ksvotes form
    Given I enter voter data on external form
    When I click submit
    Then My voter details are prepopulated
