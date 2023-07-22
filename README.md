## Alexa Test Accounts Application

A simple 'test accounts' web database application was created based on the requirements of the Amazon Alexa team.

Part of the responsibilities of the Contextual Shopping Information (CSI) team at Amazon is to develop and test new 
functions for Alexa devices. In order to test new features, the team's engineers need to create multiple Amazon/Alexa accounts 
from various parts of the world to track the behaviour of each function in different locales. Therefore, a simple web 
database application was created to store the details of these test accounts, such as the purpose of the account 
(e.g. test feature abc or xyz), the corresponding locale and the engineer who created it.


### Current functions:

* Register User (Creates in database)
* Login User
* Logout User
* Create Accounts (Creates in database)
* View Accounts (Reads database)
* View User Accounts (Reads database)
* View Currently Testing (Reads database)
* Set Testing Status (Updates database)
* Update Account (Updates database)
* Remove Account (Deletes in database - ADMIN)

### Database Tables:

* Account
* Engineer
* django.contrib.auth.models.User

### Dependencies:
* [requirements.txt](https://github.com/fernawndabisinoto/web_app_project_assignment/blob/a234d8a11ade6c39534754eed3b205d5dfcba05c/requirements.txt) 