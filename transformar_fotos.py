import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

def compress_image(image, max_size=(350,350)):
    image = image.copy()
    image.thumbnail(max_size) # Ajusta la resolución al tamaño deseado
    return image

def add_watermark_to_image(image, watermark_text, font):
    """Agrega una marca de agua al centro de la imagen."""
    # Crear objeto de dibujo
    draw = ImageDraw.Draw(image)
    # Calcular posición para centrar la marca de agua
    text_width, text_height = font.getbbox(watermark_text)[2:]
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2
    # Dibujar la marca de agua
    draw.text((x, y), watermark_text, fill="gray", font=font)
    return image

def create_collage_with_watermark(images, cell_size=(350, 350), watermark_text='Shot by Leomar'):
    """Crea un collage con las imágenes dadas y una marca de agua."""
    # Calcular las dimensiones del collage
    cols = int(len(images)**0.5) or 1
    rows = (len(images) + cols - 1) // cols
    collage_width = cols * cell_size[0]
    collage_height = rows * cell_size[1]

    # Crear el lienzo del collage
    collage = Image.new("RGB", (collage_width, collage_height), color="white")

    # Fuente para números y marca de agua
    try:
        font_size = 25  # Cambia este valor al tamaño de fuente deseado
        font = ImageFont.truetype('arial.ttf', font_size)
    except:
        font = ImageFont.load_default()
        st.warning("No se encontró la fuente 'arial.ttf'. Usando fuente predeterminada, el tamaño no puede cambiar.")

    # Añadir imágenes al collage
    index = 0
    for row in range(rows):
        for col in range(cols):
            if index >= len(images):
                break
            # Redimensionar las imágenes
            img = images[index].resize(cell_size)
            # Agregar la marca de agua al centro de la imagen
            img = add_watermark_to_image(img, watermark_text, font)
            x = col * cell_size[0]
            y = row * cell_size[1]
            # Pegar la imagen
            collage.paste(img, (x, y))
            # Dibujar el número
            draw = ImageDraw.Draw(collage)
            draw.text((x + 10, y + 10), f"#{index + 1}", fill="black", font=font)
            index += 1

    # Retornar el collage final
    return collage

# Streamlit App
st.title("Gestor de Imágenes y Collage")

# Subida de imágenes
uploaded_files = st.file_uploader(
    "Sube tus imágenes aquí",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Has subido {len(uploaded_files)} imágenes.")
    images = []
    for file in uploaded_files:
        # Cargar imagen con PIL
        original_image = Image.open(file)
        compressed_image = compress_image(original_image)  # Comprimir imagen
        images.append(compressed_image)

    # Vista previa de imágenes comprimidas
    st.write("Vista previa de las imágenes comprimidas:")
    for idx, img in enumerate(images, start=1):
        st.image(img, caption=f"Imagen {idx} (baja calidad)", use_container_width=True)

    # Crear y mostrar el collage
    st.write("Generando collage...")
    collage = create_collage_with_watermark(images, watermark_text="Shot by Leomar")
    st.image(collage, caption="Collage Final", use_container_width=True)

    # Botón para descargar el collage
    buf = io.BytesIO()
    collage.save(buf, format="JPEG")
    st.download_button(
        label="Descargar Collage",
        data=buf.getvalue(),
        file_name="collage_final.jpg",
        mime="image/jpeg"
    )