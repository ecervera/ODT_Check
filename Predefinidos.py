import tornado
import tornado.ioloop
import tornado.web
import os, uuid

__UPLOADS__ = "uploads/"

from odt_parse import OdtData
from odt_diff import odt_compare

ref_name = './docs/libro_predefinidos.odt'
ref = OdtData(ref_name)


class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("Predefinidos.html")


class UploadAndCheck(tornado.web.RequestHandler):
    def post(self):
        try:
            fileinfo = self.request.files['filearg'][0]
            fname = fileinfo['filename']
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            fname = __UPLOADS__ + cname
            fh = open(fname, 'wb')
            fh.write(fileinfo['body'])
            doc = OdtData( fname, par_prop, text_prop )
            if doc.err:
                s = 'Error de lectura del fitxer\n'
            else:
                s = odt_compare(ref, doc)
        except KeyError:
            s = "No s'ha triat cap fitxer."
        s += '<br><hr><button type="button" onclick="javascript:history.back()">Back</button>'
        self.finish(s)


application = tornado.web.Application([
        (r"/", Userform),
        (r"/checkPredefinidos", UploadAndCheck),
        ], debug=True)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
