from jpype import *
import os
import jpype
from configuration import const

#jpype安装说明
# https://blog.csdn.net/shuihupo/article/details/79714949
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype
def getEncodePassword(strTransferKey, strDate):
    jvmPath = jpype.getDefaultJVMPath()
    jarPath = os.path.join(os.path.abspath('.'),  const._global_configuration().invokeJarPath)#第二个参数是jar包的路径
    jarDependency = os.path.join(os.path.abspath('.'),  const._global_configuration().invokeJarDependencyPath)
    # jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s;%s"%(jarPath, jarDependency))#启动jvm
    jvmStatus = jpype.isJVMStarted()
    if not jvmStatus:
        jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarPath, "-Djava.ext.dirs=%s" % jarDependency)
    # jpype.java.lang.System.out.println("Hello World")
    javaClass = jpype.JClass('tools.Utils')
    # javaInstance = javaClass()#创建类的实例，可以调用类里边的方法
    # encodeStr = javaInstance.getCipher(strTransferKey, strDate)
    encodeStr = javaClass.getCipher(strTransferKey, strDate)
    # jpype.shutdownJVM()#最后关闭jvm
    return encodeStr
# print(getEncodePassword('41227312490261166168189947899258', 'xjd12345'))