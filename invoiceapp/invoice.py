import os

from reportlab.lib import utils
from reportlab.lib.pagesizes import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak

from business_settings.models import BusinessInfo


def format_phone_number(value):
    """
    Function to format US based phone numbers.
    """
    if not value:
        return ''
    if len(value) == 10:
        phone = '({0}){1}-{2}'.format(value[0:3], value[3:6], value[6:10])
    elif len(value) == 11:
        phone = '+{0}({1}){2}-{3}'.format(value[0],
                                          value[1:4], value[4:7], value[7:11])
    else:
        phone = value

    return phone


class AlignedImage(Image):
    """
    This is used to align the business logo on the invoice page
    """

    def __init__(self, filename, hAlign='CENTER', **kwargs):
        Image.__init__(self, filename, **kwargs)
        self.hAlign = hAlign


def get_image(path, width=1 * cm):
    """
    Get a thumbnail of the logo to display on the invoice page
    """
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return AlignedImage(path, hAlign="CENTER", width=width,
                        height=(width * aspect))

# TODO: file path shoudl be None default, to return as buffer


def generate_invoice(invoice, services,
                                file_path="output_commercial_invoice.pdf"):  # self, request, *args, **kwargs):
    """
    Generate a pdf invoice using reportlab. This is based on fedex_commercial_invoice
    layout.
    """

    current_directory = os.path.dirname(os.path.realpath(__file__))

    print("Invoice gen: " + invoice.invoice_title)

    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    from reportlab.lib import colors

    # TODO: return as buffer vs file
    # if file_path = None then return buffer instead
    doc = SimpleDocTemplate(file_path, rightMargin=.5 * cm, leftMargin=.5 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    story = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Data',
                              alignment=TA_LEFT, fontSize=8, leading=7))
    styles.add(ParagraphStyle(name='Line_Data_Small',
                              alignment=TA_LEFT, fontSize=7, leading=8))
    styles.add(ParagraphStyle(name='Line_Data_Large',
                              alignment=TA_LEFT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Line_Data_Largest',
                              alignment=TA_LEFT, fontSize=14, leading=15))
    styles.add(ParagraphStyle(name='Line_Label', font='Helvetica-Bold',
                              fontSize=7, leading=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Label_Center',
                              font='Helvetica-Bold', fontSize=7, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Line_Label_Center_Large',
                              font='Helvetica-Bold', fontSize=12, alignment=TA_CENTER))

    # Comany address
    from address.models import Address
    if (len(BusinessInfo.objects.all()) == 1):
        busInfo = BusinessInfo.objects.all()[0]
    else:
        busInfo = BusinessInfo.objects.create(owner='Owner',
                                              business_name='Enter your business info first',
                                              address=Address.objects.create(
                                                  address_1='1 Main St',
                                                  city='City',
                                                  zip_code='00000',
                                                  phone_number='000-000-0000'),
                                              logo='icons/logo.png')

    # story.append(Paragraph(logo_image_path, styles["Left"]))

    if (busInfo.address.address_2):
        # Get company information
        company_address = '{0}<br />{1}<br />{2}, {3} {4}<br />Phone: {5}'.format(busInfo.address.address_1,
                                                                            busInfo.address.address_2,
                                                                            busInfo.address.city,
                                                                            busInfo.address.state,
                                                                            busInfo.address.zip_code,
                                                                            busInfo.address.phone_number)
    else:
        company_address = '{0}<br />{1}, {2} {3}<br />Phone: {4}'.format(busInfo.address.address_1,
                                                                    busInfo.address.city,
                                                                    busInfo.address.state,
                                                                    busInfo.address.zip_code,
                                                                    busInfo.address.phone_number)
    # Add Logo
    logo_image_path = os.path.join(os.path.dirname(
        current_directory), busInfo.logo.path)
    if logo_image_path:
        logo = get_image(logo_image_path, width=4 * cm)

        if logo:
            # Logo
            data1 = [
                [logo],
            ]

            # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
            t1 = Table(data1, colWidths=(4 * cm))

            t1.hAlign = 'CENTER'

            story.append(t1)
            # end logo

    data1 = [[Paragraph(busInfo.business_name, styles["Line_Data_Large"])],
             [Paragraph('', styles["Line_Label"])],
             [Paragraph(company_address, styles["Line_Data_Large"])],
             [Paragraph('', styles["Line_Label"])]

             ]

    # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
    t1 = Table(data1, colWidths=(9 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (0, 1), 0.25, colors.black),
        ('INNERGRID', (0, 2), (0, 3), 0.25, colors.black),
    ]))
    t1.hAlign = 'CENTER'
    t1.vAlign = 'TOP'

    story.append(t1)

    story.append(Spacer(0.1 * cm, 1 * cm))
    # End Company Address

    # Invoice title
    story.append(Paragraph("COMMERCIAL INVOICE", styles["Line_Label_Center"]))

    data1 = [[Paragraph('INVOICE NO.', styles["Line_Label"]),
              Paragraph(invoice.invoice_title, styles["Line_Data_Large"]),
              ]]

    t1 = Table(data1, colWidths=(4 * cm, 8.5 * cm,))
    t1.setStyle(TableStyle([
        ('INNERGRID', (1, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(t1)
    # End invoice title

    # Invoice dates
    data1 = [[Paragraph('DATE OF INVOICE', styles["Line_Label"]),
              Paragraph('DUE DATE', styles["Line_Label"])],
             [Paragraph(invoice.date_billed.strftime("%m/%d/%Y"), styles["Line_Data_Largest"]),
              Paragraph(invoice.date_due.strftime("%m/%d/%Y"),
                        styles["Line_Data_Largest"]),
              ]]
    t1 = Table(data1, colWidths=(9.6 * cm, 10 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        ('INNERGRID', (0, 1), (1, 1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)

    story.append(Spacer(0, 1 * cm))
    # End invoice dates

    # Line items header
    story.append(Paragraph("Line Items", styles["Line_Label_Center_Large"]))

    story.append(Spacer(0, 0.1 * cm))

    data1 = [[
        #   Paragraph('NO. OF<br />PKGS.', styles["Line_Label"]),
        Paragraph('TYPE OF<br />SERVICE', styles["Line_Label"]),
        Paragraph('SERVICE DESCRIPTION', styles["Line_Label"]),
        Paragraph('DURATION', styles["Line_Label"]),
        #   Paragraph('PET', styles["Line_Label"]),
        #   Paragraph('WEIGHT(Lbs)', styles["Line_Label"]),
        Paragraph('UNIT PRICE<br />($)', styles["Line_Label"]),
        Paragraph('TOTAL<br />VALUE($)', styles["Line_Label"])],
    ]

    t1 = Table(data1, colWidths=(3.0 * cm, 8 *
                                 cm, 2.7 * cm, 3.0 * cm, 2.9 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    # End line items header

    # Line items data
    products = []
    from invoiceapp.models import ServiceQuantity
    for service in services:
        serv_q = ServiceQuantity.objects.get(invoice=invoice, service=service)
        line_item = {}
        line_item['type'] = service.type_of_service
        line_item['description'] = service.description
        line_item['quantity'] = str(
            serv_q.quantity) + ' ' + str(service.per) + '(s)'
        line_item['unit_value'] = serv_q.price
        line_item['total_value'] = serv_q.total_price

        products.append(line_item)

    data1 = [[
        Paragraph(str(product['type']), styles["Line_Data"]),
        Paragraph(str(product['description']), styles["Line_Data"]),
        Paragraph(str(product['quantity']), styles["Line_Data"]),
        Paragraph(str(product['unit_value']), styles["Line_Data"]),
        Paragraph(str(product['total_value']), styles["Line_Data"])] for product in products]

    t1 = Table(data1, colWidths=(3.0 * cm, 8 *
                                 cm, 2.7 * cm, 3.0 * cm, 2.9 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    # End line items data

    # Invoice total
    total_value = 0.0

    # Use this as a template to align the logo
    # then remove the unnecessary parts
    data1 = [['',
              '',
              '',
              '',
              '',
              Paragraph('TOTAL INVOICE VALUE', styles["Line_Label"]),
              ],
             ['',
              '',
              '',
              '',
              '',
              Paragraph('${0}'.format(invoice.invoice_total),
                        styles["Line_Data"]),
              ]]

    t1 = Table(data1, colWidths=(1.7 * cm, 1.3 * cm,
                                 11.5 * cm, 1.4 * cm, 0.8 * cm, 2.9 * cm))
    t1.setStyle(TableStyle([
        # ('INNERGRID', (1, 0), (1, 1), 0.25, colors.black),
        # ('INNERGRID', (3, 0), (3, 1), 0.25, colors.black),
        ('INNERGRID', (5, 0), (5, 1), 0.25, colors.black),
        # ('BOX', (1, 0), (1, 1), 0.25, colors.black),
        # ('BOX', (3, 0), (3, 1), 0.25, colors.black),
        ('BOX', (5, 0), (5, 1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)

    # End invoice total

    story.append(Spacer(0, 4 * cm))

    # Legal statement
    story.append(Table([[Paragraph('I DECLARE THE INFORMATION CONTAINED IN THIS '
                                   'INVOICE TO BE TRUE AND CORRECT', styles["Line_Label"])]]))

    story.append(Spacer(0, 1 * cm))
    # End legal statement

    # Signature block
    data1 = [
        [Paragraph(busInfo.owner, styles["Line_Data_Large"]), '',
         Paragraph(invoice.date_billed.strftime(
             "%m/%d/%Y"), styles["Line_Data_Large"])
         ],
        [Paragraph('SIGNATURE OF BILLER (Type name and title and sign.)', styles["Line_Label"]), '',
         Paragraph('DATE', styles["Line_Label"])]]

    t1 = Table(data1, colWidths=(None, 2 * cm, None))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (0, 1), 0.25, colors.black),
        ('INNERGRID', (2, 0), (2, 1), 0.25, colors.black),
    ]))

    story.append(t1)

    # End signature block

    doc.build(story)

    return doc
