@web
Feature: Crear publicación

@user1 @web
Scenario: E001: Crear publicación básica
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I click on new post
    And I introduce the post title
    And I introduce the post content
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the new post title