class Loger():
    def ReadToList(self,filename):
        loglist = []
        filelog = open(filename, 'r')
        for line in filelog:
            loglist.append(line.strip())
        filelog.close()
        return loglist

    def LogWrite(self,filename, content):
        filelog = open(filename, "a")
        filelog.writelines(content.strip() + "\n")
        filelog.close()