import streamlit as st
import pickle
import pandas as pd
st.set_page_config(layout="wide")

with open("model_rf_kti", "rb") as file:
    model = pickle.load(file)

# =============================
# GLOBAL STYLE (FINAL VERSION)
# =============================
st.markdown("""
<style>

/* Background full halaman - biru sangat muda */
[data-testid="stAppViewContainer"] {
    background-color: #f4f9ff;
}

/* Header wrapper */
.header-wrapper {
    margin-top: 3rem;
}

/* Highlight SmartBurn */
.brand-highlight {
    display: inline-block;
    background-color: #dbeeff;
    padding: 8px 22px;
    border-radius: 9px;
    font-size: 45px;
    font-weight: 700;
    color: #1565c0;
}

/* ===== RESULT CARD ===== */

.card {
    padding: 50px;
    border-radius: 15px;
    color: white;
    margin-top: 20px;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* Ukuran teks dalam card */
.card h2 {
    margin-bottom: 18px;
    font-size: 20px;
}

.card h1 {
    font-size: 36px;
    margin-bottom: 15px;
}

.card p {
    font-size: 18px;
}

/* Warna kategori */

.rendah {
    background: linear-gradient(135deg, #1f77b4, #4fa3f7);
}

.sedang {
    background: linear-gradient(135deg, #f4b400, #ffcc33);
}

.tinggi {
    background: linear-gradient(135deg, #e91e63, #ff4d88);
}

/* ========================= */
/* RADIO BUTTON CUSTOM SIZE  */
/* ========================= */

div[data-testid="stRadio"] label {
    font-size: 20px !important;
    font-weight: 500;
}

div[data-testid="stRadio"] input[type="radio"] {
    transform: scale(1.6);
    margin-right: 12px;
}

div[data-testid="stRadio"] > div {
    gap: 12px;
}
                     
</style>

<div class="header-wrapper">
    <span class="brand-highlight">SMARTBURN</span>
</div>
""", unsafe_allow_html=True)

# =============================
# INIT SESSION STATE
# =============================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

# =============================
# DATA PERTANYAAN
# =============================
questions = [
    "Saya merasa tertekan ketika harus menyelesaikan banyak tugas akademik secara bersamaan",
    "Saya merasa kesulitan memahami isi materi perkuliahan",
    "Saya merasa kesulitan menguasai materi perkuliahan secara mandiri",
    "Saya merasa kewalahan karena banyaknya kewajiban akademik",
    "Banyaknya tanggung jawab membuat jadwal saya bertabrakan",
    "Saya memiliki terlalu banyak materi perkuliahan yang harus dipelajari",
    "Saya menerima tugas dalam jumlah banyak",
    "Saya merasa tidak punya cukup waktu",
    "Saya sering dikejar tenggat waktu",
    "Saya merasa kurang mampu mengatur waktu belajar",
    "Saya mudah menyerah menghadapi tugas yang sulit",
    "Saya merasa tidak mampu menghadapi tantangan akademik",
    "Saya kesulitan mengatur waktu secara efektif",
    "Saya merasa tidak mendapat dukungan di kelas",
    "Tidak ada orang yang peduli pada saya",
    "Saya tidak merasa didukung keluarga",
    "Saya tidak merasa diberi dukungan oleh teman saat saya stres"
]

opsi_likert = [
    "Sangat Tidak Setuju",
    "Tidak Setuju",
    "Netral",
    "Setuju",
    "Sangat Setuju"
]

# =============================
# CALLBACK AUTO NEXT
# =============================
def auto_next():
    idx = st.session_state.current_q
    jawaban = st.session_state[f"q_{idx}"]

    st.session_state.answers[idx] = jawaban

    if idx < len(questions) - 1:
        st.session_state.current_q += 1
    else:
        st.session_state.page = "result"

    

# =============================
# HOME PAGE
# =============================
if st.session_state.page == "home":

    st.title("DETEKSI INDIKASI BURNOUT MAHASISWA KALTIM")
    st.markdown("""
            Apakah kamu merupakan mahasiswa dari Provinsi Kalimantan Timur yang merasa burnout?
            Sebagai seorang mahasiswa, berbagai tuntutan akademik, non-akademik dan tanggung jawab lainnya terkadang dapat menimbulkan tekanan yang menyebabkan kelelahan yang berkepanjangan. 
            """)
    st.markdown("Melalui tes ini, kamu akan memperoleh gambaran awal mengenai indikasi burnout dalam diri kamu. Indikator pertanyaan yang diberikan telah disesuaikan berdasarkan penelitian yang telah dilakukan menggunakan Analisis Persamaan Struktural dan Random Forest melalui survei pada mahasiswa di Kalimantan Timur.") 
    st.markdown("""
            1. Tes ini memakan waktu sekitar 3-5 menit
            2. Pilihlah jawaban dari setiap pertanyaan dengan jujur dan sesuai dengan keadaan kamu sesungguhnya
            """)


    if st.button("**Mulai Kuis**"):
        st.session_state.page = "quiz"
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.rerun()

# =============================
# QUIZ PAGE (AUTO SLIDE)
# =============================
elif st.session_state.page == "quiz":

    total_q = len(questions)
    idx = st.session_state.current_q

    st.progress((idx + 1) / total_q)
    st.write(f"Pertanyaan {idx + 1} dari {total_q}")

    st.markdown(f"### {questions[idx]}")

    st.radio(
        "",
        opsi_likert,
        index=None,
        key=f"q_{idx}",
        on_change=auto_next
    )

    # Optional tombol previous
    if idx > 0:
        if st.button("Sebelumnya"):
            st.session_state.current_q -= 1
            st.rerun()

# =============================
# RESULT PAGE
# =============================
elif st.session_state.page == "result":

    st.title("**Hasil**")

    def konversi(j):
        return opsi_likert.index(j) + 1

    skor = [konversi(st.session_state.answers[i]) for i in range(len(questions))]

    # SESUAIKAN DENGAN STRUKTUR TRAINING KAMU
    X1 = sum(skor[0:3])
    X2 = sum(skor[3:9])
    X3 = sum(skor[9:13])
    X4 = sum(skor[13:17])

    data_input = pd.DataFrame(
        [[X1, X2, X3, X4]],
        columns=["X1", "X2", "X3", "X4"]
    )

    hasil = model.predict(data_input)[0]

    kategori = {
        1: "Burnout Rendah",
        2: "Burnout Sedang",
        3: "Burnout Tinggi"
    }

    # Tentukan tampilan berdasarkan hasil
    if hasil == 1:
        warna = "rendah"
        judul = "Terdapat Indikasi Burnout Tingkat Rendah"
        deskripsi = "Indikasi burnout tingkat rendah mungkin berbeda pada setiap orang.\
                    Kamu mungkin merasakan: Keluhan fisik ringan dan tidak spesifik seperti sakit kepala atau nyeri punggung disertai rasa lelah dan penurunan efektivitas."

    elif hasil == 2:
        warna = "sedang"
        judul = "Terdapat Indikasi Burnout Tingkat Sedang"
        deskripsi = "Indikasi burnout tingkat sedang mungkin berbeda pada setiap orang. \
                    Kamu mungkin merasakan: muncul gangguan pada aspek kognitif dan emosional, lebih mudah terseinggung, berkurangnya motivasi secara bertahap, munculnya perasaan frustrasi."
                

    else:
        warna = "tinggi"
        judul = "Terdapat Indikasi Burnout Tingkat Tinggi"
        deskripsi = "Indikasi burnout tingkat tinggi mungkin berbeda pada setiap orang. \
                    Kamu mungkin merasakan:Peningkatan perilaku absen, penolakan atau keenganan menyelesaikan tugas, tidak mampu mengontrol pikiran dan tindakan sendiri."

    st.markdown(f"""
    <div class="card {warna}">
        <h2>Hasil Prediksi Kamu</h2>
        <h1>{judul}</h1>
        <p>{deskripsi}</p>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("**Hasil tes ini hanya memberikan gambaran awal mengenai indikasi burnout yang mungkin kamu alami. Untuk hasil yang lebih akurat, silahkan konsultasikan kepada pihak profesional seperti psikolog, konselor, atau tenaga kesehatan.**")
    
    st.markdown(
        """
        <p style='font-size:18px; font-weight:bold; color:#2845D6;'>
        Beberapa cara yang dapat dilakukan untuk mengurangi burnout pada mahasiswa:
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="line-height:1.3; font-size:16px;">

        <b>1. Penanganan berfokus pada masalah</b>

        Fokus pada penyelesaian masalah yang menyebabkan stress dan kelelahan berkepanjangan, seperti:

        <ul style="margin-top:5px;">
        <li>Mengatur jadwal kuliah dan kegiatan lainnya</li>
        <li>Membuat daftar prioritas tugas, membentuk grup belajar</li>
        <li>Mencari solusi langsung terhadap hambatan. Misalnya terkait akademik, maka berkonsultasi secara aktif kepada dosen</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="line-height:1.3; font-size:16px;">

        <b>2. Penangan berfokus pada emosi</b>

        Mengelola perasaan dan emosi terhadap stress, seperti:

        <ul style="margin-top:5px;">
        <li>Melakukan kegiatan akhir pekan yang menyenangkan</li>
        <li>Berbicara kepada teman atau keluarga </li>
        <li>Bergabung dengan komunitas atau kelompok diskusi</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="line-height:1.3; font-size:16px;">

        <b>3. Gaya hidup sehat</b>
       
        Hidup sehat bertujuan menjaga keseimbangan fisik dan sosial melalui kebiasaan secara konsisten, seperti:    

        <ul style="margin-top:5px;">
        <li>Pola makan yang seimbang</li>
        <li>Tidur yang cukup</li>
        <li>Melakukan olahraga dan aktivitas fisik untuk meningkatkan suasana hati</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="line-height:1.3; font-size:16px;">

        <b>4. Peduli terhadap diri sendiri</b>

        Tidak selalu mengkritik atau menyalahkan diri sendiri

        <ul style="margin-top:5px;">
        <li>Memberi izin pada diri untuk beristirahat saat lelah</li>
        <li>Menulis jurnal refleksi</li>
        <li>mencari solusi langsung terhadap hambatan. Misalnya terkait akademik, maka berkonsultasi secara aktif kepada dosen</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)
    

    st.markdown("""
        <div style="line-height:1.3; font-size:12px;">

        <b>Sumber:</b>

        Harnawati, R. A. (2023). Penerapan manajemen stres untuk mengelola stres. Jurnal Kesehatan Panca Bhakti Lampung, 11(2), 117–122.
        Lase, J., & Maria Th, A. D. (2025). Strategi mengatasi burnout dan stres di lingkungan kerja pada generasi Z. MBI (Manajemen dan Bisnis Indonesia), 19(9).
        Raharjo, S. T., & Prahara, S. A. (2022). Mahasiswa yang bekerja: Problem focused coping dengan academic burnout. Jurnal Sudut Pandang (JSP), 2(12).
        Sukadiyanto. (2010). Stress dan cara menguranginya. Cakrawala Pendidikan, 29(1), 55–66.
        Syafira, M., Khotimah, S., & Nugrahayu, E. Y. (2023). Hubungan stres dengan burnout pada mahasiswa program studi kedokteran Fakultas Kedokteran Universitas Mulawarman. Jurnal Kedokteran Mulawarman, 10(1), 11–19.
        Vidyputri, Y. X., Zefanya, N., & Hestyanti, Y. R. (2023). Gambaran strategi coping pada mahasiswa yang mengalami academic burnout di masa pandemi. Jurnal Muara Ilmu Sosial, Humaniora, dan Seni, 7(1), 10–18.

        </div>
        """, unsafe_allow_html=True)

    
    if st.button("Kembali ke Halaman Utama"):
        st.session_state.page = "home"
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.rerun()
