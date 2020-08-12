import frida,sys
import time


test_hook = '''
Java.perform(
    function(){
        send('gggg')
        /*var e = Java.use('com.dianping.nvnetwork.tunnel.Encrypt.e')
        e.a.overload('java.lang.String').implementation = function(str){
            send('a string')
            //printstack()
            return this.a(str)
        }
        e.a.overload().implementation = function(){
            send('a none')
            //printstack()
            return this.a()
        }
        e.a.overload('com.dianping.nvnetwork.tunnel.Encrypt.e').implementation = function(p1){
            send('a e')
            //printstack()
            return this.a(p1)
        }
        e.a.overload('com.dianping.nvnetwork.tunnel.Encrypt.e$b').implementation = function(p1){
            send('e$b')
            //printstack()
            return this.a(p1)
        }
        e.a.overload('int', 'com.dianping.nvnetwork.tunnel.Encrypt.SocketSecureCell', 'com.dianping.nvnetwork.tunnel.Encrypt.SecureProtocolData').implementation = function(p1,p2,p3){
            send('a int SocketSecureCell SecureProtocolData')
            //printstack()
            return this.a(p1,p2,p3)
        }
        e.a.overload('com.dianping.nvnetwork.tunnel.Encrypt.SocketSecureCell', 'java.lang.String', 'int').implementation = function(p1,p2,p3){
            send('a SocketSecureCell string int')
            //printstack()
            return this.a(p1,p2,p3)
        }
        e.a.overload('com.dianping.nvnetwork.tunnel.Encrypt.c', 'com.dianping.nvnetwork.tunnel.Encrypt.d').implementation = function(p1,p2){
            send('a c d')
            //printstack()
            return this.a(p1,p2)
        }
        e.a.overload('com.dianping.nvnetwork.tunnel.Encrypt.e', 'com.dianping.nvnetwork.tunnel.Encrypt.e$a').implementation = function(p1,p2){
            send('a e e$a')
            //printstack()
            return this.a(p1,p2)
        }
        e.a.overload('com.dianping.nvnetwork.tunnel.Encrypt.SocketSecureCell', 'com.dianping.nvnetwork.tunnel.Encrypt.SecureProtocolData').implementation = function(p1,p2){
            send('a SocketSecureCell SecureProtocolData')
            //printstack()
            return this.a(p1,p2)
        }
        e.a.overload('com.dianping.nvnetwork.tunnel.Encrypt.e', 'boolean').implementation = function(p1,p2){
            send('a e boolean')
            //printstack()
            return this.a(p1,p2)
        }
        e.a.overload('boolean').implementation = function(p1){
            send('a boolean')
            //printstack()
            return this.a(p1)
        }
        e.a.overload('int', 'com.dianping.nvnetwork.tunnel.Encrypt.SocketSecureCell', 'java.lang.String', 'java.lang.String').implementation = function(p1,p2,p3,p4){
            send('a int SocketSecureCell str str')
            //printstack()
            return this.a(p1,p2,p3,p4)
        }
        
        e.d.implementation = function(){
            send('e.d')
            //printstack()
            return this.d()
        }*/

        var SocketSecureManager = Java.use('com.dianping.nvnetwork.tunnel.Encrypt.SocketSecureManager')
        SocketSecureManager.getEncriptData.implementation = function(p1){
            send('getEncriptData')
            //printstack()
            var ret = this.getEncriptData(p1)
            //send(ret.a)
            return ret
        }
        SocketSecureManager.encryptData.implementation = function(p1,p2){
            //send(p1)
            //send(p2)
            //printstack()
            var ret = this.encryptData(p1,p2)
            //send(ret.a)
            return ret
        }
        SocketSecureManager.decryptData.implementation = function(p1,p2){
            send('decryptData')
            //send(p1)
            //send(p2)
            //printstack()
            var ret = this.decryptData(p1,p2)
            //send(ret)
            //bytearr2string(ret)
            return ret
        }

        /*var tunnel2a = Java.use('com.dianping.nvnetwork.tunnel2.a')
        tunnel2a.isSocketConnected.implementation = function(){
            return false
        }*/

        /*var CandyJni = Java.use('com.meituan.android.common.candy.CandyJni')
        CandyJni.getCandyDataWithKeyForJava.implementation = function(p1,p2,p3){
            //send('p2 str')
            
            var res = bytearr2string(p2)

            if(-1 != res.search('/v7/')){
                send('p2:'+res)
                //printstack()
            }
            send('p3:'+p3)
            var ret = this.getCandyDataWithKeyForJava(p1,p2,p3)
            send('ret:'+ret)
            return ret
        }*/
    }
)

function printstack() {
    send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
}

function bytearr2string(ret){
    var buffer = Java.array('byte', ret);
    //console.log(buffer.length);
    var result = "";
    for(var i = 0; i < buffer.length; ++i){
        result+= (String.fromCharCode(buffer[i]));
    }
    return result
    //send(result);
}

'''

test_scipt = '''
//遍历已加载的类
Java.perform(
    function () {
        Java.enumerateLoadedClasses({
            onMatch: function (className) {
                if (-1 != className.search('.nvnetwork.tunnel.Encrypt')){
                    //send('class name:'+className)
                    traceClass(className);
                }
            },
            onComplete: function () {
            }
        });
        send('done')
});

//Hook指定类里的所有方法
function traceClass(classname) {
    try {
        //Hook住指定的类
        var target = Java.use(classname);

        //调用getDeclaredMethods方法获得该类的所有方法的声明
        var methods = target.class.getDeclaredMethods();

        //遍历所有方法的声明，拿到方法名和方法的重载名
        methods.forEach(function (method) {
            //得到方法名
            var methodName = method.getName();

            //得到方法的所有重载
            var overloads = target[methodName].overloads;

            //遍历该方法的所有重载，组装overload()里的参数
            overloads.forEach(function (overload) {
                var proto = "(";
                overload.argumentTypes.forEach(function (type) {
                    proto += type.className + ", ";
                });
                if (proto.length > 1) {
                    proto = proto.substr(0, proto.length - 2);
                }
                proto += ")";
                //send("hooking: " + classname + "." + methodName + proto);

                //组装overload完成， 开始Hook该方法
                overload.implementation = function () {
                    send(classname+'.'+methodName+proto)
                    printstack()
                    var args = [];
                    //var tid = getTid();
                    //var tName = getTName();
                    for (var j = 0; j < arguments.length; j++) {
                        args[j] = arguments[j] + ""
                    }
                    //enter(tid, tName, classname, methodName + proto, args);
                    var retval = this[methodName].apply(this, arguments);
                    //exit(tid, "" + retval);
                    return retval;
                }
            });
        });
    } catch (e) {
        send("'" + classname + "' hook fail: " + e)
    }
}


function printstack() {
    send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
}
'''

test_rpc = '''
rpc.exports = {
    getsig:function(bArr_str, str){
        var skcy=''
        Java.perform(function(){
            send('enter')
            var CandyJni = Java.use('com.meituan.android.common.candy.CandyJni')

            var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
            var context = currentApplication.getApplicationContext();
            
            send('jack:'+bArr_str)
            var JString = Java.use('java.lang.String')
            bArr_str = JString.$new(bArr_str)
            skcy = CandyJni.getCandyDataWithKeyForJava(context, bArr_str.getBytes(), str)
            send('tom')
            send(skcy)
        })
        return skcy
    }
}
'''


test_mt='''
Java.perform(
    function(){
        var SocketSecureManager = Java.use('com.dianping.nvnetwork.tunnel.Encrypt.SocketSecureManager')
        SocketSecureManager.getEncriptData.implementation = function(p1){
            send('enter getEncriptData')
            printstack()
            return this.getEncriptData(p1)
        },
        SocketSecureManager.decryptData.implementation = function(p1,p2){
            send('enter decriptData')
            printstack()
            return this.decryptData(p1,p2)
        }

        var tunnel2a = Java.use('com.dianping.nvnetwork.tunnel2.a')
        tunnel2a.isSocketConnected.implementation = function(){
            //send('enter isSocketConnected')
            //printstack()
            return false
        }
        var CandyJni = Java.use('com.meituan.android.common.candy.CandyJni')
        CandyJni.getCandyDataWithKeyForJava.implementation = function(p1,p2,p3){
            send('enter getCandyDataWithKeyForJava')
            //printstack()
            send("p2:"+p2)
            var ori = bytearr2string(p2)
            send(ori)
            send("p3:"+p3)
            var ret = this.getCandyDataWithKeyForJava(p1,p2,p3)
            send('ret:'+ret)
            return ret
        }
})

function printstack() {
    send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
}
function bytearr2string(ret){
    var buffer = Java.array('byte', ret);
    //console.log(buffer.length);
    var result = "";
    for(var i = 0; i < buffer.length; ++i){
        result+= (String.fromCharCode(buffer[i]));
    }
    return result
    //send(result);
}
'''


test_sky = '''
rpc.exports = {
    getsig:function(bArr, str){
        var skcy = ''
        Java.perform(function(){
            var CandyJni = Java.use('com.meituan.android.common.candy.CandyJni')

            var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
            var context = currentApplication.getApplicationContext();

            var JString = Java.use('java.lang.String')
            var bArr_str = JString.$new(bArr)
            skcy = CandyJni.getCandyDataWithKeyForJava(context, bArr_str.getBytes(), str)
        })
        return skcy
    }
}
'''


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


def test():
    process = frida.get_usb_device().attach('com.sankuai.meituan')
    script = process.create_script(test_mt)
    script.on('message', on_message)
    script.load()


    #device = frida.get_usb_device()
    #pid = device.spawn(['com.sankuai.meituan'])
    #device.resume(pid)
    #process = device.attach(pid)
    #script = process.create_script(test_scipt)
    #script.on('message', on_message)
    #script.load()

    #print('hook_prepare is ok')

    #ts = str(int(time.time()))
    #script.exports.getsig(ts)

    #script.exports.getsig(ts)
    #script.exports.getsig(ts)
    #script.exports.getsig(ts)
    #script.exports.getsig(ts)
    #script.exports.getsig(ts)
    #script.exports.getsig(ts)
    #script.exports.getsig(ts)

    sys.stdin.read()

def hook_prepare():
    process = frida.get_usb_device().attach('com.sankuai.meituan')
    script = process.create_script(test_sky)
    script.on('message', on_message)
    script.load()
    print('hook_prepare is ok')
    return script

#hook_prepare()
if __name__ == "__main__":
    test()