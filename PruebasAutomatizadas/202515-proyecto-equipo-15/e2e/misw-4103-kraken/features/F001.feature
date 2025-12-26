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
    And I wait for 2 seconds
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

@user2 @web
Scenario: E002: Crear publicación con imagen principal
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I wait for 2 seconds
    And I click on new post
    And I introduce the post title
    And I introduce the post content
    And I introduce the post feature image
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the new post title

@user3 @web
Scenario: E003: Crear publicación sin título
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I wait for 2 seconds
    And I click on new post
    And I introduce the post content
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the post title untitled

@user4 @web
Scenario: E004: Crear publicación sin contenido
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I wait for 2 seconds
    And I click on new post
    And I introduce the post title
    And I click the post content to leave it empty
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the new post title

@user5 @web
Scenario: E001_Apriori: Crear publicación básica con datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I wait for 2 seconds
    And I click on new post
    And I introduce the post title from apriori data
    And I introduce the post content from apriori data
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the new post title

@user6 @web
Scenario: E002_Apriori: Crear publicación con imagen principal con datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I wait for 2 seconds
    And I click on new post
    And I introduce the post title from apriori data
    And I introduce the post content from apriori data
    And I introduce the post feature image
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the new post title

@user7 @web
Scenario: E003_Apriori: Crear publicación sin título con datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I wait for 2 seconds
    And I click on new post
    And I introduce the post content from apriori data
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the post title untitled

@user8 @web
Scenario: E004_Apriori: Crear publicación sin contenido con datos apriori
    Given I navigate to page "<BASEURL>"
    And I wait for 2 seconds
    And I run this project
    And I wait for 2 seconds
    When I register or login into the site with email "<EMAIL>", user "<FULLNAME>", title "<SITETITLE>" and password "<PASSWORD>"
    And I wait for 5 seconds
    And I click within the posts list
    And I wait for 2 seconds
    And I click on new post
    And I introduce the post title from apriori data
    And I click the post content to leave it empty
    And I wait for 5 seconds
    And I click on publish
    And I click on continue
    And I click on publish right now
    And I close the window
    And I click on go back to posts
    Then I should see the new post title