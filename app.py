# GEREKLI MODULLER
import numpy as np
import streamlit as st
import cv2
import io
from PIL import Image

# SAYFA YAPILANDIRILMASI
st.set_page_config(
    page_title="Görüntüyü gri formata dönüştürme",
    page_icon="🌄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_image(image_file):
    """yüklenen görüntüyü okur ve döndürür"""
    img = Image.open(image_file)
    return img

def convert_to_grayscale(img):
    """görüntüyü griye dönüştürür"""
    img_array = np.array(img)
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        gray_image = img.convert("L")
        return gray_image
    else:
        return img

def apply_filter(img, filter_type, intensity=1.0):
    img_array = np.array(img)
    
    if filter_type == "Bulanıklaştırma":
        kernel_size = int(intensity * 5)
        if kernel_size % 2 == 0:
            kernel_size += 1
        # Hem renkli hem gri resim için aynı işlem uygulanabilir
        filtered_img = cv2.GaussianBlur(img_array, (kernel_size, kernel_size), 0)
        
    elif filter_type == "Keskinleştirme":
        kernel = np.array([[-1, -1, -1],  
                           [-1,  9, -1],  
                           [-1, -1, -1]]) 
        filtered_img = cv2.filter2D(img_array, -1, kernel)
        
    elif filter_type == "Kenar algılama":
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)      
        else:
            gray = img_array
            
        threshold1 = 50 * intensity
        threshold2 = 150 * intensity
        edges = cv2.Canny(gray, int(threshold1), int(threshold2))
        filtered_img = edges
    elif filter_type=="Negatif":
        filtered_img=255-img_array
    else:
        filtered_img=img_array
    filtered_img=np.clip(filtered_img,0,255).astype(np.uint8)    

    if len(filtered_img.shape)==2:
        return Image.fromarray(filtered_img,mode="L")
    else:
        return Image.fromarray(filtered_img)
def add_custom_css():
    st.markdown("""
    <style>
                .main-header{
                font-size:2.5rem;
                color:#4527A0;
                text-align: center;
                margin-bottom:1rem;
               }
                .sub-header{
                font,size:1.5rem;
                color:#5E35B1;
                margin-top:1rem;
                margin-bottom:0.5rem
                }
                .info-text{
                font-size:1rem;
                color:#333;
                margin-bottom:1rem;
                }
                .stButton>button{
                background-color:#5E3581;
                color:white;
                font-weight:boild;
                border-radius:5rem;
                padding:0.5rem,1rem
                border:none;
                }
                .stButton>button:hover{
                background-color:#4527A0
                }
    </style>
                """,unsafe_allow_html=True)   
def sidebar_contect():
    st.sidebar.title("Hakkında")
    st.sidebar.info(
        "görüntü işleme streamlit konusunda bir web sayfası"
        
    )
    st.sidebar.title("Nasıl Kullanılır?")
    st.sidebar.markdown(
    """
    1. Sol taraftaki 'Bir görüntü yükleyin' butonuna tıklayın.
    2. Bilgisayarınızdan bir görüntü seçin (JPG, JPEG veya PNG).
    3. 'Gri formata dönüştür' butonuna tıklayın.
    4. İsterseniz ek filtreler uygulayabilirsiniz.
    5. Dönüştürülen görüntüyü indirmek için 'Görüntüyü indir' butonuna tıklayın.
    """
)
    st.sidebar.title("Görüntü İşleme Hakkında")
    st.sidebar.markdown(
    """
    **Gri Formata Dönüştürme Nedir?**  
    Renkli bir görüntüyü gri formata dönüştürmek,
    her pikselin renk bilgisini (RGB) tek bir gri
    ton değerine dönüştürme işlemidir.

    **Filtreler Hakkında**  
    - **Bulanıklaştırma**: Görüntüdeki gürültüyü azaltır ve detayları yumuşatır.  
    - **Keskinleştirme**: Görüntüdeki kenarları ve detayları vurgular.  
    - **Kenar Algılama**: Görüntüdeki nesnelerin kenarlarını tespit eder.  
    - **Negatif**: Görüntünün renklerini tersine çevirir.
    """
)
def main():
    add_custom_css()
    sidebar_contect()    
    st.markdown(
        "<h1 class='main-header'> Görüntü gri formata dönüştürücü </h1>",unsafe_allow_html=True
        
    )
    st.markdown(
        "<p class='info-text'>Bu uygulama yüklediğiniz görüntüyü gri formata dönüştürür ve çeşitli filtreler uygulamanıza olanak sağlar</p>",unsafe_allow_html=True
    )
col1,col2=st.columns(2) #sayfayı ikiye böler
#görüntü yükleme
with col1:
    uploaded_file=st.file_uploader("Bir görsel yükleyin",type=["jpg","jpeg","png"])
    if uploaded_file is not None:
        image=load_image(uploaded_file)
        with col1:
            st.markdown('<h2 class="sub-header">Orjinal Görüntü </h2>',unsafe_allow_html=True)
            st.image(image,caption="yüklenen görüntü",use_column_width=True)
            st.markdown('<h3 class="sub-header">Görüntü Bilgileri </h3>',unsafe_allow_html=True)
            img_array=np.array(image)
            st.write("Boyut : {}x{}".format(img_array.shape[1],img_array.shape[0]))
            if len(img_array.shape)==3:
                st.write("Kanal sayısı: {}".format(img_array.shape[2]))
                st.write("Renk Formatı: RGB")
            else:
                st.write("Kanal Sayısı:1")
                st.write("Renk Formatı:Gri Tonlama")    
            #işlem seçenekleri
            process_option = st.radio(
                "İşlem türünü seçin:",
                ["Sadece Gri Formata Dönüştür",
                 "Gri Formata Dönüştür ve Filtre Uygula",
                 "Sadece Filtre Uygula"]
            )

            if "Filtre" in process_option:
                filter_type = st.selectbox(
                    "Filtre türünü seçin:",
                    ["Bulanıklaştırma", "Keskinleştirme", "Kenar algılama", "Negatif"]
                )

                intensity = st.slider(
                    "Filtre Yoğunluğu",
                    min_value=0.1,
                    max_value=2.0,
                    value=1.0,
                    step=0.1
                )

            process_button = st.button("İşlemi Başlat")
            if process_button:
                try:
                    if process_option == "Sadece Gri Formata Dönüştür":
                         st.info("Görüntü gri formata dönüştürülüyor...")
                         processed_image = convert_to_grayscale(image)
                         result_caption = "Gri Formatlı Görüntü"
                    elif process_option == "Gri Formata Dönüştür ve Filtre Uygula":
                        st.info("Görüntü gri formata dönüştürülüyor ve filtre uygulanıyor...")
                        gray_image = convert_to_grayscale(image)
                        processed_image = apply_filter(gray_image, filter_type, intensity)
                        result_caption = "Gri Formatlı ve {} Filtresi Uygulanmış Görüntü".format(filter_type) 
                    else:
                        st.info("{} filtresi uygulanıyor...".format(filter_type))
                        processed_image = apply_filter(image, filter_type, intensity)
                        result_caption = "{} Filtresi Uygulanmış Görüntü".format(filter_type)     
                    with col2:
                        st.markdown("<h2 class='sub-header'>işlenmiş görüntü</h2>",unsafe_allow_html=True)
                        st.image(processed_image,caption=result_caption,use_column_width=True)
                        #indirme seçeneği
                        buf=io.BytesIO()
                        processed_image.save(buf,format="PNG")
                        byte_im=buf.getvalue()
                        st.download_button(label="görüntüyü indir",
                                           data="byte_im",
                                           file_name="processed_image.png",
                                           mime="image/png")
                except Exception as e:
                    st.error("bir hata oluştu:{}".format(e))
                    st.error("Lütfen Farklı Bir Görüntü veye Dosya Seçin")
    else:
        st.info("Lütfen bir görüntü ekleyin desteklenen formatlar JPG,JPEG VE PNG")
if __name__=="main":
    main()

                
                      
        