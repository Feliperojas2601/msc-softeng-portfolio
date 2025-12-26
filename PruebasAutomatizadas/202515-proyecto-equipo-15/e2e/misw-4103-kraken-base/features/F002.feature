@web
Feature: Crear página

@user1 @web
Scenario: E006: Crear página básica
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the pages list
    And I click on new page
    And I introduce the page title
    And I introduce the page content
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    Then I should see the new page title