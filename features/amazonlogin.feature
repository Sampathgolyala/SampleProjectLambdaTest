Feature: Amazonlogin

Scenario: Verify the User is redirected to Amazon sign in Page
  Given I click "Customer Service" link
  When I click "Computers" link
  Then I verify the title of the page as "Computers & Accessories: Buy Computers & Accessories Online at Low Prices in India - Amazon.in"