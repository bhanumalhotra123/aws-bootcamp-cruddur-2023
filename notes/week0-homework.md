Was able to setup gitpod and added the configuration to download aws-cli whenever gitpod is launched.

![1](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/a6553859-1406-4f99-b94e-b5e2eba86a73)




Recreated Logical Architecture Design in Ludichart.

![2](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/2f2b6c85-0b39-4edf-aab5-8cee7e5297f1)


[Ludi Charts Share Link](https://lucid.app/lucidchart/29a2bc3b-92f6-4cd1-ae2f-5296873b761b/edit?invitationId=inv_64938dd2-b1c3-4b51-b837-3ad8d5dfba80)


Also understood how to setup budget and alarms by following the cli commands given in journal/week0.md



How to resolve the issue of pushing the sensitive info to remote bymistake?

Using trufflehog and bfg


The primary purpose of BFG Repo-Cleaner is to remove specific files or content from the Git history, not from the working directory or the latest commit. When you use BFG Repo-Cleaner with options like --delete-files or --replace-text, it modifies the Git history by removing or replacing the specified content in the commits.

If you want to remove specific strings from the actual content of files in the working directory or the latest commit, you need to manually modify the files, commit the changes, and push the new commit to the remote repository.