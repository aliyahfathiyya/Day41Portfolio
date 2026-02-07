# -*- coding: utf-8 -*-

# Menentukan Objective A/B Testing

# 1. Tentukan tujuan utama dari pengujian A/B Testing berdasarkan dataset.
# - Identifikasi metrik yang ingin diukur dalam pengujian.
# - Pastikan objective spesifik dan dapat diuji dengan data.
# - Jelaskan bagaimana pengujian ini dapat berdampak pada bisnis.
# - Goals: Memastikan pengujian memiliki tujuan yang jelas dan dapat diukur.
# 2. Menyusun Hipotesis
# - Buat hipotesis yang dapat diuji secara statistik berdasarkan dataset.
# - Tentukan hipotesis alternatif (H1) dan hipotesis nol (H0).
# - Pastikan hipotesis berhubungan langsung dengan metrik yang digunakan dalam dataset.
# - Jelaskan bagaimana hasil pengujian akan menentukan penerimaan atau penolakan hipotesis.
# - Goals: Membantu student dalam menyusun hipotesis yang kuat dan objektif.
# 3. Merancang Desain Pengujian
# - Tentukan bagaimana pengujian akan dilakukan menggunakan dataset yang diberikan.
# - Pembagian Grup:
# - Control Group: Pengguna yang tetap menggunakan fitur lama.
# - Target Group: Pengguna yang mendapatkan fitur baru.
# - Sample Size: Berikan perkiraan jumlah sampel yang diperlukan.
# - Randomization: Jelaskan bagaimana pengacakan akan dilakukan.
# - Durasi: Tentukan durasi pengujian untuk mengumpulkan data yang cukup.
# - Goals: Merancang pengujian yang terstruktur dan bebas dari bias.

# Eksplorasi Data

import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('data\marketing_AB.csv')

df.head()

df.sample(10)

df.info()

# 1. Index: Row index
# 2. user id: User ID (unique)
# 3. test group: If "ad" the person saw the advertisement, if "psa" they only saw the public service announcement
# 4. converted: If a person bought the product then True, else is False
# 5. total ads: Amount of ads seen by person
# 6. most ads day: Day that the person saw the biggest amount of ads
# 7. most ads hour: Hour of day that the person saw the biggest amount of ads

df.isna().sum()

df[df.duplicated('user id')]

# Objective A/B testing

# ~ Untuk mengetahui apakah dengan adanya perbedaan perlakuan iklan berpengaruh terhadap variabel/metrik dari user.

# Metrik yang diukur
# - Conversion Rate
# - Total ads
# - most ads hour

# ~ pengujian ini berdampak pada bisnis karena dapat digunakan untuk menentukan kelayakan strategi iklan baru dan mengoptimalkan revenue dari iklan.

# # Hipotesis

# Hipotesis Nol (H0): tidak terdapat perbedaan variabel antara kelompok kontrol dan kelompok intervensi (test)

# Hipotesis alternatif (H1): terdapat perbedaan variabel antara kelompok kontrol dan kelompok test

# ~ cara menarik keputusan: aoabila nilai p-value < alpha (0,05) maka H0 ditolak dan H1 diterima sehingga terdapat hubungan antara variabel tersebut dan apabila p-value >= alpha maka H0 gagal ditolak.

# # Merancang Desain Uji

# Kelompok dibagi menjadi kelompok kontrol dan test (yang diberikan perlakuan)

# Jumlah sampel: dilakukan dengan menggunakan (https://www.surveymonkey.com/mp/sample-size-calculator/) dengan CI: 95% dan Margin of error 5% didapatkan minimal sampel 384 sehingga pada data ini dianggap sudah memenuhi minimal sampel.  

# Randomisasi: user sudah diacak ke dalam kelompok kontrol dan test serta tidak overlap

# ## Conversion Rate

# ~ ingin mengevaluasi conversion rate pada kelompok yang mendapatkan ad lebih baik dari psa

# - H0: ad <= psa
# - H1: ad > psa

from statsmodels.stats.proportion import proportions_ztest

psa = df[df['test group'] == 'psa']
ad = df[df['test group'] == 'ad']

conversion = [psa['converted'].sum(),ad['converted'].sum()]
sample_size = [psa.shape[0],ad.shape[0]]

z_stat, p_value = proportions_ztest(count=conversion,nobs=sample_size,alternative='larger')

print(f"P-value: {p_value:.4f}")

cvr_control = psa['converted'].mean()
cvr_test = ad['converted'].mean()

print(f"CVR Control : {cvr_control:.4f}")
print(f"CVR Test    : {cvr_test:.4f}")

alpha = 0.05

if p_value < alpha:
    print("Reject H0 → Conversion rate test group lebih tinggi dari control")
else:
    print("Fail to reject H0 → Tidak ada bukti conversion test lebih tinggi")

# """p-value bernilai > 0,05 sehingga disimpulkan bahwa gagal menolak H0 atau menerima H1. Tingkat convertion rate psa dan ad tidak memiliki nilai yang signifikan secara statistik (ad < psa).

# Convertion rate pada kelompok kontrol (psa) adalah 2% sedangkan pada kelompok test (ad) adalah 1,7%.

# ## Most Ads Hour

# ~ ingin mengetahui perbedaan rata-rata waktu iklan yang tayang pada user

# H_0 : \bar{x}ad \leq \bar{x}psa
# H_1 : \bar{x}ad > \bar{x}psa

ads_hour_control = df[ df['test group'] == 'psa']['most ads hour']
ads_hour_test = df[ df['test group'] == 'ad']['most ads hour']

def ad_normal_test(x):
  # Perform the Anderson-Darling test
  result = stats.anderson(x, dist='norm')

  # Interpretation
  for cv, sig in zip(result.critical_values[2:], result.significance_level[2:]):
    if result.statistic < cv:
        print(f"Fail to reject normality at {sig}% significance level")
    else:
        print(f"Reject normality at {sig}% significance level")

ad_normal_test(ads_hour_control)

ad_normal_test(ads_hour_test)

# Perform the Mann-Whitney U test
stat, p_value = stats.mannwhitneyu(ads_hour_control, ads_hour_test, alternative='greater')

# Print results
print(f"P-value: {p_value}")
print(f"Mean of ads hour test group: {ads_hour_test.mean():.2f}")
print(f"Mean of ads hour control group: {ads_hour_control.mean():.2f}")

# p-value bernilai > 0,05 sehingga H0 gagal ditolak dan H1 ditolak artinya tidak terdapat perbedaan yang signifikan antara rata-rata waktu user melihat iklan, di mana rata-rata kelompok test melihat pada pukul 14.30 dan kelompok kontrol pad apukul 14.48.

## Total Ads

# ~ ingin mengetahui perbedaan jumlah iklan yang tayang pada user

# H0 : total ad < total psa

# H1 : toal ad > total psa

total_ads_control = df[ df['test group'] == 'psa']['total ads']
total_ads_test = df[ df['test group'] == 'ad']['total ads']

ad_normal_test(total_ads_control)

ad_normal_test(total_ads_test)

# Perform the Mann-Whitney U test
stat, p_value = stats.mannwhitneyu(total_ads_control, total_ads_test, alternative='greater')

# Print results
print(f"P-value: {p_value}")
print(f"Total ads view test: {total_ads_test.sum():.2f}")
print(f"Total ads view control: {total_ads_control.sum():.2f}")

# p-value bernilai > 0,05 sehingga H0 gagal ditolak dan H1 ditolak artinya tidak terdapat perbedaan yang signifikan antara jumlah waktu user melihat iklan, di mana jumlah  melihat total 14014701 dan kelompok kontrol pad apukul 5823481."""