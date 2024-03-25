# INDOML: Machine Learning Library untuk Indonesia

INDOML adalah sebuah perpustakaan Machine Learning yang dirancang khusus untuk mendukung pengembangan dan implementasi proyek-proyek AI di Indonesia. Library ini menyediakan serangkaian alat dan model yang telah disesuaikan untuk memenuhi kebutuhan spesifik pengembang dan peneliti di Indonesia, termasuk dukungan untuk bahasa Indonesia dan dataset lokal.

## Fitur Utama

- **Dukungan Bahasa Indonesia:** INDOML hadir dengan model yang telah dilatih khusus untuk bahasa Indonesia, memungkinkan analisis semantik, pengolahan bahasa alami, dan tugas-tugas lainnya dengan akurasi yang tinggi.
- **Dataset Lokal:** Akses ke koleksi dataset lokal yang kaya, dari teks hingga gambar, yang relevan dengan konteks Indonesia untuk pelatihan dan pengujian model.
- **Pretrained Models:** Berbagai model yang telah dilatih sebelumnya, siap untuk digunakan atau dikustomisasi lebih lanjut sesuai dengan kebutuhan proyek Anda.
- **Alat Visualisasi:** Alat-alat visualisasi yang memudahkan analisis data dan interpretasi model.
- **Kompatibilitas:** Mudah diintegrasikan dengan framework machine learning populer seperti TensorFlow dan PyTorch.

## Instalasi

INDOML dapat dengan mudah diinstal menggunakan pip. Jalankan perintah berikut di terminal Anda:

<pre><div class="dark bg-gray-950 rounded-md"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>sh</span><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 3.5C10.8954 3.5 10 4.39543 10 5.5H14C14 4.39543 13.1046 3.5 12 3.5ZM8.53513 3.5C9.22675 2.3044 10.5194 1.5 12 1.5C13.4806 1.5 14.7733 2.3044 15.4649 3.5H17.25C18.9069 3.5 20.25 4.84315 20.25 6.5V18.5C20.25 20.1569 19.1569 21.5 17.25 21.5H6.75C5.09315 21.5 3.75 20.1569 3.75 18.5V6.5C3.75 4.84315 5.09315 3.5 6.75 3.5H8.53513ZM8 5.5H6.75C6.19772 5.5 5.75 5.94772 5.75 6.5V18.5C5.75 19.0523 6.19772 19.5 6.75 19.5H17.25C18.0523 19.5 18.25 19.0523 18.25 18.5V6.5C18.25 5.94772 17.8023 5.5 17.25 5.5H16C16 6.60457 15.1046 7.5 14 7.5H10C8.89543 7.5 8 6.60457 8 5.5Z" fill="currentColor"></path></svg>Copy code</button></span></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-sh">pip install INDOML
</code></div></div></pre>

Pastikan Anda memiliki Python versi 3.6 atau lebih baru.

## Mulai Cepat

Untuk memulai dengan cepat, Anda bisa mengikuti contoh kode berikut untuk menggunakan model Bagging bersama dengan Decision Tree Classifier sebagai model dasar:

<pre><div class="dark bg-gray-950 rounded-md"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>python</span><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 3.5C10.8954 3.5 10 4.39543 10 5.5H14C14 4.39543 13.1046 3.5 12 3.5ZM8.53513 3.5C9.22675 2.3044 10.5194 1.5 12 1.5C13.4806 1.5 14.7733 2.3044 15.4649 3.5H17.25C18.9069 3.5 20.25 4.84315 20.25 6.5V18.5C20.25 20.1569 19.1569 21.5 17.25 21.5H6.75C5.09315 21.5 3.75 20.1569 3.75 18.5V6.5C3.75 4.84315 5.09315 3.5 6.75 3.5H8.53513ZM8 5.5H6.75C6.19772 5.5 5.75 5.94772 5.75 6.5V18.5C5.75 19.0523 6.19772 19.5 6.75 19.5H17.25C18.0523 19.5 18.25 19.0523 18.25 18.5V6.5C18.25 5.94772 17.8023 5.5 17.25 5.5H16C16 6.60457 15.1046 7.5 14 7.5H10C8.89543 7.5 8 6.60457 8 5.5Z" fill="currentColor"></path></svg>Copy code</button></span></div><div class="p-4 overflow-y-auto"><sider-code-explain id="sider-code-explain" data-gpts-theme="light"><div class="chat-gpt-quick-query-container"><div class="sider-code-explain-button-wrapper-common"><button class="sider-code-explain-button"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M5.68295 2C6.70532 2 7.54943 2.78898 7.67665 3.8101L7.67665 4H5.80113C5.75613 4 5.71253 4.01612 5.67779 4.04561L4.8942 4.71084C4.83578 4.6825 4.77053 4.66667 4.70169 4.66667C4.45167 4.66667 4.24898 4.8756 4.24898 5.13333C4.24898 5.39107 4.45167 5.6 4.70169 5.6C4.95172 5.6 5.1544 5.39107 5.1544 5.13333C5.1544 5.09411 5.14971 5.05602 5.14087 5.01962L5.87066 4.4H7.67665V7.8L4.0114 7.80002C3.93875 7.64234 3.78285 7.53333 3.60225 7.53333C3.35223 7.53333 3.14954 7.74227 3.14954 8C3.14954 8.25773 3.35223 8.46667 3.60225 8.46667C3.78283 8.46667 3.93871 8.35769 4.01137 8.20005L7.67665 8.2V11.6H5.87066L5.14087 10.9804C5.14971 10.944 5.1544 10.9059 5.1544 10.8667C5.1544 10.6089 4.95172 10.4 4.70169 10.4C4.45167 10.4 4.24898 10.6089 4.24898 10.8667C4.24898 11.1244 4.45167 11.3333 4.70169 11.3333C4.77053 11.3333 4.83578 11.3175 4.8942 11.2892L5.67779 11.9544C5.71253 11.9839 5.75613 12 5.80113 12H7.67665L7.67665 12.19C7.53504 13.2133 6.67959 14 5.65053 14C4.702 14 3.90447 13.3316 3.67452 12.4257C2.98645 12.1157 2.50543 11.4064 2.50543 10.581C2.50543 10.3864 2.53217 10.1982 2.58209 10.0202C1.9669 9.68964 1.54411 9.02923 1.53294 8.26565L1.53271 8.2C1.53271 7.36486 2.02928 6.64928 2.73466 6.34987C2.60485 6.10439 2.5248 5.82672 2.50852 5.53139L2.50673 5.49159C2.50413 5.4503 2.50281 5.40864 2.50281 5.36667C2.50281 4.53921 3.01594 3.8353 3.73207 3.57461C3.94984 2.6702 4.74069 2 5.68295 2Z" fill="currentColor"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12.2734 3.59773C12.0636 2.68163 11.2673 2 10.3171 2C9.29472 2 8.45061 2.78898 8.32338 3.8101V12.19C8.46499 13.2133 9.32044 14 10.3495 14C11.298 14 12.0956 13.3316 12.3255 12.4257C13.0136 12.1157 13.4946 11.4064 13.4946 10.581C13.4946 10.3864 13.4679 10.1982 13.4179 10.0202C14.0415 9.68517 14.4673 9.01132 14.4673 8.23464C14.4673 7.53577 14.1225 6.92015 13.5992 6.55985C13.5968 6.59869 13.5834 6.63721 13.5585 6.67023C13.1689 7.18747 12.7286 7.51297 12.2439 7.64614C12.235 7.67034 12.2262 7.69666 12.2179 7.72495C12.1766 7.86578 12.1552 8.02272 12.1631 8.19103C12.1697 8.33136 12.1967 8.47381 12.2473 8.6176C12.284 8.72199 12.2319 8.83738 12.1309 8.87534C12.03 8.9133 11.9184 8.85944 11.8816 8.75506C11.8175 8.57273 11.7829 8.39053 11.7745 8.21058C11.7662 8.03442 11.7829 7.86786 11.8182 7.71364C11.3286 7.73647 10.7996 7.58187 10.2368 7.24953C10.1435 7.19444 10.1111 7.07159 10.1644 6.97514C10.2177 6.87869 10.3365 6.84517 10.4298 6.90026L10.4643 6.9204C11.6 7.57618 12.5085 7.36099 13.2541 6.3709C13.4073 6.08954 13.4946 5.76481 13.4946 5.41899C13.4946 4.58509 12.9867 3.87382 12.2734 3.59773ZM9.29072 10.3742C9.25083 10.2711 9.29938 10.1541 9.39914 10.1128C9.49534 10.0731 9.60404 10.1183 9.64745 10.2141L9.65199 10.2249L9.66035 10.2429C9.67743 10.2779 9.70278 10.3199 9.73685 10.3641C9.79288 10.4367 9.86143 10.5 9.94329 10.5484C10.1435 10.6666 10.4046 10.6877 10.7488 10.5692C11.031 10.3804 11.3822 10.2904 11.7985 10.3029C11.9058 10.3061 11.9904 10.3987 11.9873 10.5097C11.9842 10.6207 11.8946 10.7081 11.7872 10.7049C11.0216 10.6821 10.5702 11.0581 10.3872 11.8781C10.3631 11.9863 10.2586 12.0538 10.154 12.0288C10.0493 12.0039 9.98396 11.8959 10.0081 11.7877C10.0721 11.501 10.1677 11.2546 10.2939 11.0496C10.0914 11.0445 9.90988 10.9919 9.75026 10.8976C9.5263 10.7653 9.3829 10.5793 9.30197 10.4007L9.30013 10.3966L9.29072 10.3742ZM10.1774 3.87702C10.07 3.87963 9.98496 3.97176 9.98748 4.0828C9.99567 4.44343 10.0709 4.75308 10.211 5.00946C9.87934 5.0337 9.55545 5.21444 9.26077 5.5776C9.19172 5.6627 9.20247 5.78956 9.28479 5.86094C9.36711 5.93232 9.48981 5.92121 9.55886 5.83611C9.79929 5.5398 10.0381 5.41437 10.2729 5.40904C10.3671 5.40691 10.4574 5.42463 10.5416 5.45708C10.5929 5.47681 10.6355 5.49935 10.6676 5.52025L10.6837 5.53124L10.6937 5.53857C10.6981 5.54159 10.7026 5.54441 10.7072 5.54694C10.9276 5.69287 11.1976 5.79553 11.5155 5.8534C11.6213 5.87267 11.7222 5.79961 11.7408 5.69022C11.7595 5.58082 11.6888 5.47653 11.583 5.45726C11.3135 5.4082 11.0909 5.3252 10.9135 5.2066L10.8962 5.19416L10.8763 5.18076C10.5506 4.94521 10.388 4.58 10.3765 4.07336C10.3739 3.96232 10.2848 3.87441 10.1774 3.87702Z" fill="currentColor"></path></svg>Menjelaskan</button></div></div></sider-code-explain><code class="!whitespace-pre hljs language-python">from sklearn.tree import DecisionTreeClassifier
from INDOML.model.ensemble import Bagging

# Membuat model dasar
model = DecisionTreeClassifier()

# Membuat objek Bagging
bagging = Bagging(model, n_model=10, random_state=42)

# Melakukan training dan prediksi
y_pred = bagging.fit_predict(X_train, y_train)

# Menghitung akurasi
akurasi = bagging.score_accuracy(y_pred, y_test)

print(f"Akurasi Model: {akurasi*100:.2f}%")
</code></div></div></pre>

Dalam contoh di atas, kita menggunakan `DecisionTreeClassifier` dari `sklearn` sebagai model dasar untuk metode `Bagging` yang disediakan oleh INDOML. Ini merupakan cara sederhana untuk meningkatkan performa model klasifikasi melalui teknik ensemble.

## Dokumentasi

Untuk informasi lebih lanjut tentang penggunaan INDOML, termasuk tutorial lengkap, API reference, dan panduan pengembangan, kunjungi [Dokumentasi Resmi INDOML]().

## Kontribusi

INDOML adalah proyek open-source dan kontribusi dari komunitas sangat dihargai. Jika Anda ingin berkontribusi, silakan lihat [panduan kontribusi]() di situs resmi kami.

## Lisensi

INDOML dilisensikan di bawah [GNU General Public License (GPL)](). GPL adalah lisensi perangkat lunak bebas yang menjamin pengguna akhir kebebasan untuk menjalankan, mempelajari, berbagi, dan memodifikasi perangkat lunak. Menggunakan GPL sebagai lisensi berarti setiap kode yang dihasilkan dari kode yang telah dilisensikan di bawah GPL harus juga dilisensikan di bawah GPL. Ini menciptakan kondisi yang menguntungkan untuk pengembangan perangkat lunak bebas dan terbuka.

Untuk informasi lebih lanjut tentang kondisi dan batasan yang diberlakukan oleh GNU GPL, silakan kunjungi [tautan resmi GNU GPL]().

## Dukungan

Jika Anda memiliki pertanyaan atau memerlukan bantuan mengenai INDOML, jangan ragu untuk bergabung dengan [komunitas INDOML]() atau kirimkan pertanyaan Anda melalui [sistem tiket dukungan]().

---

Dengan fitur dan dukungan yang kaya, INDOML bertujuan untuk memperkuat ekosistem AI di Indonesia dan membantu pengembang serta peneliti dalam menciptakan solusi inovatif yang relevan dengan kebutuhan lokal. Mari bersama-sama mendorong batas kemungkinan AI di Indonesia dengan INDOML!
