![1a](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/d1ce2b14-1bae-4842-95de-0e6aa66e027b)
![1b](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/ff3b9678-1450-432d-a24c-72d4cba3fadd)
![1c](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/36d85541-e538-447d-822f-40e22ecdfda3)
![1d](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/685fa221-291f-4839-977a-996575b48045)
![1e](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/6efa9253-d54e-4cec-9e2b-ecd999967c80)
![1f](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/43ba4414-063e-4fc5-9756-07a1ffb422ca)
![scp](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/bbc89f35-58a1-41ad-80b0-ac089c651a32)
![1h](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/63c2e675-892f-4570-b169-786323b94011)

  





Was able to setup gitpod and added the configuration to download aws-cli whenever gitpod is launched.

![1](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/a6553859-1406-4f99-b94e-b5e2eba86a73)



  





Recreated Logical Architecture Design in Ludichart.

![2](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/2f2b6c85-0b39-4edf-aab5-8cee7e5297f1)


[Ludi Charts Share Link](https://lucid.app/lucidchart/29a2bc3b-92f6-4cd1-ae2f-5296873b761b/edit?invitationId=inv_64938dd2-b1c3-4b51-b837-3ad8d5dfba80)


Also understood how to setup budget and alarms by following the cli commands given in journal/week0.md



How to resolve the issue of pushing the sensitive info to remote bymistake?

Using trufflehog and bfg


The primary purpose of BFG Repo-Cleaner is to remove specific files or content from the Git history, not from the working directory or the latest commit. When you use BFG Repo-Cleaner with options like --delete-files or --replace-text, it modifies the Git history by removing or replacing the specified content in the commits.

If you get to know your creds were being exposed, firstly go to aws and deactivate and delete them.

  
brew install trufflesecurity/trufflehog/trufflehog


  
brew install bfg

  
We can test using test-repo
   
trufflehog git https://github.com/trufflesecurity/test_keys --only-verified
  
then you test your own repo
  
trufflehog git https://github.com/bhanumalhotra123/repo_name --only-verified
  
Now once you have found the security issues, to replace those values we use tool called bfg

  
https://rtyley.github.io/bfg-repo-cleaner/
  
Remember to keep the requirements file out of the project repo so that it is not pushed to remote by mistake as it contains the sensitive data.

$ bfg --replace-text ../passwords.txt  my-repo.git

 ![3](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/1ab982df-30ec-4a9a-b7f5-066063798fcc)


If you want to remove specific strings from the actual content of files in the working directory or the latest commit, you need to manually modify the files, commit the changes, and push the new commit to the remote repository.




  Implemented cloudwatch logs

![1i](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/fc1b9122-8c5b-4c67-a5bc-45480fc696bb)


Implemented x-ray and x-ray subsegment
  
![1j](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/e69994a0-e76c-44ef-a7f5-8b54529ed1ce)
  
![1k](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/af7a808e-81c1-43dd-9d72-9b6c881e9385)
  
![1l](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/66d9949d-2d7e-48bf-88bd-17fc6eca2679)
  
![1m](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/9114a4ff-a69b-4df0-8132-4b1de1ac3256)

![1o](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/acd96495-5fc5-4293-92e3-1046e2d04360)
