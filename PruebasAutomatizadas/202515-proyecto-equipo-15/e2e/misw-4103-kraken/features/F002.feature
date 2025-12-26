@web
Feature: Crear página

@user1 @web
Scenario: E001: Crear página básica
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

@user2 @web
Scenario: E002: Crear página con imagen principal
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
    And I introduce the page feature image
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    Then I should see the new page title

@user3 @web
Scenario: E001_Apriori: Crear página básica con datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the pages list
    And I click on new page
    And I introduce the page title from apriori data
    And I introduce the page content from apriori data
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    Then I should see the new page title

@user4 @web
Scenario: E002_Apriori: Crear página con imagen principal usando datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the pages list
    And I click on new page
    And I introduce the page title from apriori data
    And I introduce the page content from apriori data
    And I introduce the page feature image
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    Then I should see the new page title