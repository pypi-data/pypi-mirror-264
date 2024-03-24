![Banner](https://cdn.discordapp.com/attachments/1092315227057561630/1221146760949272596/actkeys.png?ex=6611848b&is=65ff0f8b&hm=04e35eda04715e10e7ee19039571d0f44fa5ff6746500d36135c9f34c7c8bec4&)
<div align="center">
    </a>
    <br />
    
   [tagoWorks](https://tago.works/) - [AKoD](https://github.com/tagoworks/akod)
   

  Activating Keys on Discord Validating Package is coded to simplify the process of checking keys in your Python projects. Instead of taking up extra lines it handling decryption and key checking, AKoDAuth provides simple functions. You can use the validate function, passing in your email and key variables. AKoDAuth handles all the decryption and checking behind the scenes, allowing you to focus on your main code. For example, you can use `if akodauth.isValid(emailvar, licensekeyvar) == False:` to quickly check if a key is valid, without worrying about the details of the validation process. To use AKoDAuth in your code and key your software please visit https://github.com/t-a-g-o/vlod. View AKoDAuth's PyPi page at https://pypi.org/project/akodauth

</div>

# How to use AKoDAuth

1. Install AKoDAuth

   ```sh
   pip install AKoDAuth
   ```

2. Import & Set AKoD

   ```py
   import AKoDAuth
   ```

   * To set your private key use `AKoDAuth.privatekey('hehSUUXf3m33ns9Hwenj')`
   * To set your authentication webserver link use `AKoDAuth.publicserverkey('jweikAAAA-jemef-efj-_eneiebeufu_38h')`

3. Implement a way to get user input for email and key

4. Check if the account and key is valid using AKoDAuth.isValid()
   ```py
   if AKoDAuth.isValid(usernamevar, keyvar) == False:
      print("Invalid email or key")
   else:
      # Run your main code here
   ```
