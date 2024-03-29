import os
import subprocess


class downLoad:
    def __init__(self):
        self.Mount_Save = True

    def Move(self, original, final, identifier):
        if original == "2":
            stepThree = subprocess.Popen(["sudo umount /mnt/mydev"],
                                         shell=True,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         encoding='utf-8')
            stepThree.wait(2)
            if stepThree.poll() == 0:
                print("取消挂载成功！")
                if stepThree.stdout.read() != "":
                    print("输出：", stepThree.stdout.read())
            else:
                print("**取消挂载失败！")
                print("**错误：", stepThree.stderr.read())

            return True
        TAG = "/dev/sda1"
        if not os.path.exists("/mnt/mydev"):
            subp = subprocess.Popen(["sudo mkdir /mnt/mydev"],
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
            subp.wait(2)
            if subp.poll() == 0:  
                print("挂载文件已经创建成功！")
                if subp.stdout.read() != "":
                    print("输出：", subp.stdout.read())
            else:
                print("**挂载文件创建失败！")
                print("**错误：", subp.stderr.read())
        else:
            print("挂载文件已经存在！")
            pass

        subp = subprocess.Popen(["sudo fdisk -l"],
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')
        subp.wait(2)
        if subp.poll() == 0:  
            num = -1
            for index, line in enumerate(subp.stdout.readlines()):
                if line == "磁盘标识符：%s\n" % identifier:
                    num = index + 3
                if index == num:
                    TAG = line[0:9]
                    print("成功获取U盘标志！")
        else:
            print("**U盘标志获取失败！")
            print("**错误：", subp.stderr.read())
            pass

        stepOne = subprocess.Popen(["sudo mount %s /mnt/mydev" % TAG],
                                   shell=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   encoding='utf-8')
        stepOne.wait(2)
        if stepOne.poll() == 0:  
            print("挂载成功！")
            if stepOne.stdout.read() != "":
                print("输出：", stepOne.stdout.read())
        else:
            print("**挂载失败！")
            print("**错误：", stepOne.stderr.read())
            return False

        if original == "1":
            return True

        file_path = original.split("/")
        file_name = file_path[len(file_path) - 1]

        file_new_path = final.split("/")
        file_new_name = file_new_path[len(file_new_path) - 1]
        if not os.path.exists("/mnt/mydev/%s" % file_new_name):
            subp = subprocess.Popen(["sudo mkdir /mnt/mydev/%s" % file_new_name],
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
            subp.wait(2)
            if subp.poll() == 0:  
                print("U盘文件夹已经创建成功！")
                if subp.stdout.read() != "":
                    print("输出：", subp.stdout.read())
            else:
                print("**U盘文件夹创建失败！")
                print("**错误：", subp.stderr.read())
        else:
            print("U盘文件夹已经存在！")
            pass
        stepTwo = subprocess.Popen(["sudo cp %s %s" % (original, final)],
                                   shell=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   encoding='utf-8')
        stepTwo.wait(30)
        if stepTwo.poll() == 0:
            print("%s文件复制成功!" % file_name)
            if stepTwo.stdout.read() != "":
                print("输出：", stepTwo.stdout.read())
        else:
            print("**文件复制失败！")
            print("**错误：", stepTwo.stderr.read())

        stepThree = subprocess.Popen(["sudo umount /mnt/mydev"],
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     encoding='utf-8')
        stepThree.wait(2)
        if stepThree.poll() == 0:
            print("取消挂载成功！")
            if stepThree.stdout.read() != "":
                print("输出：", stepThree.stdout.read())
        else:
            print("**取消挂载失败！")
            print("**错误：", stepThree.stderr.read())

        return True


if __name__ == '__main__':
    mMove = downLoad()

    ori = "/home/topeet/test/start_rknn.sh"
    fin = "/mnt/mydev"
    id = "0xc009d7d1"

    flag = mMove.Move(ori, fin, id)

    print("操作标志：", flag)
