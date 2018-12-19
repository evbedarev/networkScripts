import os,re, ReadAccountData;

print ("current dir: " + os.getcwd());
# t = open(os.getcwd() + "\\profile.txt");
# # rowsFile = t.readlines();
# # for line in rowsFile:
# #     if len(re.findall(r'(?im)^username:(.+)', line)) > 0:
# #         username = re.findall(r'(?im)^username:(.+)', line);
# #     if len(re.findall(r'(?im)^password:(.+)', line)) > 0:
# #         password = re.findall(r'(?im)^password:(.+)', line);
# #
readAccData = ReadAccountData.ReadAccountDataFromFile(os.getcwd() + "\\profile.txt");
print("username: " + readAccData.read_username());
print("password: " + readAccData.read_password());
readAccData.close()