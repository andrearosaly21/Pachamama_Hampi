import tkinter as tk
from tkinter import messagebox
import json
import os
from PIL import Image, ImageTk

class SoftwareHampiApp: #
  def __init__(self, root):
    self.root =root
    self.root.title("Pachamama Hampi")
    self.root.geometry("540x680")
    self.root.configure(bg="#F4F6F4")

    self.idioma = "es"
    self.enfermedad_actual =None #
    self.imagenes_cache = {} #

    self.ruta_base = os.path.dirname(os.path.abspath(__file__))
    self.db = self.cargar_datos(os.path.join(self.ruta_base, "datos.json"))

    self.ui_textos = {
      "es": {
        "titulo": "Recurso Medicinal", #
        "subtitulo": "Selecciona una enfermedad",
        "volver": "Volver a enfermedades",
        "científico": "Nombre científico:",
        "familia": "Familia botánica:",
        "parte": "Parte utilizada:",
        "uso": "Uso y preparación:",
        "alerta": "Precauciones:",
        "aviso_legal": "Aviso: Información educativa y cultural. No reemplaza la atención médica.",
      },
      "en": {
        "titulo": "Medicinal resource", #
        "subtitulo": "Select a condition",
        "volver": "Back to conditions",
        "científico": "Scientific name:",
        "familia": "Botanical family:",
        "parte": "Part used:",
        "uso": "Use and preparation:",
        "alerta": "Precautions:",
        "aviso_legal": "Educational and cultural information. Does not replace medical care.",
      },
      "qu": {
        "titulo": "Hampi waqaychay", #
        "subtitulo": "Huk unquyta akllay",
        "volver": "Unquykunaman kutiy",
        "científico": "Yachay sutin:",
        "familia": "Qura ayllun:",
        "parte": "Apaykachana rakin:",
        "uso": "Imayna apaykachana:",
        "alerta": "Paqtataq:",
        "aviso_legal": "Manan hampiqpa rantinpichu.",
      },
      "shp": { #
        "titulo": "Rao onanti",
        "subtitulo": "Isin katowe rao oinnoxon",
        "volver": "Kawe",
        "científico": "Onanti jane:",
        "familia": "Rao kaibo:",
        "parte": "Akinati tsekati:",
        "uso": "Jawekeska akin akati:",
        "alerta": "Oinbires akawe:",
        "aviso_legal": "Onanti joi riki. Doctor rao yamai.",
      },
    }

    self.barra_superior = tk.Frame(self.root, bg="#1B4332", pady=10)
    self.barra_superior.pack(fill="x")
    self.actualizar_barra_idiomas()

    self.contenedor = tk.Frame(self.root, bg="#F4F6F4")
    self.contenedor.pack(fill="both", expand=True, padx=20, pady=10)

    self.lbl_aviso = tk.Label(
      self.root,
      text=self.ui_textos[self.idioma]["aviso_legal"],
      font=("Arial", 8, "italic"),
      bg="#E8ECE8",
      fg="#4A5568",
      pady=6,
      wraplength=500,
    )
    self.lbl_aviso.pack(fill="x", side="bottom")

    self.mostrar_lista_enfermedades()

  def cargar_datos(self, ruta):
    if not os.path.exists(ruta):
      messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}")
      return {"enfermedades o dolencias": []}
    with open(ruta, "r", encoding="utf-8") as f:
      return json.load(f)

  def actualizar_barra_idiomas(self):
    for widget in self.barra_superior.winfo_children():
      widget.destroy()
    
    idiomas = [
      ("es", "Español"),
      ("en", "English"),
      ("qu", "Runasimi"),
      ("shp", "Shipibo-Konibo"),
    ]
    for cod, nombre in idiomas:
      activo = self.idioma == cod
      tk.Button(
        self.barra_superior,
        text=nombre,
        font=("Arial", 10, "bold"),
        bg="#D8F3DC" if activo else "#2D6A4F",
        fg="#1B4332" if activo else "white",
        relief= "flat",
        padx=10,
        pady=4,
        cursor="hand2",
        command=lambda c=cod: self.cambiar_idioma(c),
      ).pack(side="left", padx=8)

  def cambiar_idioma(self, nuevo_idioma):
    self.idioma = nuevo_idioma
    self.actualizar_barra_idiomas()
    self.lbl_aviso.config(text=self.ui_textos[self.idioma]["aviso_legal"])

    if self.enfermedad_actual:
      self.mostrar_detalle_enfermedads(self.enfermedad_actual)
    else:
      self.mostrar_lista_enfermedades()

  def limpiar_contenedor(self):
    for widget in self.contenedor.winfo_children():
      widget.destroy()

  def cargar_imagen_segura(self, ruta_relativa, tamaño=(180, 130)):
    ruta_completa = os.path.join(self.ruta_base, ruta_relativa)
    clave = f"{ruta_completa}_{tamaño[0]}*{tamaño[1]}"
    if clave in self.imagenes_cache:
      return self.imagenes_cache[clave]                                                             #        ****

    if os.path.exists(ruta_completa):
      img = Image.open(ruta_completa).resize(
      tamaño, Image.Resampling.LANCZOS
      )
      foto = ImageTk.PhotoImage(img)
      self.imagenes_cache[clave] = foto
      return foto
      return None

  def mostrar_lista_enfermedades(self):
    self.enfermedad_actual = None
    self.limpiar_contenedor()
    txt = self.ui_textos[self.idioma]

      tk.Label(
        self.contenedor,
        text=txt["titulo"],
        font=("Arial", 18, "bold"),
        bg="#F4F6F4",
        fg="#1B4332",
      ).pack(pady=(5, 2))

      tk.Label(
        self.contenedor,
        text=txt["subtitulo"],
        font=("Ariel", 10),
        bg="#F4F6F4",
        fg="#52796F",
      ).pack(pady=(0, 15))

    for enf in self.db["enfermedades o dolencias"]:
      tarjeta = tk.Frame(
        self.contenedor,
        bg="white",
        bd=1,
        relief="solid",
        padx=15,
        pady=12,
        cursor="hand2",
      )
      tarjeta.pack(fill="x", pady=6)

      lbl_nom = tk.Label(
        tarjeta,
        text=enf["nombres"][self.idioma],
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#1B4332",
        anchor="w",
      )
      lbl_nom.pack(fill="x")

      lbl_desc = tk.Label(
        tarjeta,
        text=enf["descripción"][self.idioma],
        font=("Arial", 10),
        bg="white",
        fg="#4A5568",
        anchor="w",
        wraplength=460,
        justify="left",
      )
      lbl_desc.pack(fill="x", pady=(4,0))

    for w in (tarjeta, lbl_nom, lbl_desc):
      w.bind(
        "<Button-1>",
        lambda e, item=enf: 
          self.mostrar_detalle_enfermedades(item),                                                    aqui
      )

    def mostrar_detalle_enfermedades(self, enfermedad):                                                        #
      self.enfermedad_actual = enfermedad
      self.limpiar_contenedor()
      txt = self.ui_textos[self.idioma]

    tk.Button(
      self.contenedor,
      text=txt["volver"],
      font=("Arial", 10, "bold"),
      bg="#D8F3DC",
      fg="#1B4332",
      relief="flat",
      padx=10,
      pady=4,
      cursor="hand2",
      command=self.mostrar_lista_enfermedades,
    ).pack(anchor="w", pady=(0, 10))

    tk.Label(
      self.contenedor,
      text=enfermedad["nombres"][self.idioma],
      font=("Arial",18, "bold"),
      bg="#F4F6F4",
      fg="#1B4332",
    ).pack(anchor="w")

    tk.Label(
      self.contenedor,
      text=enfermedad["descripción"][self.idioma],
      font=("Arial", 10),
      bg="#F4F6F4",
      fg="#4A5568",
      wraplength=480,
      justify="left",
    ).pack(anchor="w", pady=(2,12))

    canvas = tk.Canvas(
      self.contenedor, 
      bg="#F4F6F4", 
      highlightthickness=0,
    )
    scrollbar = tk.Scrollbar(
      self.contenedor, 
      orient="vertical", 
      command=canvas.yview,
    )
    scroll_frame = tk.Frame(
      canvas, 
      bg="#F4F6F4",
    )

    scroll_frame.bind(
      "<Configure>",
      lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
      ),
    )
    canvas.create_window(
      (0,0), 
      window=scroll_frame, 
      anchor="nw",
    )
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(
      side="left", 
      fill="both", 
      expand=True,
    )
    scrollbar.pack(side="right", fill="y")

    for trat in enfermedad["formas_de_tratamiento"]:
      card = tk.Frame(
        scroll_frame, 
        bg="white", 
        bd=1, 
        relief="solid", 
        padx=12, 
        pady=12
      )
      card.pack(fill="x", pady=8, padx=2)

      reg_nombre = trat["región"][self.idioma]
      planta_nombre = trat["planta"][self.idioma]
      
      tk.Label(
        card,
        text=f"{planta_nombre} - {reg_nombre}",
        font=("Arial", 13, "bold"),
        bg="white",
        fg="#2D6A4F",
      ).pack(anchor="w")                                                                                       ++++++++
      if "imagen" in trat and trat["imagen"]:
        foto = self.cargar_imagen_segura(
          trat["imagen"], 
          tamaño=(180, 130)
        )
      if foto:
        lbl_img = tk.Label(card, image=foto, bg="white")
        lbl_img.image = foto
        lbl_img.pack(anchor="w", pady=(8, 6))
      datos_ficha = [
        (txt["científico"], trat.get("nombre_científico", "")),
        (txt["familia"], trat.get("familia_botánica", "")),
        (txt["parte"], trat.get("parte_utilizada", {}).get(self.idioma, "")),
      ]

      for etiqueta, valor in datos_ficha:
        if valor:
        tk.Label(
          card,
          text=f"{etiqueta} {valor}",
          font=("Arial", 10),
          bg="white",
          fg="#2D3748",
          anchor="w",
          wraplength=440,
          justify="left",
        ).pack(anchor="w", pady=1)
      uso_texto = trat.get("uso", {}).get(self.idioma, "")
      if uso_texto:
        tk.Label(
          card,
          text=txt["uso"],
          font=("Arial", 10, "bold"),
          bg="white",
          fg="#1B4332",
          anchor="w",
        ).pack(anchor="w", pady=(8, 2))

        tk.Label(
          card,
          text=uso_texto,
          font=("Arial", 10),
          bg="white",
          fg="#4A5568",
          anchor="w",
          wraplength=440,
          justify="left",
        ).pack(anchor="w")
        
      aviso_texto = trat.get("advertencias", {}).get(self.idioma, "")
      if aviso_texto:
        tk.Label(
          card,
          text=txt["alerta"],
          font=("Arial", 10, "bold"),
          bg="white",
          fg="#9B2C2C",
          anchor="w",
        ).pack(anchor="w", pady=(8, 2))

        tk.Label(
          card,
          text=aviso_texto,
          font=("Arial", 10),
          bg="white",
          fg="#9B2C2C",
          anchor="w",
          wraplength=440,
          justify="left",
        ).pack(anchor="w")
