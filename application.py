from flask import Flask, jsonify, send_file
from fpdf import FPDF
import datetime
import os

app = Flask(__name__)


class FPDF(FPDF):
    def header(self):
        self.set_font('times', 'UB', 20)
        self.cell(0, 10, 'INVOICE', ln=1, align='C')

        return super().header()


class mkPdf():
    dt = datetime.datetime.now()
    pdf = FPDF('P', 'mm', (100, 150))

    rstName = ""
    invcNm = ""
    pdf.r_margin = 5
    pdf.l_margin = 5

    cusOrd = []
    billTotl = 0

    def getData(self):
        self.cusOrd.append({"iNm": "Burger", "iRt": 150, "iCt": 1})
        self.cusOrd.append({"iNm": "Pizza", "iRt": 399, "iCt": 1})
        self.cusOrd.append({"iNm": "Dosa", "iRt": 120, "iCt": 2})

    def genPdf(self):
        rpe = "₹"
        self.pdf.add_page()

        self.pdf.set_font('times', '', 10)
        self.pdf.cell(0, 10, self.rstName, ln=1, align="C")
        self.pdf.cell(0, 0, "---", ln=1, align="C")
        self.pdf.cell(0, 10, "33, Narayan Joshi Marg, Opp J D Bros, Kandivali (west)", ln=1, align="C")
        self.pdf.dashed_line(5, 39, 95, 39, dash_length=1, space_length=1)
        self.pdf.cell(40, 5, "DATE - " + str(self.dt.date()))
        self.pdf.cell(40, 5, "Time - " + str(self.dt.time()), ln=1)
        """ pdf.set_font('times','B',10) """
        self.pdf.cell(0, 5, 'Invoice NO. - ' + str(self.invcNm), ln=1)
        self.pdf.cell(0, 5, "Customer - Pranay", ln=1)
        self.pdf.dashed_line(5, 55.5, 95, 55.5, dash_length=2, space_length=2)
        self.pdf.set_font('times', '', 11)
        self.pdf.cell(0, 2, "", ln=1)
        self.billTotl = 0
        for i in range(len(self.cusOrd)):
            print(self.cusOrd[i]['iNm'])
            self.pdf.cell(30, 5.5, self.cusOrd[i]['iNm'], align="L")
            self.pdf.cell(30, 5.5, str(self.cusOrd[i]['iCt']) + " X " + str(self.cusOrd[i]['iRt']), align="C")
            self.pdf.cell(30, 5.5, "RS " + str(self.cusOrd[i]['iCt'] * self.cusOrd[i]['iRt']), ln=1, align="R")
            self.billTotl += self.cusOrd[i]['iRt'] * self.cusOrd[i]['iCt']

        self.pdf.cell(90, 6, 'Sub Total - RS ' + str(self.billTotl) + '/-', border="T", align='R', ln=1)
        self.pdf.cell(90, 6, 'GST 5% - ' + str((self.billTotl * 0.05)), align='R', ln=1)
        self.pdf.dashed_line(30, 98, 60, 98, dash_length=2, space_length=2)
        self.pdf.set_font('times', 'B', 11)
        self.pdf.cell(90, 6, 'Total - RS ' + str(self.billTotl + self.billTotl * 0.05) + '/-', border="", align='R',
                      ln=1)

        print(self.invcNm)

    def getPdf(self):
        self.pdf.output(str(self.invcNm) + '.pdf')


data = [
    {
        'coupon': "AnyCoupon",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    },
    {
        'coupon': "ABCD",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    },
    {
        'coupon': "2021Launch",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    },
    {
        'coupon': "MyCoupon",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    }
]


@app.route('/')
def index():
    return "hello"


@app.route("/pdf/<int:id>", methods=['get'])
def pdf(id):
    pdf = mkPdf()
    pdf.rstName = "My rst"
    pdf.invcNm = id
    pdf.getData()
    pdf.genPdf()
    pdf.getPdf()
    return send_file(str(id) + '.pdf', attachment_filename=str(id) + '.pdf')


@app.route("/fetch", methods=['get'])
def get():
    return jsonify(data)


@app.route("/check/coupon/<string:cid>", methods=['get'])
def getcoup(cid):
    myCoup = []
    for cp in data:
        if cp.get('coupon') == cid and cp.get('avbl') > 0:
            myCoup.append(cp)
    return jsonify(myCoup)


@app.route("/dec/coupon/code/gjsll/jdvcgh/dnjdkdl/dnhchchd/<string:cid>", methods=['get'])
def dec_coup(cid):
    for i in range(len(data)):
        if data[i]['coupon'] == cid:
            data[i]['avbl'] -= 1
            return jsonify(data[i]['avbl'])


@app.route("/update/coupon/code/gjsll/jdvcgh/dnjdkdl/dnhchchd/<string:cid>", methods=['get'])
def update_coup(cid):
    detl = cid.split("__")
    for i in range(len(data)):
        if data[i]['coupon'] == detl[0]:
            data[i]['avbl'] = int(detl[1])
            return jsonify(data[i]['avbl'])


@app.route("/coupon/code/gjsll/jdvcgh/dnjadddl/dnhchchd/<string:cid>", methods=['get'])
def add_coup(cid):
    detl = cid.split("__")
    if len(detl) == 4:
        data.append(
            {
                'coupon': detl[0],
                'dic': int(detl[1]),
                'avbl': int(detl[2]),
                'for': detl[3]
            }
        )
        return jsonify(
            {
                'coupon': detl[0],
                'dic': int(detl[1]),
                'avbl': int(detl[2]),
                'for': detl[3]
            }
        )
    else:
        return jsonify({"Invalid"})


if __name__ == '__main__':
    app.run(debug=True)
