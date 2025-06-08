import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

file_path = "Data_Penduduk.xlsx"
dataFrame = pd.read_excel(file_path)
print("Kolom yang tersedia:", dataFrame.columns.tolist())

def buat_pie_profesi():
    hitung_profesi = dataFrame['Profesi'].value_counts()

    warna = ['#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#A0C4FF', '#BDB2FF']

    plt.figure(figsize=(9, 7))
    hitung_profesi.plot(
        kind='pie',  
        autopct=lambda p: f'{p:.1f}%' if p > 5 else '',
        colors=warna,
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.5}
    )
    plt.title("Sebaran Profesi Warga Desa Cibodas", pad=20, fontweight='bold')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('profesi_pie.png', dpi=300)
    plt.close()

def bandingkan_pendidikan_gender():
    df_bersih = dataFrame.dropna(subset=['Pendidikan_Terakhir', 'Jenis_Kelamin'])
    df_bersih['Pendidikan_Terakhir'] = df_bersih['Pendidikan_Terakhir'].str.strip().str.upper()
    df_bersih['Jenis_Kelamin'] = df_bersih['Jenis_Kelamin'].str.strip().str.capitalize()

    if 'ID' not in df_bersih.columns:
        df_bersih['Dummy'] = 1
        values_used = 'Dummy'
    else:
        values_used = 'ID'

    pivot_data = df_bersih.pivot_table(
        index='Pendidikan_Terakhir',
        columns='Jenis_Kelamin',
        values=values_used,
        aggfunc='count'
    ).fillna(0)

    urutan_pendidikan = ['SD', 'SMP', 'SMA', 'D3', 'S1', 'S2']
    pivot_data = pivot_data.reindex(urutan_pendidikan)

    rcParams['font.size'] = 10
    plt.figure(figsize=(12, 6))
    pivot_data.plot(
        kind='bar',
        color=['#FF9AA2', '#A2E1DB'],
        edgecolor='black',
        linewidth=0.5
    )

    plt.title("Perbandingan Pendidikan Terakhir dan Jenis Kelamin", fontweight='bold')
    plt.xlabel("Pendidikan Terakhir", labelpad=10)
    plt.ylabel("Jumlah Warga", labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Jenis Kelamin')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('pendidikan_gender_bar.png', dpi=300)
    plt.close()

def kelompokkan_penghasilan():
    bins = [0, 3_000_000, 6_000_000, 10_000_000, float('inf')]
    labels_penghasilan = ['Sangat Rendah (<3jt)', 'Rendah (3-6jt)', 'Menengah (6-10jt)', 'Tinggi (>10jt)']

    dataFrame['Kategori_Penghasilan'] = pd.cut(
        dataFrame['Penghasilan_Per_Bulan'],
        bins=bins,
        labels=labels_penghasilan
    )

    count_penghasilan = dataFrame['Kategori_Penghasilan'].value_counts()
    
    plt.figure(figsize=(9, 7))
    count_penghasilan.plot(
        kind='pie',
        autopct='%1.1f%%',
        explode=(0.05, 0.05, 0.05, 0.05),
        shadow=True,
        startangle=135,
        colors=['#FFD166', '#06D6A0', '#118AB2', '#EF476F']
    )
    plt.title("Distribusi Kategori Penghasilan Warga", fontweight='bold', pad=20)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('penghasilan_pie.png', dpi=300)
    plt.close()

def main():
    print("Mulai visualisasi data...")
    buat_pie_profesi()
    bandingkan_pendidikan_gender()
    kelompokkan_penghasilan()
    print("Selesai! Cek gambar di folder.")

if __name__ == "__main__":
    main()