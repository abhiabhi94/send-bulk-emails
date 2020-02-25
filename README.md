## Send bulk emails by just cloning the script and putting the required data files in the cloned directory:

- `output_cleaned.xlsx` -- The file that contains list of all email address.
  - This file should contain the email addresses under the column same **_E-mail Address_**(This is important).
- `email-text.html` -- Contains email text to be sent in html form.
- `email-text.txt` -- Email text to be sent in text form(in case the above version fails)
- `credentials.json` -- Create a `json` file that contains the credentials of the email account to be used for sending the email. The format should be:  
   ```json
   {  
      "port": 465,  
      "smtp": "my stmp server address",  
      "sender": "user@domain",  
      "password": "mypassword",  
      "subject" : "Subject of the email"
   }
  ```
  - For using gmail use:  
    ```json
    "smtp" : "smtp.gmail.com"
    ```
- After executing the scripts, a file `sent_info.txt` will be created. It will contain information about the `indexes` and values where emails weren't sent alongwith the `exceptions`.
