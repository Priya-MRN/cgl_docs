# -*- coding: utf-8 -*-
"""
Important World / International / National Days (January - December).
Generates a printable A4 PDF for static GK revision
(SSC CGL, Banking, Railways, TNPSC, UPSC).
"""
import os
from fpdf import FPDF

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aptitude-Tables")
os.makedirs(OUT_DIR, exist_ok=True)

# (date, name)  -- "*" prefix on date kept clean; multi-day shown as range
DAYS = {
    "JANUARY": [
        ("Jan 1", "Global Family Day / New Year"),
        ("Jan 4", "World Braille Day"),
        ("Jan 6", "World Day of War Orphans"),
        ("Jan 9", "Pravasi Bharatiya Divas (NRI Day)"),
        ("Jan 10", "World Hindi Day"),
        ("Jan 11", "National Human Trafficking Awareness Day"),
        ("Jan 12", "National Youth Day (Swami Vivekananda's Birthday)"),
        ("Jan 15", "Indian Army Day"),
        ("Jan 23", "Parakram Diwas (Netaji Subhas Chandra Bose)"),
        ("Jan 24", "National Girl Child Day"),
        ("Jan 25", "National Voters' Day / National Tourism Day"),
        ("Jan 26", "Republic Day / International Customs Day"),
        ("Jan 27", "Intl. Day of Commemoration - Holocaust Victims"),
        ("Jan 28", "Data Protection Day"),
        ("Jan 30", "Martyrs' Day (Mahatma Gandhi) / Anti-Leprosy Day"),
    ],
    "FEBRUARY": [
        ("Feb 2", "World Wetlands Day"),
        ("Feb 4", "World Cancer Day"),
        ("Feb 6", "Intl. Day of Zero Tolerance to FGM"),
        ("Feb 10", "National Deworming Day"),
        ("Feb 11", "Intl. Day of Women and Girls in Science"),
        ("Feb 12", "National Productivity Day / Darwin Day"),
        ("Feb 13", "World Radio Day / National Women's Day (Sarojini Naidu)"),
        ("Feb 14", "Valentine's Day"),
        ("Feb 20", "World Day of Social Justice"),
        ("Feb 21", "International Mother Language Day"),
        ("Feb 22", "World Thinking Day / World Scout Day"),
        ("Feb 24", "Central Excise Day"),
        ("Feb 27", "World NGO Day"),
        ("Feb 28", "National Science Day (Raman Effect)"),
    ],
    "MARCH": [
        ("Mar 1", "World Civil Defence Day / Zero Discrimination Day"),
        ("Mar 3", "World Wildlife Day / World Hearing Day"),
        ("Mar 4", "National Safety Day"),
        ("Mar 8", "International Women's Day"),
        ("Mar 10", "CISF Raising Day"),
        ("Mar 14", "Pi Day / Intl. Day of Action for Rivers"),
        ("Mar 15", "World Consumer Rights Day"),
        ("Mar 18", "Ordnance Factories Day"),
        ("Mar 20", "World Sparrow Day / Intl. Day of Happiness"),
        ("Mar 21", "World Forestry Day / World Down Syndrome Day"),
        ("Mar 22", "World Water Day"),
        ("Mar 23", "World Meteorological Day / Shaheed Diwas (Bhagat Singh)"),
        ("Mar 24", "World TB Day"),
        ("Mar 27", "World Theatre Day"),
    ],
    "APRIL": [
        ("Apr 1", "Odisha Foundation Day / April Fools' Day"),
        ("Apr 2", "World Autism Awareness Day"),
        ("Apr 4", "Intl. Day for Mine Awareness"),
        ("Apr 5", "National Maritime Day"),
        ("Apr 7", "World Health Day"),
        ("Apr 10", "World Homeopathy Day"),
        ("Apr 11", "National Safe Motherhood Day"),
        ("Apr 13", "Jallianwala Bagh Massacre Day"),
        ("Apr 14", "Ambedkar Jayanti / World Quantum Day"),
        ("Apr 17", "World Hemophilia Day"),
        ("Apr 18", "World Heritage Day"),
        ("Apr 21", "National Civil Services Day"),
        ("Apr 22", "World Earth Day"),
        ("Apr 23", "World Book and Copyright Day"),
        ("Apr 24", "National Panchayati Raj Day"),
        ("Apr 25", "World Malaria Day"),
        ("Apr 26", "World Intellectual Property Day"),
    ],
    "MAY": [
        ("May 1", "International Labour Day / Maharashtra & Gujarat Day"),
        ("May 3", "World Press Freedom Day"),
        ("May 8", "World Red Cross Day / World Thalassaemia Day"),
        ("May 11", "National Technology Day"),
        ("May 12", "International Nurses Day"),
        ("May 15", "International Day of Families"),
        ("May 17", "World Telecommunication Day"),
        ("May 18", "International Museum Day"),
        ("May 21", "Anti-Terrorism Day / World Day for Cultural Diversity"),
        ("May 22", "International Day for Biological Diversity"),
        ("May 24", "Commonwealth Day"),
        ("May 31", "World No Tobacco Day"),
    ],
    "JUNE": [
        ("Jun 1", "World Milk Day / Global Day of Parents"),
        ("Jun 3", "World Bicycle Day"),
        ("Jun 5", "World Environment Day"),
        ("Jun 7", "World Food Safety Day"),
        ("Jun 8", "World Oceans Day / World Brain Tumour Day"),
        ("Jun 9", "World Accreditation Day"),
        ("Jun 12", "World Day Against Child Labour"),
        ("Jun 14", "World Blood Donor Day"),
        ("Jun 15", "World Elder Abuse Awareness Day"),
        ("Jun 20", "World Refugee Day"),
        ("Jun 21", "International Yoga Day / World Music Day"),
        ("Jun 23", "International Olympic Day / UN Public Service Day"),
        ("Jun 26", "Intl. Day Against Drug Abuse & Illicit Trafficking"),
        ("Jun 29", "National Statistics Day"),
    ],
    "JULY": [
        ("Jul 1", "National Doctors' Day / GST Day / CA Day"),
        ("Jul 6", "World Zoonoses Day"),
        ("Jul 11", "World Population Day"),
        ("Jul 12", "World Malala Day / Paper Bag Day"),
        ("Jul 17", "World Day for International Justice"),
        ("Jul 18", "Nelson Mandela International Day"),
        ("Jul 22", "Pi Approximation Day / National Flag Adoption Day"),
        ("Jul 26", "Kargil Vijay Diwas"),
        ("Jul 28", "World Hepatitis Day / World Nature Conservation Day"),
        ("Jul 29", "International Tiger Day"),
    ],
    "AUGUST": [
        ("Aug 1", "World Breastfeeding Week begins (Aug 1-7)"),
        ("Aug 6", "Hiroshima Day"),
        ("Aug 9", "Quit India Day / Nagasaki Day / Indigenous People Day"),
        ("Aug 12", "International Youth Day"),
        ("Aug 13", "World Organ Donation Day / Left Handers' Day"),
        ("Aug 15", "Independence Day (India)"),
        ("Aug 19", "World Photography Day / World Humanitarian Day"),
        ("Aug 20", "Sadbhavana Diwas / World Mosquito Day"),
        ("Aug 23", "Intl. Day for Remembrance of Slave Trade"),
        ("Aug 29", "National Sports Day (Major Dhyan Chand)"),
    ],
    "SEPTEMBER": [
        ("Sep 5", "Teachers' Day (India) / Intl. Day of Charity"),
        ("Sep 8", "World Literacy Day"),
        ("Sep 14", "Hindi Diwas"),
        ("Sep 15", "Engineers' Day (India) / Intl. Day of Democracy"),
        ("Sep 16", "World Ozone Day"),
        ("Sep 21", "International Day of Peace / World Alzheimer's Day"),
        ("Sep 22", "Rose Day (Welfare of Cancer Patients)"),
        ("Sep 25", "Antyodaya Diwas / World Pharmacist Day"),
        ("Sep 26", "World Contraception Day"),
        ("Sep 27", "World Tourism Day"),
        ("Sep 29", "World Heart Day"),
    ],
    "OCTOBER": [
        ("Oct 1", "International Day of Older Persons"),
        ("Oct 2", "Gandhi Jayanti / International Day of Non-Violence"),
        ("Oct 4", "World Animal Welfare Day"),
        ("Oct 5", "World Teachers' Day"),
        ("Oct 8", "Indian Air Force Day"),
        ("Oct 9", "World Post Office Day"),
        ("Oct 10", "World Mental Health Day"),
        ("Oct 11", "International Day of the Girl Child"),
        ("Oct 13", "Intl. Day for Disaster Risk Reduction"),
        ("Oct 16", "World Food Day"),
        ("Oct 24", "United Nations Day / World Development Information Day"),
        ("Oct 31", "National Unity Day (Sardar Patel) / World Cities Day"),
    ],
    "NOVEMBER": [
        ("Nov 1", "Haryana / Karnataka / Kerala Foundation Day"),
        ("Nov 5", "World Tsunami Awareness Day"),
        ("Nov 7", "National Cancer Awareness Day / Infant Protection Day"),
        ("Nov 9", "Legal Services Day / Uttarakhand Foundation Day"),
        ("Nov 11", "National Education Day (Maulana Azad)"),
        ("Nov 14", "Children's Day (India) / World Diabetes Day"),
        ("Nov 16", "International Day for Tolerance / National Press Day"),
        ("Nov 17", "National Epilepsy Day"),
        ("Nov 19", "World Toilet Day / National Integration Day"),
        ("Nov 20", "Universal Children's Day"),
        ("Nov 21", "World Television Day / World Fisheries Day"),
        ("Nov 26", "Constitution Day / National Law Day"),
        ("Nov 29", "Intl. Day of Solidarity with Palestinian People"),
    ],
    "DECEMBER": [
        ("Dec 1", "World AIDS Day"),
        ("Dec 2", "National Pollution Control Day / Abolition of Slavery Day"),
        ("Dec 3", "International Day of Persons with Disabilities"),
        ("Dec 4", "Indian Navy Day"),
        ("Dec 5", "World Soil Day / Intl. Volunteer Day"),
        ("Dec 7", "Armed Forces Flag Day / Intl. Civil Aviation Day"),
        ("Dec 10", "Human Rights Day"),
        ("Dec 11", "International Mountain Day / UNICEF Day"),
        ("Dec 14", "National Energy Conservation Day"),
        ("Dec 16", "Vijay Diwas"),
        ("Dec 18", "International Migrants Day / Minorities Rights Day"),
        ("Dec 20", "International Human Solidarity Day"),
        ("Dec 22", "National Mathematics Day (Ramanujan)"),
        ("Dec 23", "National Farmers' Day (Kisan Diwas)"),
        ("Dec 24", "National Consumer Rights Day"),
        ("Dec 25", "Good Governance Day / Christmas"),
    ],
}

HDR = (31, 78, 120)
ALT = (223, 233, 245)
MONTH_BG = (31, 78, 120)


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*HDR)
        self.cell(0, 8, "IMPORTANT DAYS OF THE YEAR (January - December)",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 5, "Static GK Revision  -  SSC CGL | Banking | Railways | TNPSC | UPSC",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, f"Page {self.page_no()}  |  National & International Days",
                  align="C")


def build_pdf(path):
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    # Two columns of months on the page
    page_w = 210
    margin = 10
    gutter = 8
    col_w = (page_w - 2 * margin - gutter) / 2     # ~92 mm
    date_w = 20
    name_w = col_w - date_w
    col_x = [margin, margin + col_w + gutter]
    top_y = 26
    bottom_limit = 285
    line_h = 4.4
    month_gap = 2.5

    col = 0
    y = top_y

    def draw_month(x, y, month, items):
        # month banner
        pdf.set_xy(x, y)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(*MONTH_BG)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_w, 6, "  " + month, border=0, fill=True,
                 new_x="LMARGIN", new_y="NEXT", align="L")
        yy = y + 6
        for i, (d, n) in enumerate(items):
            if i % 2 == 1:
                pdf.set_fill_color(*ALT)
                fill = True
            else:
                fill = False
            pdf.set_text_color(*HDR)
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_xy(x, yy)
            pdf.cell(date_w, line_h, d, border=0, fill=fill, align="L")
            pdf.set_text_color(20, 20, 20)
            pdf.set_font("Helvetica", "", 7.3)
            pdf.set_xy(x + date_w, yy)
            # truncate gracefully if too long
            txt = n
            while pdf.get_string_width(txt) > name_w - 2 and len(txt) > 4:
                txt = txt[:-2]
            if txt != n:
                txt = txt.rstrip() + "."
            pdf.cell(name_w, line_h, txt, border=0, fill=fill, align="L")
            yy += line_h
        return yy

    for month, items in DAYS.items():
        block_h = 6 + len(items) * line_h + month_gap
        x = col_x[col]
        if y + block_h > bottom_limit:
            if col == 0:
                col = 1
                y = top_y
                x = col_x[col]
            else:
                pdf.add_page()
                col = 0
                y = top_y
                x = col_x[col]
        y = draw_month(x, y, month, items) + month_gap

    pdf.output(path)
    return path


if __name__ == "__main__":
    out = build_pdf(os.path.join(OUT_DIR, "World_Important_Days_Jan_Dec.pdf"))
    total = sum(len(v) for v in DAYS.values())
    print("PDF saved:", out)
    print("Total days listed:", total)
