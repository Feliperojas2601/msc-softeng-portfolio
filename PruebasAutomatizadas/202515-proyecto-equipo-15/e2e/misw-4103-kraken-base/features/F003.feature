@web
Feature: Editar publicación

@user1 @web
Scenario: E008: Editar título de una publicación
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click on new post
    And I introduce the post title
    And I introduce the post content
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I wait for 5 seconds
    And I click on the posts list
    And I wait for 2 seconds
    And I click within the created post
    And I wait for 2 seconds
    And I modify the header
    And I wait for 1 seconds
    And I press on update
    And I wait for 1 seconds
    And I click on return to posts
    And I wait for 1 seconds
    Then I should find the new post titled