import json
import socket
import _thread
import re
import time
from urllib import parse
import uuid
import traceback


class ContentType:
    data = {
        ".*": "application/octet-stream",
        ".tif": "application/x-tif",
        ".001": "application/x-001",
        ".301": "application/x-301",
        ".323": "text/h323",
        ".906": "application/x-906",
        ".907": "drawing/907",
        ".a11": "application/x-a11",
        ".acp": "audio/x-mei-aac",
        ".ai": "application/postscript",
        ".aif": "audio/aiff",
        ".aifc": "audio/aiff",
        ".aiff": "audio/aiff",
        ".anv": "application/x-anv",
        ".asa": "text/asa",
        ".asf": "video/x-ms-asf",
        ".asp": "text/asp",
        ".asx": "video/x-ms-asf",
        ".au": "audio/basic",
        ".avi": "video/avi",
        ".awf": "application/vnd.adobe.workflow",
        ".biz": "text/xml",
        ".bmp": "application/x-bmp",
        ".bot": "application/x-bot",
        ".c4t": "application/x-c4t",
        ".c90": "application/x-c90",
        ".cal": "application/x-cals",
        ".cat": "application/vnd.ms-pki.seccat",
        ".cdf": "application/x-netcdf",
        ".cdr": "application/x-cdr",
        ".cel": "application/x-cel",
        ".cer": "application/x-x509-ca-cert",
        ".cg4": "application/x-g4",
        ".cgm": "application/x-cgm",
        ".cit": "application/x-cit",
        ".class": "java/*",
        ".cml": "text/xml",
        ".cmp": "application/x-cmp",
        ".cmx": "application/x-cmx",
        ".cot": "application/x-cot",
        ".crl": "application/pkix-crl",
        ".crt": "application/x-x509-ca-cert",
        ".csi": "application/x-csi",
        ".css": "text/css",
        ".cut": "application/x-cut",
        ".dbf": "application/x-dbf",
        ".dbm": "application/x-dbm",
        ".dbx": "application/x-dbx",
        ".dcd": "text/xml",
        ".dcx": "application/x-dcx",
        ".der": "application/x-x509-ca-cert",
        ".dgn": "application/x-dgn",
        ".dib": "application/x-dib",
        ".dll": "application/x-msdownload",
        ".doc": "application/msword",
        ".dot": "application/msword",
        ".drw": "application/x-drw",
        ".dtd": "text/xml",
        ".dwf": "application/x-dwf",
        ".dwg": "application/x-dwg",
        ".dxb": "application/x-dxb",
        ".dxf": "application/x-dxf",
        ".edn": "application/vnd.adobe.edn",
        ".emf": "application/x-emf",
        ".eml": "message/rfc822",
        ".ent": "text/xml",
        ".epi": "application/x-epi",
        ".eps": "application/postscript",
        ".etd": "application/x-ebx",
        ".exe": "application/x-msdownload",
        ".fax": "image/fax",
        ".fdf": "application/vnd.fdf",
        ".fif": "application/fractals",
        ".fo": "text/xml",
        ".frm": "application/x-frm",
        ".g4": "application/x-g4",
        ".gbr": "application/x-gbr",
        ".": "application/x-",
        ".gif": "image/gif",
        ".gl2": "application/x-gl2",
        ".gp4": "application/x-gp4",
        ".hgl": "application/x-hgl",
        ".hmr": "application/x-hmr",
        ".hpg": "application/x-hpgl",
        ".hpl": "application/x-hpl",
        ".hqx": "application/mac-binhex40",
        ".hrf": "application/x-hrf",
        ".hta": "application/hta",
        ".htc": "text/x-component",
        ".htm": "text/html",
        ".html": "text/html",
        ".htt": "text/webviewhtml",
        ".htx": "text/html",
        ".icb": "application/x-icb",
        ".ico": "application/x-ico",
        ".iff": "application/x-iff",
        ".ig4": "application/x-g4",
        ".igs": "application/x-igs",
        ".iii": "application/x-iphone",
        ".img": "application/x-img",
        ".ins": "application/x-internet-signup",
        ".isp": "application/x-internet-signup",
        ".IVF": "video/x-ivf",
        ".java": "java/*",
        ".jfif": "image/jpeg",
        ".jpe": "application/x-jpe",
        ".jpeg": "image/jpeg",
        ".jpg": "application/x-jpg",
        ".js": "application/x-javascript",
        ".jsp": "text/html",
        ".la1": "audio/x-liquid-file",
        ".lar": "application/x-laplayer-reg",
        ".latex": "application/x-latex",
        ".lavs": "audio/x-liquid-secure",
        ".lbm": "application/x-lbm",
        ".lmsff": "audio/x-la-lms",
        ".ls": "application/x-javascript",
        ".ltr": "application/x-ltr",
        ".m1v": "video/x-mpeg",
        ".m2v": "video/x-mpeg",
        ".m3u": "audio/mpegurl",
        ".m4e": "video/mpeg4",
        ".mac": "application/x-mac",
        ".man": "application/x-troff-man",
        ".math": "text/xml",
        ".mdb": "application/x-mdb",
        ".mfp": "application/x-shockwave-flash",
        ".mht": "message/rfc822",
        ".mhtml": "message/rfc822",
        ".mi": "application/x-mi",
        ".mid": "audio/mid",
        ".midi": "audio/mid",
        ".mil": "application/x-mil",
        ".mml": "text/xml",
        ".mnd": "audio/x-musicnet-download",
        ".mns": "audio/x-musicnet-stream",
        ".mocha": "application/x-javascript",
        ".movie": "video/x-sgi-movie",
        ".mp1": "audio/mp1",
        ".mp2": "audio/mp2",
        ".mp2v": "video/mpeg",
        ".mp3": "audio/mp3",
        ".mp4": "video/mpeg4",
        ".mpa": "video/x-mpg",
        ".mpd": "application/vnd.ms-project",
        ".mpe": "video/x-mpeg",
        ".mpeg": "video/mpg",
        ".mpg": "video/mpg",
        ".mpga": "audio/rn-mpeg",
        ".mpp": "application/vnd.ms-project",
        ".mps": "video/x-mpeg",
        ".mpt": "application/vnd.ms-project",
        ".mpv": "video/mpg",
        ".mpv2": "video/mpeg",
        ".mpw": "application/vnd.ms-project",
        ".mpx": "application/vnd.ms-project",
        ".mtx": "text/xml",
        ".mxp": "application/x-mmxp",
        ".net": "image/pnetvue",
        ".nrf": "application/x-nrf",
        ".nws": "message/rfc822",
        ".odc": "text/x-ms-odc",
        ".out": "application/x-out",
        ".p10": "application/pkcs10",
        ".p12": "application/x-pkcs12",
        ".p7b": "application/x-pkcs7-certificates",
        ".p7c": "application/pkcs7-mime",
        ".p7m": "application/pkcs7-mime",
        ".p7r": "application/x-pkcs7-certreqresp",
        ".p7s": "application/pkcs7-signature",
        ".pc5": "application/x-pc5",
        ".pci": "application/x-pci",
        ".pcl": "application/x-pcl",
        ".pcx": "application/x-pcx",
        ".pdf": "application/pdf",
        ".pdx": "application/vnd.adobe.pdx",
        ".pfx": "application/x-pkcs12",
        ".pgl": "application/x-pgl",
        ".pic": "application/x-pic",
        ".pko": "application/vnd.ms-pki.pko",
        ".pl": "application/x-perl",
        ".plg": "text/html",
        ".pls": "audio/scpls",
        ".plt": "application/x-plt",
        ".png": "application/x-png",
        ".pot": "application/vnd.ms-powerpoint",
        ".ppa": "application/vnd.ms-powerpoint",
        ".ppm": "application/x-ppm",
        ".pps": "application/vnd.ms-powerpoint",
        ".ppt": "application/x-ppt",
        ".pr": "application/x-pr",
        ".prf": "application/pics-rules",
        ".prn": "application/x-prn",
        ".prt": "application/x-prt",
        ".ps": "application/postscript",
        ".ptn": "application/x-ptn",
        ".pwz": "application/vnd.ms-powerpoint",
        ".r3t": "text/vnd.rn-realtext3d",
        ".ra": "audio/vnd.rn-realaudio",
        ".ram": "audio/x-pn-realaudio",
        ".ras": "application/x-ras",
        ".rat": "application/rat-file",
        ".rdf": "text/xml",
        ".rec": "application/vnd.rn-recording",
        ".red": "application/x-red",
        ".rgb": "application/x-rgb",
        ".rjs": "application/vnd.rn-realsystem-rjs",
        ".rjt": "application/vnd.rn-realsystem-rjt",
        ".rlc": "application/x-rlc",
        ".rle": "application/x-rle",
        ".rm": "application/vnd.rn-realmedia",
        ".rmf": "application/vnd.adobe.rmf",
        ".rmi": "audio/mid",
        ".rmj": "application/vnd.rn-realsystem-rmj",
        ".rmm": "audio/x-pn-realaudio",
        ".rmp": "application/vnd.rn-rn_music_package",
        ".rms": "application/vnd.rn-realmedia-secure",
        ".rmvb": "application/vnd.rn-realmedia-vbr",
        ".rmx": "application/vnd.rn-realsystem-rmx",
        ".rnx": "application/vnd.rn-realplayer",
        ".rp": "image/vnd.rn-realpix",
        ".rpm": "audio/x-pn-realaudio-plugin",
        ".rsml": "application/vnd.rn-rsml",
        ".rt": "text/vnd.rn-realtext",
        ".rtf": "application/x-rtf",
        ".rv": "video/vnd.rn-realvideo",
        ".sam": "application/x-sam",
        ".sat": "application/x-sat",
        ".sdp": "application/sdp",
        ".sdw": "application/x-sdw",
        ".sit": "application/x-stuffit",
        ".slb": "application/x-slb",
        ".sld": "application/x-sld",
        ".slk": "drawing/x-slk",
        ".smi": "application/smil",
        ".smil": "application/smil",
        ".smk": "application/x-smk",
        ".snd": "audio/basic",
        ".sol": "text/plain",
        ".sor": "text/plain",
        ".spc": "application/x-pkcs7-certificates",
        ".spl": "application/futuresplash",
        ".spp": "text/xml",
        ".ssm": "application/streamingmedia",
        ".sst": "application/vnd.ms-pki.certstore",
        ".stl": "application/vnd.ms-pki.stl",
        ".stm": "text/html",
        ".sty": "application/x-sty",
        ".svg": "text/xml",
        ".swf": "application/x-shockwave-flash",
        ".tdf": "application/x-tdf",
        ".tg4": "application/x-tg4",
        ".tga": "application/x-tga",
        ".tiff": "image/tiff",
        ".tld": "text/xml",
        ".top": "drawing/x-top",
        ".torrent": "application/x-bittorrent",
        ".tsd": "text/xml",
        ".txt": "text/plain",
        ".uin": "application/x-icq",
        ".uls": "text/iuls",
        ".vcf": "text/x-vcard",
        ".vda": "application/x-vda",
        ".vdx": "application/vnd.visio",
        ".vml": "text/xml",
        ".vpg": "application/x-vpeg005",
        ".vsd": "application/x-vsd",
        ".vss": "application/vnd.visio",
        ".vst": "application/x-vst",
        ".vsw": "application/vnd.visio",
        ".vsx": "application/vnd.visio",
        ".vtx": "application/vnd.visio",
        ".vxml": "text/xml",
        ".wav": "audio/wav",
        ".wax": "audio/x-ms-wax",
        ".wb1": "application/x-wb1",
        ".wb2": "application/x-wb2",
        ".wb3": "application/x-wb3",
        ".wbmp": "image/vnd.wap.wbmp",
        ".wiz": "application/msword",
        ".wk3": "application/x-wk3",
        ".wk4": "application/x-wk4",
        ".wkq": "application/x-wkq",
        ".wks": "application/x-wks",
        ".wm": "video/x-ms-wm",
        ".wma": "audio/x-ms-wma",
        ".wmd": "application/x-ms-wmd",
        ".wmf": "application/x-wmf",
        ".wml": "text/vnd.wap.wml",
        ".wmv": "video/x-ms-wmv",
        ".wmx": "video/x-ms-wmx",
        ".wmz": "application/x-ms-wmz",
        ".wp6": "application/x-wp6",
        ".wpd": "application/x-wpd",
        ".wpg": "application/x-wpg",
        ".wpl": "application/vnd.ms-wpl",
        ".wq1": "application/x-wq1",
        ".wr1": "application/x-wr1",
        ".wri": "application/x-wri",
        ".wrk": "application/x-wrk",
        ".ws": "application/x-ws",
        ".ws2": "application/x-ws",
        ".wsc": "text/scriptlet",
        ".wsdl": "text/xml",
        ".wvx": "video/x-ms-wvx",
        ".xdp": "application/vnd.adobe.xdp",
        ".xdr": "text/xml",
        ".xfd": "application/vnd.adobe.xfd",
        ".xfdf": "application/vnd.adobe.xfdf",
        ".xhtml": "text/html",
        ".xls": "application/x-xls",
        ".xlw": "application/x-xlw",
        ".xml": "text/xml",
        ".xpl": "audio/scpls",
        ".xq": "text/xml",
        ".xql": "text/xml",
        ".xquery": "text/xml",
        ".xsd": "text/xml",
        ".xsl": "text/xml",
        ".xslt": "text/xml",
        ".xwd": "application/x-xwd",
        ".x_b": "application/x-x_b",
        ".sis": "application/vnd.symbian.install",
        ".sisx": "application/vnd.symbian.install",
        ".x_t": "application/x-x_t",
        ".ipa": "application/vnd.iphone",
        ".apk": "application/vnd.android.package-archive",
        ".xap": "application/x-silverlight-app"
    }


class Multipart:
    def __init__(self):
        self.name = None
        self.file_name = None
        self.data = None
        self.type = None


class Session:
    def __init__(self, name, value, time_size=30):
        self.__name = name
        self.__value = value
        self.__time = time_size
        self.__lost_time = time.time()

    def get_value(self):
        return self.__value


class Cookie:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Request:

    def __parsing(self, head: bytes):
        # 拆分请求头和请求体
        pack = head.split("\r\n\r\n".encode(), 1)
        head = pack[0].decode()
        body = ""
        if len(pack) > 1:
            body = pack[1]

        request_list_head = head.split("\r\n")

        # 解析请求行
        request_line = request_list_head[0].split(" ")
        path_list = request_line[1].split("?")
        path = path_list[0]
        if len(path_list) > 1 and path_list[1] != "":
            self.__param_parsing(path_list[1])

        self.__method = request_line[0]
        self.__major = request_line[1]
        self.__path = path

        # 解析请求头
        for i in range(1, len(request_list_head)):
            head_map_list = request_list_head[i].split(":")
            self.__head[head_map_list[0]] = head_map_list[1].replace(" ", "")

        # 针对POST解析请求体
        content_type = self.get_head("Content-Type")
        if content_type is not None and "application/x-www-form-urlencoded" in content_type:
            self.__param_parsing(body.decode())
        if content_type is not None and "multipart / form - data" in content_type:
            self.__multipart_parsing(body)

    def __multipart_parsing(self, body):
        """
        对多文件上传进行解析
        :param body: 原始请求体二进制数据
        :return: Node
        """
        # 对多文件拆解成块信息拆解
        q = "\r\n--" + self.get_head("Content-Type").split("=")[1] + "\r\n"
        body_list = body.split(q.encode())
        for i in body_list:
            multiparts = i.split("\r\n\r\n".encode(), 1)
            if len(multiparts) > 1:
                m = Multipart()
                multipart_string = multiparts[0].decode()
                names = re.findall('name="(.*?)"', multipart_string)

                m.name = names[0]
                if len(names) > 1:
                    m.file_name = names[1]
                m.data = multiparts[1]

                content_type = re.findall("Content-Type: (.*)", multipart_string)
                if len(content_type) > 0:
                    m.type = content_type[0]

                if m.type is None:
                    self.__params[m.name] = m.data.decode()
                    continue
                if "text" in m.type:
                    m.data = m.data.decode()
                self.__multipart[m.name] = m

    def __init__(self, request_data: bytes):
        """
        初始化操作
        :param request_data:带解析的完整数据
        """
        self.__params = {}
        self.__head = {}
        self.__method = ""
        self.__major = ""
        self.__path = ""
        self.__multipart = {}
        self.__cookie = {}
        self.__parsing(request_data)
        self.__cookie_parsing()
        self.__parsing_utf_8()
        self.session = {}

    def __param_parsing(self, params: str):
        """
        参数解析
        :param params: 待解析的参数字符串，
        :return: Node
        """
        params = params.split("&")
        for param_key_map in params:
            param_list = param_key_map.split("=")
            if len(param_list) == 2:
                self.__params[param_list[0]] = param_list[1]

    def show_view(self):
        return str(self.__dict__)

    def get_multipart(self, name) -> Multipart:
        """
        获取文件对象
        :param name: 获取的参数名称
        :return: Multipart对象
        """
        return self.__multipart.get(name)

    def get_cookie(self, name) -> Cookie:
        """
        获取Cookie参数
        :param name:cookie名称
        :return: cookie对象
        """

        return self.__cookie.get(name)

    def get_head(self, name) -> str:
        """
        获取请求头参数
        :param name:请参数名称
        :return: str
        """
        return self.__head.get(name)

    def get_param(self, name) -> str:
        """
        获取提交参数
        :param name: 参数名称
        :return: str
        """
        return self.__params.get(name)

    def get_path(self) -> str:
        """
        获取请求路径
        :return: str
        """
        return self.__path

    def get_method(self) -> str:
        """
        获取请求方式
        :return: str
        """
        return self.__method

    def get_major(self) -> str:
        """
        获取协议版本
        :return: str
        """
        return self.__major

    def show_head(self):
        for i in self.__head:
            print(f"{i}=>{self.__head[i]}")
        for i in self.__params:
            print(f"{i}=>{self.__params[i]}")
        for i in self.__cookie:
            print(f"{i}=>{self.__cookie[i]}")

    def __cookie_parsing(self):
        """
        cookie解析
        :return: Node
        """
        cookies = self.get_head("Cookie")
        if cookies is None:
            return
        cookies = cookies.split(";")
        for i in cookies:
            cookie_map = i.split("=")
            cookie = Cookie(cookie_map[0], cookie_map[1])
            self.__cookie[cookie.name] = cookie

    def __parsing_utf_8(self):
        for i in self.__params:
            self.__params[i] = parse.unquote(self.__params[i])
        for i in self.__cookie:
            self.__cookie[i].value = parse.unquote(self.__cookie[i].value)

    def get_session(self, name):
        if name in self.session:
            return self.session[name].get_value()
        else:
            return None

    def show_all_cookie(self):
        for i in self.__cookie:
            print(f"{i} -> {self.__cookie[i].value}")


class Response:

    def __init__(self, file_root):
        self.major = "HTTP/1.1"
        self.code = "200"
        self.msg = "OK"
        self.content_type = "text/html"
        self.header = None
        self.body = ""
        self.content_length = 0
        self.flag = "text"
        self.cookies = {}
        self.session = {}
        self.__root = file_root

    def __create_response_line(self):
        """
        生成相应行
        :return: str
        """
        return f"{self.major} {self.code} {self.msg} \r\n"

    def __create_response_head(self):
        """
        生成响应头
        :return: str
        """
        return f"Content-Length:{len(self.body)}\r\nContent-Type:{self.content_type}\r\n"

    def __create_cookie(self):
        """
        生成cookie的响应信息
        :return: str
        """
        if len(self.cookies) == 0:
            return ""
        string = ""
        for i in self.cookies:
            string += f"Set-Cookie:{i}={self.cookies[i].value}\r\n"
        return string

    def write_body(self, string: str):
        self.body = self.body + string

    def open_file(self, file_path):
        try:
            with open(self.__root + file_path, "rb") as f:
                self.body = f.read()
        except FileNotFoundError:
            self.code = 404
            self.msg = ""

    def set_cookie(self, name, value):
        self.cookies[name] = Cookie(name, value)

    def set_sessions(self, name, value):
        self.session[name] = Session(name, value)

    def encode(self) -> bytes:
        """
        生成二进制流
        :return: bytes
        """
        head = self.__create_response_line() + self.__create_response_head() + self.__create_cookie()
        head = head.encode()
        if not isinstance(self.body, bytes):
            body = ("\r\n" + self.body).encode()
        else:
            body = "\r\n".encode() + self.body
        return head + body


class Server:

    # 初始化操作
    def __init__(self, path, listen_size=10, address=("", 11451)):
        self.socket = socket.socket()
        self.socket.bind(address)
        self.socket.listen(listen_size)
        self.content_type = ContentType.data
        self.path = path
        self.all_session = {}
        self.servlet = {}
        self.index = {}
        self.flag = True

    def start(self):
        print("服务器已启动")
        while self.flag:
            client, address = self.socket.accept()
            _thread.start_new_thread(self.run, (client, address,))

    def run(self, client: socket.socket, address):
        request_data = client.recv(1024 * 1024 * 4)
        # 无效访问过滤
        if len(request_data) < 10:
            resp = Response(self.path)
            resp.code = 404
            resp.write_body("404 ERROR")
            client.send(resp.encode())
            return

        request = Request(request_data)
        # session解析
        session_cookie = request.get_cookie("SESSION_ID")
        session_id = None
        if session_cookie is not None:
            session_id = session_cookie.value
        if session_id is not None:
            session_map = self.all_session.get(session_id)
            if session_map is None:
                session_id = None
            else:
                request.session = session_map

        response = Response(self.path)
        path = request.get_path()
        if path in self.servlet:
            try:
                self.servlet[path].servlet(request, response)
            except:
                response.code = 500
                response.write_body("code:500 server error")
                traceback.print_exc()
        elif path in self.index:
            response.open_file(self.index[path])
        else:
            file_type = re.findall(".*(\..*)", path)
            response_type = self.content_type.get(".*")
            if len(file_type) > 0:
                if file_type[0] in self.content_type:
                    response_type = self.content_type[file_type[0]]
            response.content_type = response_type
            response.open_file(path)

        if len(response.session) > 0:
            if session_id is None:
                session_id = str(uuid.uuid4()).replace("-", "")
                self.all_session[session_id] = response.session
            else:
                self.all_session[session_id].update(response.session)
            response.set_cookie("SESSION_ID", session_id)

        client.send(response.encode())
        client.close()


class Servlet:
    def servlet(self, request: Request, response: Response):
        pass
