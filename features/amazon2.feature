# Created by golyals at 14-06-2021
Feature: Do some other actions on Amazon site
  # Enter feature description here

Scenario: Verify the User is redirected to New Releases Page on Amazon App
  Given I click "New Releases" link
  When I click "Most Wished For" link
  Then I verify the title of the page as "Amazon.in Most Wished For: Items that customers have added to Wish Lists and registries most often on Amazon"