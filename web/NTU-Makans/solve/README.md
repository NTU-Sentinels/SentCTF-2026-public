# Solution

1. Players will explore the website. When browsing the various menus, inspecting the POST requests using Burpsuite or other tools will show a payload “category” being sent to the server.

2. By tampering with the payload value, players will be led to the 404 page where the error produced by the command used to read the menu files is displayed.

3. Try out different Linux commands gather information on the filesystem. Listing directory will show the presence of company_secrets directory. (category=noodles;ls+#)

4. If the player tries to use `cat` to read or access the **company\*secrets** directory with its full name, it will tell the player the string `cat` or `secret` was detected and hence the command is not executed.

- Players need to evade these checks using Linux knowledge, like using `tac`,`less`,`head` in place of `cat`, and using `?` or `*` to access the directory name and then the `secret` file. (`category=noodles;less+company\*???????/??????.txt+#)`

# Hints

1. In Linux, how to run more than 1 command at once?
2. In Linux, what special characters can be used to match patterns in filenames?
3. In Linux, there are multiple ways to read a file.
