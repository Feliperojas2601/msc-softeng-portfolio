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

@user2 @web
Scenario: E009: Editar imagen de una publicación
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click on new post
    And I introduce the post title
    And I introduce the post content
    And I introduce the post feature image
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
    And I modify the post image
    And I wait for 3 seconds
    And I press on update
    And I wait for 3 seconds
    Then I may confirm that the post image has been changed

@user3 @web @focus
Scenario: E010: Editar una publicación al restaurar una versión anterior
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click on new post
    And I introduce the post title
    And I introduce the post content
    And I introduce the post feature image
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I wait for 5 seconds
    And I click on the posts list
    And I wait for 5 seconds
    And I click on the posts list
    And I wait for 3 seconds
    And I click within the created post
    And I wait for 3 seconds
    And I modify the header
    And I wait for 3 seconds
    And I press on update
    And I wait for 3 seconds
    And I click on return to all posts
    And I wait for 3 seconds
    And I click within the modified post
    And I wait for 5 seconds
    And I click on the settings sidebar
    And I wait for 5 seconds
    And I scroll within the settings sidebar
    And I wait for 5 seconds
    And I click on the post history
    And I wait for 3 seconds
    And I click on the previous version
    And I wait for 5 seconds
    And I click on the restore button
    And I wait for 5 seconds
    And I click on restore post
    And I wait for 5 seconds
    And I get the restored post title value
    And I wait for 5 seconds
    And I click on return to all posts
    And I wait for 5 seconds
    And I click on the posts list
    And I wait for 3 seconds
    Then I should see the restored post title

@user4 @web
Scenario: E008_Apriori: Editar título de una publicación con datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click on new post
    And I introduce the post title from apriori data
    And I introduce the post content from apriori data
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
    And I modify the header from apriori data
    And I wait for 1 seconds
    And I press on update
    And I wait for 1 seconds
    And I click on return to posts
    And I wait for 1 seconds
    Then I should find the new post titled

@user5 @web
Scenario: E009_Apriori: Editar imagen de una publicación con datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click on new post
    And I introduce the post title from apriori data
    And I introduce the post content from apriori data
    And I introduce the post feature image
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
    And I modify the post image
    And I wait for 3 seconds
    And I press on update
    And I wait for 3 seconds
    Then I may confirm that the post image has been changed