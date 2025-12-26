@web
Feature: Asignar etiqueta

@user1 @web
Scenario: E011: Asignar etiqueta a publicación
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
    And I click within the tags list
    And I click on new tag
    And I introduce the tag name and slug
    And I introduce the tag description
    And I wait for 3 seconds
    And I click on save tag
    And I wait for 3 seconds
    And I click within the posts list
    And I click on the created post
    And I click on the post settings
    And I wait for 3 seconds
    And I assign the created tag to the post
    And I wait for 3 seconds
    Then I should see the assigned tag in the post