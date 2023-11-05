import dash
from dash import dcc
from dash import  html
from dash.dependencies import Input, Output, State
from fpdf import FPDF
from PIL import Image

app = dash.Dash(__name__)    

zahl=2

class Rechz:
    def __init__(self,name,anz,preis):
        self.besch=name
        self.anzahl=int(anz)
        self.ppe=float(preis)
        self.gesamtpreis = int(anz)*float(preis)


def cdiv(z):
    divs = []
    
    n=html.H5(f"{z}. Leistung:")
    new_div = html.Div([
            html.Label(f"Leistungsbeschreibung {z}:"),
            dcc.Input(id=f"lebe{z}", type="text", value=''),
        ], style={'margin-bottom': '.5cm'})
    
    nd= html.Div([
            html.Label(f"Anzahl {z}:"),
            dcc.Input(id=f"lean{z}", type="number", value=0),
        ], style={'margin-bottom': '.5cm'})
        
    nnd= html.Div([
            html.Label(f"Einzelpreis der Leistung {z}:"),
            dcc.Input(id=f"leei{z}", type="number", value=0.0, step='0.01'),
        ], style={'margin-bottom': '.5cm'})
    
    divs.append(n)
    divs.append(new_div)
    divs.append(nd)
    divs.append(nnd)
       
    return divs
        

app.layout = html.Div([
    html.Div([
    html.Img(src='Stads_Logo.png', alt='Stads Logo', style={'width': '300px', 'height': 'auto', 'float': 'right'}),
    ], style={'margin-bottom': '.5cm'}),
    
    html.H1("Rechnungsersteller Formular"),
    html.Div([
        html.Div([
            html.H3("1. Adressat eintragen"),
            html.Div([
                html.Label("Firmenname:"),
                dcc.Input(id="firmenname", type="text", placeholder="Muster 2 Gmbh"),
            ], style={'margin-bottom': '.5cm'}),
            html.Div([
                html.Label("zuständige Person:"),
                dcc.Input(id="zustaendige_person", type="text", placeholder="-"),
            ], style={'margin-bottom': '.5cm'}),
            html.Div([
                html.Label("Geschäftsbereich:"),
                dcc.Input(id="geschaeftsbereich", type="text", placeholder=""),
            ], style={'margin-bottom': '.5cm'}),
            html.Div([
                html.Label("Straße + Hausnummer:"),
                dcc.Input(id="strasse", type="text", placeholder="Teststraße 0"),
            ], style={'margin-bottom': '.5cm'}),
            html.Div([
                html.Label("PLZ, Ort:"),
                dcc.Input(id="plz_ort", type="text", placeholder="70178 Stuttgart"),
            ]),
        ]),
        html.Div([
            html.H3("2. Datum/ Rechnungsnummer"),
            html.Div([
                html.Label("Datum:"),
                dcc.Input(id="datum", type="text"),
            ], style={'margin-bottom': '.5cm'}),
            html.Div([
                html.Label("Rechnung Nr.:"),
                dcc.Input(id="rechnung_nr", type="text"),
            ], style={'margin-bottom': '.5cm'}),
            html.Div([
                html.Label("Name für Rechungsdatei:"),
                dcc.Input(id="datei", type="text"),
            ], style={'margin-bottom': '.5cm'}),
        ]),
        html.Div([
            html.H3("3. Rechnungstext"),

            html.Div([
                html.Label("Ansprechpartner:"),
                dcc.Input(id="ansprechpartner", type="text", placeholder="Luca Maroon"),
            ], style={'margin-bottom': '.5cm'}),
            
            html.Div([    
                html.Label("Funktion:"),
                dcc.Input(id="funktion", type="text", placeholder="Vorstand"),
            ], style={'margin-bottom': '.5cm'}),
        
            html.Div([
                html.Label("(Mobil)Stads:"),
                dcc.Input(id="mobil_stads", type="text", placeholder="+49 160 8479261"),
            ], style={'margin-bottom': '.5cm'}),
        
            html.Div([
                html.Label("E-Mail:"),
                dcc.Input(id="email", type="text", placeholder="luca.maroon@stads.de"),
            ], style={'margin-bottom': '.5cm'}),
        ]),
    ],style={'width':'50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    
    html.Div([
        html.H3("4. Rechnungszeilen"),        
        
        html.Div(id="div-container", children=cdiv(1)),
        
        
    ],style={'width':'50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    
    html.Div(id='output-div'),
    html.Button("Create PDF", id="create_pdf"),
    html.Button("Neue Rechnungszeile hinzufügen", id="add-div-button"),
    html.Button("Lösche Reschnungszeile", id="delete_r"),
], style={'background-color': '#203864','color':'white'})




@app.callback(
    Output("div-container", "children"),
    Input("add-div-button", "n_clicks"),
    Input("delete_r", "n_clicks"),
    State("div-container", "children")
)

def add_div(n1, n2, children):    
    ctx = dash.callback_context
    if not ctx.triggered:
        return children
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'add-div-button':
        global zahl
        children.extend(cdiv(zahl))
        zahl+=1
        return children
    elif triggered_id == 'delete_r':
        if children:
            children.pop()
            children.pop()
            children.pop()
            children.pop()
            zahl-=1
        return children
    else:
        return children



def safeAsPDF(fname, zPerson, gbe, strase, plz, datum, rechnungsNr,  ansprechpartner, funktion, mobilNr, email,da , liste_rechz):
    class PDF(FPDF):
        def header(self):
            bild_datei = 'Stads_Logo.png'
            bild=Image.open(bild_datei)
            breite_I, hoehe_I = bild.size
            self.image(bild_datei, y=10, x=self.w-(breite_I/8), w=breite_I/10, h=hoehe_I/10)
            self.set_text_color(0,0,0)
            
        def footer(self):
            self.set_y(-30)
            self.set_font('Helvetica', style='',size= 10)
            ww=self.w-20
            self.multi_cell(text="""Students' Association for Data Analytics and Statistics (STADS) Mannheim e.V""",w=ww/3,h=6,align='L')
            self.set_xy(-self.w/3,-30)
            self.multi_cell(text="""Der Verein ist eingetragen im Vereinsregister Mannheim unter der Nummer VR701996""",w=ww/3,h=6,align='L')
            
            
        def block3(self, v1, v2, v3):
            self.cell(text=str(v1),w=p.w/2,h=6,align='L')
            self.cell(text=str(v2),w=p.w/4-10,h=6,align='L')
            self.cell(text=str(v3),w=p.w/4,h=6,align='L')
            p.ln()
        
        def block2(self, v1, v2, v3):
            self.cell(text=str(v1),w=30,h=6,align='L')
            self.cell(text=str(v2),w=p.w/4,h=6,align='L')
            self.cell(text=str(v3),w=p.w,h=6,align='L')
            self.ln()
        
            
        
    p = PDF()
    p.set_auto_page_break(auto=1,margin=15)
    
    
    p.add_page()
    
    p.set_font('Helvetica', style='U',size= 10)
    p.ln(10)
    p.cell(w=50, h=10, text='STADS e.V. -Schloss- 68131 Mannheim',align='L')
    p.ln()
    
    
    p.set_font('Helvetica', '', 10)
    
    p.block3(fname,'Ansprechpartner',ansprechpartner)
    p.block3(zPerson,'Funktion',funktion)
    p.block3(gbe,'Mobil',mobilNr)
    p.block3(strase,'Email',email)
    p.block3(plz,'Internet','stads.uni-mannheim.de')
    p.block3('','Datum',datum)
    
    
    p.set_font('Helvetica', style='B', size=10)
    p.cell(text=f'Rechnungs Nr.  {rechnungsNr}' ,w=p.w,h=10,align='L')
    p.ln(10)
    
    p.set_font('Helvetica', '', 10)
    p.cell(text='Sehr geehrte Damen und Herren,',w=p.w,h=15,align='L')
    p.ln(15)
    p.cell(text='im Rahmen unserer Partnerschaft erlauben wir uns ihnen folgende Leistungen in Rechnung zu stellen:',w=p.w,h=10,align='L')
    p.ln(10)
    
    
    xn=p.x
    yn=p.y
    p.set_text_color(255,255,255)
    p.set_fill_color(32,40,100) 
    p.rect(x=xn,y=yn,w=p.w-20,h=8,style='F')
    p.set_xy(x=xn,y=yn)
    p.cell(text='Beschreibung',w=p.w/2,h=8,align='L')
    p.cell(text='Anzahl',w=p.w/8,h=8,align='L')
    p.cell(text='Einzelpreis',w=p.w/8,h=8,align='L')
    p.cell(text='Gesamtpreis',w=p.w/4,h=8,align='L')
    p.ln(8)
    
    p.set_text_color(0,0,0)
    xn=p.x
    yn=p.y
    p.set_fill_color(0,0,0)
    
    p.cell(text='',w=30,h=3,align='L')
    p.ln()
    
    ho=3
    preis=0.0
    
    for r in liste_rechz:
        if r.besch is None or r.besch=='':
            r.besch='-'
        if r.anzahl is None:
            r.anzahl='-'
        if r.ppe is None:
            r.ppe='-'
        if r.gesamtpreis is None:
            r.gesamtpreis='-'
        
        y0=p.y
        p.multi_cell(txt=str(r.besch),w=p.w/2-15,h=6,align='L')
        yne=p.y
        p.set_xy(p.w/2+15,y0)
        p.cell(txt=str(r.anzahl),w=p.w/8,h=6,align='L')
        p.cell(txt=f"{r.ppe:.2f}",w=p.w/8,h=6,align='L')
        p.cell(txt=f"{float(r.gesamtpreis):.2f}",w=p.w/4,h=6,align='L')
        p.ln(5)
        p.set_xy(xn,yne)
        y1=p.y
        ho+=(y1-y0)
        preis=float(preis)+float(r.gesamtpreis)
    
    p.rect(x=xn,y=yn,w=p.w-20,h=ho)
    p.rect(x=p.x,y=p.y,w=p.w-20,h=8)
    
    p.cell(txt='Gesamtbetrag',w=p.w/2+p.w/4,h=8,align='L')
    p.cell(txt=str(f"{preis:.2f}"),w=p.w/4,h=8,align='L')
    p.ln()
    
    p.set_y(p.y+10)
    
    p.set_font('Helvetica', style='',size= 12)
    
    p.multi_cell(txt="""Als Kleinunternehmen im Sinn von § 19 Abs.1 UStG(Steuernummer: 38146/07519) wird keine Umsatzsteuer berechnet. Der Gesamtbetrag ist ab Erhalt dieser Rechnung innerhalb von 30 Tagen ohne Abzug auf folgendes Konto zu zahlen:""",w=p.w-20,h=6,align='L')
    p.ln(5)
    
    p.set_font('Helvetica', style='B',size= 12)
    
    p.block2('','Kontoinhaber','STADS Mannheim e.V.')
    p.block2('','Bankinstitut','Sparkasse Rhein-Neckar-Nord')
    p.block2('','IBAN','DE39 6705 0505 0039 8011 16')
    p.block2('','BIC','MANSDE66XXX')

    p.ln(10)
    
    p.set_font('Helvetica', style='',size=12)
    p.cell(txt='Mit freundlichen Grüßen',w=40,h=8,align='L')
    p.ln()
    p.cell(txt='Simon Schumacher, Elise Wolf und Luca Marohn',w=p.w/2,h=8,align='L')
    p.cell(txt='_______________________',w=30,h=8,align='L')
    p.ln()
    p.set_font('Helvetica', style='',size=8)
    p.cell(txt='Vertretungsberechtigter Vorstand',w=p.w/2,h=8,align='L')
    p.cell(txt='Autorisiert',w=30,h=8,align='L')
    p.ln()
    
    
    p.output(da+'.pdf')

l_rech = []


def set_l_rech(leb, lea,lee):
    global l_rech
    for i in range(0,len(leb)):
        l_rech.append(Rechz(leb[i],lea[i],lee[i]))





@app.callback(
    Output("output-div", "children"),
    [Input("create_pdf", "n_clicks"),Input("div-container", "children")],
    [State('firmenname', 'value'), State('zustaendige_person', 'value'), State('geschaeftsbereich', 'value'), State('strasse', 'value'), State('plz_ort', 'value'), State('datum', 'value'), State('rechnung_nr', 'value'),
     State('ansprechpartner', 'value'), State('funktion', 'value'), State('mobil_stads', 'value'), State('email', 'value'), State('datei','value')],
    
)

def update_output(n_clicks, children, value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8, value_9, value_10, value_11, value_12):
    if n_clicks is not None:
        if value_1 is None:
            value_1='-'
        if value_2 is None:
            value_2='-'
        if value_3 is None:
            value_3='-'
        if value_4 is None:
            value_4='-'
        if value_5 is None:
            value_5='-'
        if value_6 is None:
            value_6='-'
        if value_7 is None:
            value_7='-'
        if value_8 is None:
            value_8='-'
        if value_9 is None:
            value_9='-'
        if value_10 is None:
            value_10='-'
        if value_11 is None:
            value_11='-'
        if value_12 is None:
            value_12='-'
        
        leb = []
        lea = []
        lee = []        
            
        for item in children:
            if not isinstance(item, str):
                props = item.get('props',{})
                if not isinstance(props, str):
                    data=props.get('children',[])
                    for ch in data:
                        if not isinstance(ch, str):
                            if ch['type'] == 'Input':
                                value = ch['props']['value']
                                if ch['props']['id'].startswith('lebe'):
                                    leb.append(value)
                                elif ch['props']['id'].startswith('lean'):
                                    lea.append(value)
                                elif ch['props']['id'].startswith('leei'):
                                    lee.append(value)
                
        global l_rech  
        l_rech=[]      
               
        set_l_rech(leb, lea, lee)
        
        safeAsPDF(value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8, value_9, value_10, value_11, value_12, l_rech)

        return 'Gespeichert!'
    
    

if __name__ == "__main__":
    app.run_server(debug=True)

